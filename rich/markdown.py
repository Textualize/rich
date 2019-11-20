from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar, Dict, Iterable, List, Optional, Union

from commonmark.blocks import Parser

from .console import (
    Console,
    ConsoleOptions,
    ConsoleRenderable,
    RenderResult,
    StyledText,
)
from .panel import Panel
from .style import Style, StyleStack
from .text import Lines, Text
from ._stack import Stack


class MarkdownElement:

    new_line: ClassVar[bool] = True

    @classmethod
    def create(cls, node: Any) -> MarkdownElement:
        return cls()

    def on_enter(self, context: MarkdownContext):
        pass

    def on_text(self, context: MarkdownContext, text: str) -> None:
        pass

    def on_leave(self, context: MarkdownContext) -> RenderResult:
        return
        yield

    def on_child_close(self, context: MarkdownContext, child: MarkdownElement) -> bool:
        return True


class UnknownElement(MarkdownElement):
    pass


class TextElement(MarkdownElement):

    style_name = "none"

    def on_enter(self, context: MarkdownContext) -> None:
        context.enter_style(self.style_name)
        self.text = Text(style=context.current_style)

    def on_text(self, context: MarkdownContext, text: str) -> None:
        self.text.append(text, context.current_style)

    def on_leave(self, context: MarkdownContext) -> RenderResult:
        context.leave_style()
        yield self.text


class Paragraph(TextElement):
    style_name = "markdown.paragraph"

    def on_leave(self, context: MarkdownContext) -> Iterable[Lines]:
        context.leave_style()
        lines = self.text.wrap(context.options.max_width)
        yield from lines


class Heading(TextElement):
    @classmethod
    def create(cls, node: Any) -> Heading:
        heading = Heading(node.level)
        return heading

    def on_enter(self, context: MarkdownContext) -> None:
        self.text = Text(style=context.current_style, end="")
        context.enter_style(self.style_name)

    def __init__(self, level: int) -> None:
        self.level = level
        self.style_name = f"markdown.h{level}"
        super().__init__()

    def on_leave(self, context: MarkdownContext) -> Iterable[Lines]:
        context.leave_style()
        self.text.justify = "center"
        if self.level == 1:
            yield Panel(self.text)
        else:
            yield self.text
            yield StyledText("\n")
        # lines = self.text.wrap(context.options.max_width, justify="center")
        # yield lines


class CodeBlock(TextElement):
    style_name = "markdown.code_block"

    def on_leave(self, context: MarkdownContext) -> Iterable[Lines]:
        context.leave_style()
        lines = self.text.wrap(context.options.max_width, justify="left")
        yield lines


class BlockQuote(TextElement):
    style_name = "markdown.block_quote"

    def __init__(self) -> None:
        self.elements = []

    def on_enter(self, context: MarkdownContext) -> None:
        context.enter_style(self.style_name)

    def on_child_close(self, context: MarkdownContext, child: MarkdownElement) -> bool:
        self.elements.append(child)
        return False

    def on_leave(self, context: MarkdownContext) -> Iterable[Lines]:
        context.leave_style()
        for element in self.elements:
            yield from element.on_leave(context)


class HorizontalRule(MarkdownElement):
    new_line = False

    def on_leave(self, context: MarkdownContext) -> Iterable[StyledText]:
        style = context.console.get_style("markdown.hr")
        yield StyledText("─" * context.options.max_width, style)


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

    def on_text(self, text: str) -> None:
        """Called when the parser visits text."""
        self.stack.top.on_text(self, text)

    def enter_style(self, style_name: str) -> None:
        """Enter a style context."""
        style = self.console.get_style(style_name) or self.console.get_style("none")
        self.style_stack.push(style)

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
    }
    inlines = {"emph", "strong", "code"}

    def __init__(self, markup: str) -> None:
        """Parses the markup."""
        self.markup = markup
        parser = Parser()
        self.parsed = parser.parse(markup)

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        """Render markdown to the console."""
        context = MarkdownContext(console, options)
        nodes = self.parsed.walker()
        inlines = self.inlines
        for current, entering in nodes:
            # print(dir(current))
            print(current, entering)
            print(current.is_container())
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
            else:
                element_class = self.elements.get(node_type) or UnknownElement
                if current.is_container():
                    if entering:
                        element = element_class.create(current)
                        context.stack.push(element)
                        element.on_enter(context)
                    else:
                        element = context.stack.pop()

                        if context.stack:
                            if context.stack.top.on_child_close(context, element):
                                if element.new_line:
                                    yield StyledText("\n")
                                yield from element.on_leave(context)
                        else:
                            yield from element.on_leave(context)
                else:
                    element = element_class.create(current)
                    context.stack.push(element)
                    element.on_enter(context)
                    if current.literal:
                        element.on_text(context, current.literal.rstrip())
                    context.stack.pop()
                    if context.stack and element.new_line:
                        yield StyledText("\n")
                    yield from element.on_leave(context)


