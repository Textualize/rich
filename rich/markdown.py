from dataclasses import dataclass
from typing import Any, ClassVar, Dict, Iterable, List, Optional, Type, Union

from commonmark.blocks import Parser

from . import box
from ._loop import loop_first, loop_first_last
from ._stack import Stack
from .console import (
    Console,
    ConsoleOptions,
    ConsoleRenderable,
    JustifyValues,
    RenderResult,
    Segment,
)
from .containers import Renderables
from .jupyter import JupyterMixin
from .panel import Panel
from .rule import Rule
from .style import Style, StyleStack
from .syntax import Syntax
from .text import Lines, Text


class MarkdownElement:

    new_line: ClassVar[bool] = True

    @classmethod
    def create(cls, markdown: "Markdown", node: Any) -> "MarkdownElement":
        """Factory to create markdown element,
        
        Args:
            markdown (Markdown): THe parent Markdown object.
            node (Any): A node from Pygments.
        
        Returns:
            MarkdownElement: A new markdown element
        """
        return cls()

    def on_enter(self, context: "MarkdownContext"):
        """Called when the node is entered.
        
        Args:
            context (MarkdownContext): The markdown context.
        """

    def on_text(self, context: "MarkdownContext", text: str) -> None:
        """Called when text is parsed.
        
        Args:
            context (MarkdownContext): The markdown context.
        """

    def on_leave(self, context: "MarkdownContext") -> None:
        """Called when the parser leaves the element.
        
        Args:
            context (MarkdownContext): [description]
        """

    def on_child_close(
        self, context: "MarkdownContext", child: "MarkdownElement"
    ) -> bool:
        """Called when a child element is closed.

        This method allows a parent element to take over rendering of its children.
        
        Args:
            context (MarkdownContext): The markdown context.
            child (MarkdownElement): The child markdown element.
        
        Returns:
            bool: Return True to render the element, or False to not render the element.
        """
        return True

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":
        return ()


class UnknownElement(MarkdownElement):
    """An unknown element.
    
    Hopefully there will be no unknown elements, and we will have a MarkdownElement for
    everything in the document.
    
    """


class TextElement(MarkdownElement):
    """Base class for elements that render text."""

    style_name = "none"

    def on_enter(self, context: "MarkdownContext") -> None:
        self.style = context.enter_style(self.style_name)
        self.text = Text(justify="left")

    def on_text(self, context: "MarkdownContext", text: str) -> None:
        text = text.replace("---", "—").replace("--", "–").replace("...", "…")
        self.text.append(text, context.current_style)

    def on_leave(self, context: "MarkdownContext") -> None:
        context.leave_style()


class Paragraph(TextElement):
    """A Paragraph."""

    style_name = "markdown.paragraph"
    justify: JustifyValues

    @classmethod
    def create(cls, markdown: "Markdown", node) -> "Paragraph":
        return cls(justify=markdown.justify or "left")

    def __init__(self, justify: JustifyValues) -> None:
        self.justify = justify

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        self.text.justify = self.justify
        yield self.text


class Heading(TextElement):
    """A heading."""

    @classmethod
    def create(cls, markdown: "Markdown", node: Any) -> "Heading":
        heading = cls(node.level)
        return heading

    def on_enter(self, context: "MarkdownContext") -> None:
        self.text = Text()
        context.enter_style(self.style_name)

    def __init__(self, level: int) -> None:
        self.level = level
        self.style_name = f"markdown.h{level}"
        super().__init__()

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        text = self.text
        text.justify = "center"
        if self.level == 1:
            # Draw a border around h1s
            yield Panel(
                text, box=box.DOUBLE, style="markdown.h1.border",
            )
        else:
            # Styled text for h2 and beyond
            if self.level == 2:
                yield Text("\n")
            yield text


class CodeBlock(TextElement):
    """A code block with syntax highlighting."""

    style_name = "markdown.code_block"

    @classmethod
    def create(cls, markdown: "Markdown", node: Any) -> "CodeBlock":
        node_info = node.info or ""
        lexer_name = node_info.partition(" ")[0]
        return cls(lexer_name or "default", markdown.code_theme)

    def __init__(self, lexer_name: str, theme: str) -> None:
        self.lexer_name = lexer_name
        self.theme = theme

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        code = str(self.text).rstrip()
        syntax = Panel(
            Syntax(code, self.lexer_name, theme=self.theme), style="dim", box=box.SQUARE
        )
        yield syntax


class BlockQuote(TextElement):
    """A block quote."""

    style_name = "markdown.block_quote"

    def __init__(self) -> None:
        self.elements: Renderables = Renderables()

    def on_child_close(
        self, context: "MarkdownContext", child: "MarkdownElement"
    ) -> bool:
        self.elements.append(child)
        return False

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        render_options = options.update(width=options.max_width - 4)
        lines = console.render_lines(self.elements, render_options, style=self.style)
        style = self.style
        new_line = Segment("\n")
        padding = Segment("▌ ", style)
        for line in lines:
            yield padding
            yield from line
            yield new_line


