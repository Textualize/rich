from .console import Console, ConsoleOptions, RenderResult
from .text import Text


class Rule:
    def __init__(self, title: str = "", character: str = "─") -> None:
        self.title = title
        self.character = character

    def __repr__(self) -> str:
        return f"Rule({self.title!r}, {self.character!r})"

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        width = options.max_width

        if not self.title:
            yield Text(self.character * width, "rule.line")
        else:
            title_text = Text.from_markup(self.title, "rule.text")
            if len(title_text) > width - 4:
                title_text.set_length(width - 4)

            rule_text = Text()
            center = (width - len(title_text)) // 2
            rule_text.append(self.character * (center - 1) + " ", "rule.line")
            rule_text.append(title_text)
            rule_text.append(
                " " + self.character * (width - len(rule_text) - 1), "rule.line"
            )
            yield rule_text