# class Markdown:
#     """Render markdown to the console."""

#     def __init__(self, markup):
#         self.markup = markup

#     def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:

#         parser = Parser()

#         nodes = parser.parse(self.markup).walker()

#         rendered: List[StyledText] = []
#         style_stack: Stack[Style] = Stack()
#         style_stack.push(Style())
#         stack = Stack()

#         text = Text()

#         null_style = Style()

#         def push_style(name: str) -> Style:
#             """Enter in to a new style context."""
#             style = console.get_style(name) or null_style
#             style = style_stack.top.apply(style)
#             style_stack.push(style)
#             return style

#         def pop_style() -> Style:
#             """Leave a style context."""
#             return style_stack.pop()

#         deferred_space = False

#         def new_content(
#             *objects: Union[ConsoleRenderable, StyledText, str], line=True
#         ) -> RenderResult:
#             nonlocal deferred_space
#             if deferred_space and line:
#                 yield StyledText("\n")
#             for render_object in objects:
#                 if isinstance(render_object, str):
#                     yield StyledText(render_object)
#                 elif isinstance(render_object, StyledText):
#                     yield render_object
#                 else:
#                     yield render_object
#             deferred_space = True

#         element_stack: Stack[MarkdownElement] = Stack()
#         for current, entering in nodes:
#             node_type = current.t
#             if node_type == "text":
#                 element_stack.top.on_text(current.literal)
#             elif node_type == "emph":
#                 if entering:
#                     push_s

#         # for current, entering in nodes:
#         #     print(current, entering)
#         #     node_type = current.t
#         #     if node_type == "text":
#         #         style = push_style("markdown.text")
#         #         text.append(current.literal, style)
#         #         pop_style()
#         #     elif node_type == "paragraph":
#         #         if entering:
#         #             push_style("markdown.paragraph")
#         #         else:
#         #             pop_style()
#         #             yield from new_content(text.wrap(options.max_width))
#         #             text = Text()
#         #     elif node_type == "heading":
#         #         if entering:
#         #             push_style(f"markdown.h{current.level}")
#         #         else:
#         #             pop_style()
#         #             yield from new_content(
#         #                 text.wrap(options.max_width, justify="center")
#         #             )
#         #             text = Text()
#         #     elif node_type == "code_block":
#         #         style = push_style("markdown.code_block")
#         #         code_text = Text(current.literal.rstrip(), style=style)
#         #         wrapped_text = code_text.wrap(options.max_width, justify="left")
#         #         yield from new_content(wrapped_text)
#         #         pop_style()
#         #     elif node_type == "code":
#         #         style = push_style("markdown.code")
#         #         text.append(current.literal, style)
#         #         pop_style()
#         #     elif node_type == "softbreak":
#         #         text.append("\n")
#         #     elif node_type == "thematic_break":
#         #         style = push_style("markdown.hr")
#         #         yield from new_content(StyledText(f"{'—' * options.max_width}", style))
#         #         pop_style()
#         #     elif node_type == "block_quote":
#         #         if entering:
#         #             push_style("markdown.block_quote")
#         #         else:
#         #             style = pop_style()
#         #     elif node_type == "list":
#         #         if entering:
#         #             push_style("markdown.list")
#         #         else:
#         #             pop_style()
#         #     elif node_type == "item":
#         #         if entering:
#         #             push_style("markdown.item")
#         #         else:
#         #             pop_style()

#         yield from rendered


markup = """
# This is a header

## This is a header L2

### This is a header L3

#### This is a header L4

##### This is a header L5

###### This is a header L6

The main area where I think *Django's models* are `missing` out is the lack of type hinting (hardly surprising since **Django** pre-dates type hints). Adding type hints allows Mypy to detect bugs before you even run your code. It may only save you minutes each time, but multiply that by the number of code + run iterations you do each day, and it can save hours of development time. Multiply that by the lifetime of your project, and it could save weeks or months. A clear win.

```
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
> This is a *block* quote
> With another line

 * foo
 * bar
 * baz
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
    print(console.size)
    md = Markdown(markup)

    console.print(md)
    # print(console.render_spans())
