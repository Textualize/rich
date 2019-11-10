from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

from commonmark.blocks import Parser

from .console import Console, ConsoleOptions, StyledText
from .style import Style


@dataclass
class MarkdownHeading:
    """A Markdown document heading."""

    text: str
    level: int
    width: int

    def __console__(self) -> str:
        pass


class Markdown:
    """Render markdown to the console."""

    def __init__(self, markup):
        self.markup = markup

    def __console_render__(
        self, console: Console, options: ConsoleOptions
    ) -> Iterable[StyledText]:

        width = options.max_width
        parser = Parser()

        nodes = parser.parse(self.markup).walker()

        rendered: List[StyledText] = []
        append = rendered.append
        stack = [Style()]

        style: Optional[Style]
        for current, entering in nodes:
            node_type = current.t
            if node_type == "text":
                style = stack[-1].apply(console.get_style("markdown.text"))
                append(StyledText(current.literal, style))
            elif node_type == "paragraph":
                if not entering:
                    append(StyledText("\n\n", stack[-1]))
            else:
                if entering:
                    style = console.get_style(f"markdown.{node_type}")
                    if style is not None:
                        stack.append(stack[-1].apply(style))
                    else:
                        stack.append(stack[-1])
                    if current.literal:
                        append(StyledText(current.literal, stack[-1]))
                else:
                    stack.pop()

        print(rendered)
        return rendered


markup = """*hello*, **world**!

# Hi

```python
code
```

"""

if __name__ == "__main__":
    from .console import Console

    console = Console()
    md = Markdown(markup)

    console.print(md)
    # print(console.render_spans())
