from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Dict, Iterable, List, Optional, Union

from commonmark.blocks import Parser

from .console import (
    Console,
    ConsoleOptions,
    ConsoleRenderable,
    RenderResult,
    Segment,
)
from .panel import DOUBLE_BORDER, Panel
from .style import Style, StyleStack
from .syntax import Syntax
from .text import Lines, Text
from ._stack import Stack
from ._tools import iter_first, iter_first_last


class MarkdownElement:

    new_line: ClassVar[bool] = True

    @classmethod
    def create(cls, markdown: Markdown, node: Any) -> MarkdownElement:
        return cls()

    def on_enter(self, context: MarkdownContext):
        pass

    def on_text(self, context: MarkdownContext, text: str) -> None:
        pass

    def on_leave(self, context: MarkdownContext) -> None:
        pass

    def on_child_close(self, context: MarkdownContext, child: MarkdownElement) -> bool:
        return True

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        return
        yield


class UnknownElement(MarkdownElement):
    pass


class TextElement(MarkdownElement):

    style_name = "none"

    def on_enter(self, context: MarkdownContext) -> None:
        self.style = context.enter_style(self.style_name)
        self.text = Text(style=context.current_style, justify="left")

    def on_text(self, context: MarkdownContext, text: str) -> None:
        self.text.append(text, context.current_style)

    def on_leave(self, context: MarkdownContext) -> None:
        context.leave_style()

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        yield self.text


class Paragraph(TextElement):
    style_name = "markdown.paragraph"

    @classmethod
    def create(cls, markdown: Markdown, node) -> None:
        return cls(justify=markdown.justify)

    def __init__(self, justify: str) -> None:
        self.justify = justify

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        self.text.justify = self.justify
        yield self.text


class Heading(TextElement):
    @classmethod
    def create(cls, markdown: Markdown, node: Any) -> Heading:
        heading = Heading(node.level)
        return heading

    def on_enter(self, context: MarkdownContext) -> None:
        self.text = Text(style=context.current_style)
        context.enter_style(self.style_name)

    def __init__(self, level: int) -> None:
        self.level = level
        self.style_name = f"markdown.h{level}"
        super().__init__()

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        text = self.text
        text.justify = "center"
        if self.level == 1:
            yield Panel(
                text, border=DOUBLE_BORDER, style="markdown.h1.border",
            )
        else:
            yield text


class CodeBlock(TextElement):
    style_name = "markdown.code_block"

    @classmethod
    def create(cls, markdown: Markdown, node: Any) -> ListElement:
        lexer_name, _, _ = node.info.partition(" ")
        return cls(lexer_name, markdown.code_theme)

    def __init__(self, lexer_name: str, theme: str) -> None:
        self.lexer_name = lexer_name
        self.theme = theme

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:

        code = str(self.text).rstrip()
        syntax = Syntax(code, self.lexer_name, theme=self.theme, line_numbers=False)
        yield syntax


class BlockQuote(TextElement):
    style_name = "markdown.block_quote"

    def __init__(self) -> None:
        self.elements: List[MarkdownElement] = []

    def on_child_close(self, context: MarkdownContext, child: MarkdownElement) -> bool:
        self.elements.append(child)
        return False

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        render_options = options.with_width(options.max_width - 4)
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
    new_line = False

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        style = console.get_style("markdown.hr")
        yield Segment(f'{"─" * options.max_width}\n', style)


class ListElement(MarkdownElement):
    @classmethod
    def create(cls, markdown: Markdown, node: Any) -> ListElement:
        list_data = node.list_data
        return cls(list_data["type"], list_data["start"])

    def __init__(self, list_type: str, list_start: Optional[int]) -> None:
        self.items: List[ListItem] = []
        self.list_type = list_type
        self.list_start = list_start

    def on_child_close(self, context: MarkdownContext, child: MarkdownElement) -> bool:
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
    style_name = "markdown.item"

    def __init__(self) -> None:
        self.elements: List[MarkdownElement] = []

    def on_child_close(self, context: MarkdownContext, child: MarkdownElement) -> bool:
        self.elements.append(child)
        return False

    def render_bullet(self, console: Console, options: ConsoleOptions) -> RenderResult:
        render_options = options.with_width(options.max_width - 3)
        lines = console.render_lines(self.elements, render_options, style=self.style)
        bullet_style = console.parse_style("markdown.item.bullet")

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
        render_options = options.with_width(options.max_width - number_width)
        lines = console.render_lines(self.elements, render_options, style=self.style)
        number_style = console.parse_style("markdown.item.number")

        new_line = Segment("\n")
        padding = Segment(" " * number_width, number_style)
        numeral = Segment(f"{number}".rjust(number_width - 1) + " ", number_style)
        for first, line in iter_first(lines):
            yield numeral if first else padding
            yield from line
            yield new_line