class HorizontalRule(MarkdownElement):
    """A horizontal rule to divide secions."""

    new_line = False

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        style = console.get_style("markdown.hr", default="none")
        yield Rule(style=style)


class ListElement(MarkdownElement):
    """A list element."""

    @classmethod
    def create(cls, markdown: "Markdown", node: Any) -> "ListElement":
        list_data = node.list_data
        return cls(list_data["type"], list_data["start"])

    def __init__(self, list_type: str, list_start: Optional[int]) -> None:
        self.items: List[ListItem] = []
        self.list_type = list_type
        self.list_start = list_start

    def on_child_close(
        self, context: "MarkdownContext", child: "MarkdownElement"
    ) -> bool:
        assert isinstance(child, ListItem)
        self.items.append(child)
        return False

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        if self.list_type == "bullet":
            for item in self.items:
                yield from item.render_bullet(console, options)
        else:
            number = 1 if self.list_start is None else self.list_start
            last_number = number + len(self.items)
            for item in self.items:
                yield from item.render_number(console, options, number, last_number)
                number += 1


class ListItem(TextElement):
    """An item in a list."""

    style_name = "markdown.item"

    def __init__(self) -> None:
        self.elements: Renderables = Renderables()

    def on_child_close(
        self, context: "MarkdownContext", child: "MarkdownElement"
    ) -> bool:
        self.elements.append(child)
        return False

    def render_bullet(self, console: Console, options: ConsoleOptions) -> RenderResult:
        render_options = options.update(width=options.max_width - 3)
        lines = console.render_lines(self.elements, render_options, style=self.style)
        bullet_style = console.get_style("markdown.item.bullet", default="none")

        bullet = Segment(" • ", bullet_style)
        padding = Segment(" " * 3, bullet_style)
        new_line = Segment("\n")
        for first, line in loop_first(lines):
            yield bullet if first else padding
            yield from line
            yield new_line

    def render_number(
        self, console: Console, options: ConsoleOptions, number: int, last_number: int
    ) -> RenderResult:
        number_width = len(str(last_number)) + 2
        render_options = options.update(width=options.max_width - number_width)
        lines = console.render_lines(self.elements, render_options, style=self.style)
        number_style = console.get_style("markdown.item.number", default="none")

        new_line = Segment("\n")
        padding = Segment(" " * number_width, number_style)
        numeral = Segment(f"{number}".rjust(number_width - 1) + " ", number_style)
        for first, line in loop_first(lines):
            yield numeral if first else padding
            yield from line
            yield new_line


class ImageItem(TextElement):
    """Renders a placeholder for an image."""

    new_line = False

    @classmethod
    def create(cls, markdown: "Markdown", node: Any) -> "MarkdownElement":
        """Factory to create markdown element,
        
        Args:
            markdown (Markdown): THe parent Markdown object.
            node (Any): A node from Pygments.
        
        Returns:
            MarkdownElement: A new markdown element
        """
        return cls(node.destination, markdown.hyperlinks)

    def __init__(self, destination: str, hyperlinks: bool) -> None:
        self.destination = destination
        self.hyperlinks = hyperlinks
        self.link: Optional[str] = None
        super().__init__()

    def on_enter(self, context: "MarkdownContext") -> None:
        self.link = context.current_style.link
        self.text = Text(justify="left")
        super().on_enter(context)

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        link_style = Style(link=self.link or self.destination or None)
        title = self.text or Text(self.destination.strip("/").rsplit("/", 1)[-1])

        if self.hyperlinks:
            title.stylize_all(link_style)
        yield Text.assemble("🌆 ", title, " ", end="")


class MarkdownContext:
    """Manages the console render state."""

    def __init__(self, console: Console, options: ConsoleOptions, style: Style) -> None:
        self.console = console
        self.options = options
        self.style_stack: StyleStack = StyleStack(style)
        self.stack: Stack[MarkdownElement] = Stack()

    @property
    def current_style(self) -> Style:
        """Current style which is the product of all styles on the stack."""
        return self.style_stack.current

    def on_text(self, text: str) -> None:
        """Called when the parser visits text."""
        self.stack.top.on_text(self, text)

    def enter_style(self, style_name: Union[str, Style]) -> Style:
        """Enter a style context."""
        style = self.console.get_style(style_name, default="none")
        self.style_stack.push(style)
        return self.current_style

    def leave_style(self) -> Style:
        """Leave a style context."""
        style = self.style_stack.pop()
        return style


