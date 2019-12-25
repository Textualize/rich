from dataclasses import dataclass
from typing import Any, ClassVar, Dict, Iterable, List, Optional, Union

from commonmark.blocks import Parser

from . import box
from .console import (
    Console,
    ConsoleOptions,
    ConsoleRenderable,
    RenderResult,
    Segment,
)
from .containers import Renderables
from .panel import Panel
from .style import Style, StyleStack
from .syntax import Syntax
from .text import Lines, Text
from ._stack import Stack
from ._tools import iter_first, iter_first_last


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

    def __console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":
        return
        yield


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
        self.text.append(text, context.current_style)

    def on_leave(self, context: "MarkdownContext") -> None:
        context.leave_style()

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        yield self.text


class Paragraph(TextElement):
    """A Paragraph."""

    style_name = "markdown.paragraph"

    @classmethod
    def create(cls, markdown: "Markdown", node) -> "Paragraph":
        return cls(justify=markdown.justify)

    def __init__(self, justify: str) -> None:
        self.justify = justify

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        self.text.justify = self.justify
        yield self.text


class Heading(TextElement):
    """A heading."""

    @classmethod
    def create(cls, markdown: "Markdown", node: Any) -> "Heading":
        heading = Heading(node.level)
        return heading

    def on_enter(self, context: "MarkdownContext") -> None:
        self.text = Text()
        context.enter_style(self.style_name)

    def __init__(self, level: int) -> None:
        self.level = level
        self.style_name = f"markdown.h{level}"
        super().__init__()

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        text = self.text
        text.justify = "center"
        if self.level == 1:
            # Draw a border around h1s
            yield Panel(
                text, box=box.DOUBLE, style="markdown.h1.border",
            )
        else:
            # Styled text for h2 and beyond
            yield text


class CodeBlock(TextElement):
    """A code block with syntax highlighting."""

    style_name = "markdown.code_block"

    @classmethod
    def create(cls, markdown: "Markdown", node: Any) -> "ListElement":
        if node.info is None:
            return cls("default", markdown.code_theme)
        lexer_name, _, _ = node.info.partition(" ")
        return cls(lexer_name, markdown.code_theme)

    def __init__(self, lexer_name: str, theme: str) -> None:
        self.lexer_name = lexer_name
        self.theme = theme

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        code = str(self.text).rstrip()
        syntax = Syntax(code, self.lexer_name, theme=self.theme)
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

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        # Render surrounded by quotes.
        render_options = options.update(width=options.max_width - 4)
        lines = console.render_lines(self.elements, render_options, style=self.style)

        style = self.style
        new_line = Segment("\n")
        left_quote = Segment("“ ", style)
        right_quote = Segment(" ”", style)
        padding = Segment("  ", style)

        for first, last, line in iter_first_last(lines):
            yield left_quote if first else padding
            yield from line
            yield right_quote if last else padding
            yield new_line


class HorizontalRule(MarkdownElement):
    """A horizontal rule to divide secions."""

    new_line = False

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        style = console.get_style("markdown.hr")
        yield Segment(f'{"─" * options.max_width}\n', style)


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

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
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
        bullet_style = console.get_style("markdown.item.bullet")

        bullet = Segment(" • ", bullet_style)
        padding = Segment(" " * 3, bullet_style)
        new_line = Segment("\n")
        for first, line in iter_first(lines):
            yield bullet if first else padding
            yield from line
            yield new_line

    def render_number(
        self, console: Console, options: ConsoleOptions, number: int, last_number: int
    ) -> RenderResult:
        number_width = len(str(last_number)) + 2
        render_options = options.update(width=options.max_width - number_width)
        lines = console.render_lines(self.elements, render_options, style=self.style)
        number_style = console.get_style("markdown.item.number")

        new_line = Segment("\n")
        padding = Segment(" " * number_width, number_style)
        numeral = Segment(f"{number}".rjust(number_width - 1) + " ", number_style)
        for first, line in iter_first(lines):
            yield numeral if first else padding
            yield from line
            yield new_line


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

    @property
    def width(self) -> int:
        """The width of the console."""
        return self.options.max_width

    def on_text(self, text: str) -> None:
        """Called when the parser visits text."""
        self.stack.top.on_text(self, text)

    def enter_style(self, style_name: Union[str, Style]) -> Style:
        """Enter a style context."""
        style = self.console.get_style(style_name)
        self.style_stack.push(style)
        return self.current_style

    def leave_style(self) -> Style:
        """Leave a style context."""
        style = self.style_stack.pop()
        return style