class MarkdownContext:
    """Manages the console render state."""

    def __init__(self, console: Console, options: ConsoleOptions) -> None:
        self.console = console
        self.options = options
        self.style_stack: StyleStack = StyleStack(console.current_style)
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

    def enter_style(self, style_name: str) -> Style:
        """Enter a style context."""
        style = self.console.get_style(style_name) or Style()
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
        self, markup: str, code_theme: str = "monokai", justify: str = "left"
    ) -> None:
        """Parses the markup."""
        self.markup = markup
        parser = Parser()
        self.parsed = parser.parse(markup)
        self.code_theme = code_theme
        self.justify = justify

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        """Render markdown to the console."""
        context = MarkdownContext(console, options)
        nodes = self.parsed.walker()
        inlines = self.inlines
        new_line = False
        for current, entering in nodes:
            # print(dir(current))
            # print(current, current.is_container(), entering, current.destination)
            # print(current.is_container())
            node_type = current.t
            if node_type == "text":
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
# This is a header which is very long and should be wrapped accross several lines, it should render within a cyan panel

## This is a header L2

### This is a header L3

#### This is a header L4

##### This is a header L5

###### This is a header L6

The main area where I think *Django's models* are `missing` out is the lack of type hinting (hardly surprising since **Django** pre-dates type hints). Adding type hints allows Mypy to detect bugs before you even run your code. It may only save you minutes each time, but multiply that by the number of code + run iterations you do each day, and it can save hours of development time. Multiply that by the lifetime of your project, and it could save weeks or months. A clear win.

```python
    @property
    def width(self) -> int:
        \"\"\"Get the width of the console.
        
        Returns:
            int: The width (in characters) of the console.
        \"\"\"
        width, _ = self.size
        return width
```

The main area where I think Django's models are missing out is the lack of type hinting (hardly surprising since Django pre-dates type hints). Adding type hints allows Mypy to detect bugs before you even run your code. It may only save you minutes each time, but multiply that by the number of code + run iterations you do each day, and it can save hours of development time. Multiply that by the lifetime of your project, and it could save weeks or months. A clear win.

---
# Another header
qqweo qlkwje lqkwej 

> The main area where I think Django's models are missing out is the lack of type hinting (hardly surprising since Django pre-dates type hints). Adding type hints allows Mypy to detect bugs before you even run your code. It may only save you minutes each time, but multiply that by the number of code + run iterations you do each day, and it can save hours of development time. Multiply that by the lifetime of your project, and it could save weeks or months. A clear win.


 * Hello, *World*!
   Another line
 * bar
 * baz

1. First *Item* **in bold!**
   Foo bar baz etc
   * Secondary list with lots of text that will wrap on to another line, Secondary list with lots of text that will wrap on to another line, Secondary list with lots of text that will wrap on to another line,
   * Foo 
   * Bar baz
2. Second Item
3. The main area where I think Django's models are missing out is the lack of type hinting (hardly surprising since Django pre-dates type hints). Adding type hints allows Mypy to detect bugs before you even run your code.

- sdfsdf
- wewerwer

This is a [link](https://www.willmcgugan.com)

"""

# markup = """\
# # Heading

# This is `code`!
# Hello, *World*!
# **Bold**

# """

if __name__ == "__main__":
    from .console import Console

    console = Console(width=79)
    # print(console.size)

    md = Markdown(markup)

    console.print(md)
    print(console)
    # print(console.render_spans())
