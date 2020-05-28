from typing import Union

from .console import Console, ConsoleOptions, RenderResult
from .jupyter import JupyterMixin
from .segment import Segment
from .style import Style
from .text import Text


class Rule(JupyterMixin):
    """A console renderable to draw a horizontal rule (line).
    
    Args:
        title (Union[str, Text], optional): Text to render in the rule. Defaults to "".
        character (str, optional): Character used to draw the line. Defaults to "─".
    """

    def __init__(
        self,
        title: Union[str, Text] = "",
        character: str = None,
        style: Union[str, Style] = "rule.line",
    ) -> None:
        if character and len(character) != 1:
            raise ValueError(
                "Rule requires character argument to be a string of length 1"
            )
        self.title = title
        self.character = character
        self.style = style

    def __repr__(self) -> str:
        return f"Rule({self.title!r}, {self.character!r})"

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        width = options.max_width

        character = "-" if console.legacy_windows else (self.character or "─")

        if not self.title:
            yield Text(character * width, self.style)
        else:
            if isinstance(self.title, Text):
                title_text = self.title
            else:
                title_text = console.render_str(self.title, style="rule.text")
            if len(title_text) > width - 4:
                title_text.set_length(width - 4)

            rule_text = Text()
            center = (width - len(title_text)) // 2
            rule_text.append(character * (center - 1) + " ", self.style)
            rule_text.append(title_text)
            rule_text.append(" " + character * (width - len(rule_text) - 1), self.style)
            yield rule_text


if __name__ == "__main__":  # pragma: no cover
    from rich.console import Console
    import sys

    try:
        text = sys.argv[1]
    except IndexError:
        text = "Hello, World"
    console = Console()
    console.print(Rule(text))
