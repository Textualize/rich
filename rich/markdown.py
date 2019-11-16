from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

from commonmark.blocks import Parser

from .console import Console, ConsoleOptions, RenderResult, StyledText
from .style import Style
from .text import Text
from ._stack import Stack


class Heading(Text):
    def __init__(self, level: int) -> None:
        super().__init__()
        self.level = level


class Markdown:
    """Render markdown to the console."""

    def __init__(self, markup):
        self.markup = markup

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:

        parser = Parser()

        nodes = parser.parse(self.markup).walker()

        rendered: List[StyledText] = []
        style_stack: Stack[Style] = Stack()
        stack: Stack[Text] = Stack()
        style_stack.push(Style())

        null_style = Style()

        def push_style(name: str) -> Style:

            style = console.get_style(name) or null_style
            style = style_stack.top.apply(style)
            style_stack.push(style)
            return style

        def pop_style() -> Style:
            return style_stack.pop()

        paragraph_count = 0
        for current, entering in nodes:

            node_type = current.t
            if node_type == "text":
                style = push_style("markdown.text")
                stack.top.append(current.literal, style)
                pop_style()
            elif node_type == "paragraph":
                if entering:
                    if paragraph_count:
                        yield StyledText("\n")
                    paragraph_count += 1
                    push_style("markdown.paragraph")
                    stack.push(Text())
                else:
                    pop_style()
                    text = stack.pop()
                    yield text.wrap(options.max_width)
                    # yield StyledText("\n")

                    # yield StyledText("\n")
            elif node_type == "heading":
                if entering:
                    push_style(f"markdown.h{current.level}")
                    stack.push(Heading(current.level))
                else:
                    pop_style()
                    text = stack.pop()
                    yield text.wrap(options.max_width, justify="center")
                    yield StyledText("\n")
            elif node_type == "code_block":
                style = push_style("markdown.code_block")
                text = Text(current.literal.rstrip(), style=style)
                wrapped_text = text.wrap(options.max_width, justify="left")
                yield StyledText("\n")
                yield wrapped_text
                pop_style()

            elif node_type == "code":
                style = push_style("markdown.code")
                stack.top.append(current.literal, style)
                pop_style()
            elif node_type == "softbreak":
                stack.top.append("\n")
            elif node_type == "thematic_break":
                style = push_style("markdown.hr")
                yield StyledText(f"\n{'—' * options.max_width}\n", style)
                paragraph_count = 0
                pop_style()
            else:
                if entering:
                    push_style(f"markdown.{node_type}")
                else:
                    pop_style()

        yield from rendered


markup = """
# This is a header

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
"""

if __name__ == "__main__":
    from .console import Console

    console = Console(width=79)
    print(console.size)
    md = Markdown(markup)

    console.print(md)
    # print(console.render_spans())