class Markdown(JupyterMixin):
    """A Markdown renderable.

    Args:
        markup (str): A string containing markdown.
        code_theme (str, optional): Pygments theme for code blocks. Defaults to "monokai".
        justify (JustifyValues, optional): Justify value for paragraphs. Defaults to None.
        style (Union[str, Style], optional): Optional style to apply to markdown.
        hyperlinks (bool, optional): Enable hyperlinks. Defaults to ``True``.
    """

    elements: ClassVar[Dict[str, Type[MarkdownElement]]] = {
        "paragraph": Paragraph,
        "heading": Heading,
        "code_block": CodeBlock,
        "block_quote": BlockQuote,
        "thematic_break": HorizontalRule,
        "list": ListElement,
        "item": ListItem,
        "image": ImageItem,
    }
    inlines = {"emph", "strong", "code", "strike"}

    def __init__(
        self,
        markup: str,
        code_theme: str = "monokai",
        justify: JustifyValues = None,
        style: Union[str, Style] = "none",
        hyperlinks: bool = True,
    ) -> None:
        self.markup = markup
        parser = Parser()
        self.parsed = parser.parse(markup)
        self.code_theme = code_theme
        self.justify = justify
        self.style = style
        self.hyperlinks = hyperlinks

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        """Render markdown to the console."""
        style = console.get_style(self.style, default="none")
        context = MarkdownContext(console, options, style)
        nodes = self.parsed.walker()
        inlines = self.inlines
        new_line = False
        for current, entering in nodes:
            node_type = current.t
            if node_type in ("html_inline", "html_block", "text"):
                context.on_text(current.literal.replace("\n", " "))
            elif node_type == "linebreak":
                if entering:
                    context.on_text("\n")
            elif node_type == "softbreak":
                if entering:
                    context.on_text(" ")
            elif node_type == "link":
                if entering:
                    link_style = console.get_style("markdown.link", default="none")
                    if self.hyperlinks:
                        link_style += Style(link=current.destination)
                    context.enter_style(link_style)
                else:
                    context.leave_style()
                    if not self.hyperlinks:
                        context.on_text(" (")
                        style = Style(underline=True) + console.get_style(
                            "markdown.link_url", default="none"
                        )
                        context.enter_style(style)
                        context.on_text(current.destination)
                        context.leave_style()
                        context.on_text(")")
            elif node_type in inlines:
                if current.is_container():
                    if entering:
                        context.enter_style(f"markdown.{node_type}")
                    else:
                        context.leave_style()
                else:
                    context.enter_style(f"markdown.{node_type}")
                    if current.literal:
                        context.on_text(current.literal)
                    context.leave_style()
            else:
                element_class = self.elements.get(node_type) or UnknownElement
                if current.is_container():
                    if entering:
                        element = element_class.create(self, current)
                        context.stack.push(element)
                        element.on_enter(context)
                    else:
                        element = context.stack.pop()
                        if context.stack:
                            if context.stack.top.on_child_close(context, element):
                                if new_line:
                                    yield Segment("\n")
                                yield from console.render(element, context.options)
                                element.on_leave(context)
                            else:
                                element.on_leave(context)
                        else:
                            element.on_leave(context)
                            yield from console.render(element, context.options)
                        new_line = element.new_line
                else:
                    element = element_class.create(self, current)

                    context.stack.push(element)
                    element.on_enter(context)
                    if current.literal:
                        element.on_text(context, current.literal.rstrip())
                    context.stack.pop()
                    if new_line:
                        yield Segment("\n")
                    yield from console.render(element, context.options)
                    element.on_leave(context)
                    new_line = element.new_line


if __name__ == "__main__":  # pragma: no cover

    import argparse

    parser = argparse.ArgumentParser(
        description="Render Markdown to the console with Rich"
    )
    parser.add_argument("path", metavar="PATH", help="path to markdown file")
    parser.add_argument(
        "-c",
        "--force-color",
        dest="force_color",
        action="store_true",
        help="force color for non-terminals",
    )
    parser.add_argument(
        "-t",
        "--code-theme",
        dest="code_theme",
        default="monokai",
        help="pygments code theme",
    )
    parser.add_argument(
        "-y",
        "--hyperlinks",
        dest="hyperlinks",
        action="store_true",
        help="enable hyperlinks",
    )
    parser.add_argument(
        "-w",
        "--width",
        type=int,
        dest="width",
        default=None,
        help="width of output (default will auto-detect)",
    )
    parser.add_argument(
        "-j",
        "--justify",
        dest="justify",
        action="store_true",
        help="enable full text justify",
    )
    parser.add_argument(
        "-p",
        "--page",
        dest="page",
        action="store_true",
        help="use pager to scroll output",
    )
    args = parser.parse_args()

    from rich.console import Console

    with open(args.path, "rt", encoding="utf-8") as markdown_file:
        markdown = Markdown(
            markdown_file.read(),
            justify="full" if args.justify else "left",
            code_theme=args.code_theme,
            hyperlinks=args.hyperlinks,
        )
    if args.page:
        import pydoc
        import io

        console = Console(
            file=io.StringIO(), force_terminal=args.force_color, width=args.width
        )
        console.print(markdown)
        pydoc.pager(console.file.getvalue())  # type: ignore

    else:
        console = Console(force_terminal=args.force_color, width=args.width)
        console.print(markdown)
