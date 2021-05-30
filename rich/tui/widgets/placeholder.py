from ..widget import Widget

from rich.repr import RichReprResult


class Placeholder(Widget):
    def __rich_repr__(self) -> RichReprResult:
        yield "name", self.name
        yield "mouse_over", self.mouse_over