class Markdown:

    elements: ClassVar[Dict[str, MarkdownElement]] = {
        "paragraph": Paragraph,
        "heading": Heading,
        "code_block": CodeBlock,
        "block_quote": BlockQuote,
        "thematic_break": HorizontalRule,
        "list": ListElement,
        "item": ListItem,
    }
    inlines = {"emph", "strong", "code", "link"}

    def __init__(
        self,
        markup: str,
        code_theme: str = "monokai",
        justify: str = None,
        style: Union[str, Style] = "none",
    ) -> None:
        """Parses the markup."""
        self.markup = markup
        parser = Parser()
        self.parsed = parser.parse(markup)
        self.code_theme = code_theme
        self.justify = justify
        self.style = style

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        """Render markdown to the console."""
        style = console.get_style(self.style)
        context = MarkdownContext(console, options, style)
        nodes = self.parsed.walker()
        inlines = self.inlines
        new_line = False
        for current, entering in nodes:
            # print(current, current.literal)
            node_type = current.t
            if node_type in ("html_inline", "html_block", "text"):
                context.on_text(current.literal)
            elif node_type == "softbreak":
                if entering:
                    context.on_text("\n")
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
                if current.destination and not entering:
                    context.on_text(" (")
                    context.enter_style("markdown.link_url")
                    context.on_text(current.destination)
                    context.leave_style()
                    context.on_text(") ")
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


markup = """
An h1 header
============

Paragraphs are separated by a blank line.

2nd paragraph. *Italic*, **bold**, and `monospace`. Itemized lists look like:

  * this one
  * that one
  * the other one

Note that --- not considering the asterisk --- the actual text content starts at 4-columns in.

> Block quotes are
> written like so.
>
> They can span multiple paragraphs,
> if you like.

Use 3 dashes for an em-dash. Use 2 dashes for ranges (ex., "it's all in chapters 12--14"). Three dots ... will be converted to an ellipsis. Unicode is supported. ☺


An h2 header
------------

```python
    @classmethod
    def adjust_line_length(
        cls, line: List[Segment], length: int, style: Style = None
    ) -> List[Segment]:        
        line_length = sum(len(text) for text, _style in line)
        if line_length < length:
            return line[:] + [Segment(" " * (length - line_length), style)]
        elif line_length > length:
            line_length = 0
            new_line: List[Segment] = []
            append = new_line.append
            for segment in line:
                segment_length = len(segment.text)
                if line_length + segment_length < length:
                    append(segment)
                    line_length += segment_length
                else:
                    text, style = segment
                    append(Segment(text[: length - line_length], style))
                    break
            return new_line
        return line
```


"""

# markup = """\
# # Heading

# This is `code`!
# Hello, *World*!
# **Bold**

# """


if __name__ == "__main__":  # pragma: no cover
    from .console import Console

    console = Console(record=True, width=90)
    # print(console.size)

    # markup = "<foo>"
    md = Markdown(markup)

    console.print(md)
    print(console)
    # print(console.render_spans())

    # from .color import Color
    # from .style import Style

    # print(Color.downgrade.cache_info())
    # print(Color.parse.cache_info())
    # print(Color.get_ansi_codes.cache_info())

    # Style.parse("on red")

    # print(Style.parse.cache_info())
