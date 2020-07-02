from typing import TYPE_CHECKING

from .measure import Measurement
from .segment import Segment
from .style import StyleType

if TYPE_CHECKING:
    from .console import Console, ConsoleOptions, RenderResult, RenderableType


class Styled:
    """Apply a style to a renderable.

    Args:
        renderable (RenderableType): Any renderable.
        style (StyleType): A style to apply accross the entire renderable.
    """

    def __init__(self, renderable: "RenderableType", style: "StyleType") -> None:
        self.renderable = renderable
        self.style = style

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":
        style = console.get_style(self.style)
        rendered_segments = console.render(self.renderable, options)
        segments = Segment.apply_style(rendered_segments, style)
        return segments

    def __rich_measure__(self, console: "Console", max_width: int) -> Measurement:
        return Measurement.get(console, self.renderable, max_width)


if __name__ == "__main__":  # pragma: no cover
    from rich import print
    from rich.panel import Panel

    panel = Styled(Panel("hello"), "on blue")
    print(panel)
