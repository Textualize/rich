from typing import TYPE_CHECKING

from .jupyter import JupyterMixin
from .segment import Segment

if TYPE_CHECKING:
    from .console import Console, ConsoleOptions, RenderResult
    from .style import StyleType


class Crosshairs(JupyterMixin):
    def __init__(self, x: int, y: int, style: "StyleType" = ""):
        self.x = x
        self.y = y
        self.style = style

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":

        width, height = console.size
        console_style = console.get_style(self.style)

        # First, we build the line that only contains the vertical bar.
        vertical_bar_line = " " * self.x + "│" + " " * (width - self.x - 1)
        vertical_bar_segment = Segment(vertical_bar_line, style=console_style)

        # Yield all segments above the horizontal cross line.
        for _ in range(self.y):
            yield vertical_bar_segment
            yield Segment.line()

        # Then, we build the horizontal line by finding what cross centre we need.
        placement = (  # Is the cross centre flush to...
            self.x == 0,  # the left edge?
            self.x == width - 1,  # the right edge?
            self.y == 0,  # the top edge?
            self.y == height - 1,  # the bottom edge?
        )
        cross_centre_mapping = {
            (False, False, False, False): "┼",  # centre-centre
            (False, False, False, True): "┴",  # centre-bottom
            (False, False, True, False): "┬",  # centre-top
            (False, True, False, False): "┤",  # right-centre
            (False, True, False, True): "┘",  # right-bottom
            (False, True, True, False): "┐",  # right-top
            (True, False, False, False): "├",  # left-centre
            (True, False, False, True): "└",  # left-bottom
            (True, False, True, False): "┌",  # left-top
        }
        assert placement in cross_centre_mapping
        cross_centre = cross_centre_mapping[placement]

        horizontal_bar_line = "─" * self.x + cross_centre + "─" * (width - 1 - self.x)
        yield Segment(horizontal_bar_line, style=console_style)
        yield Segment.line()

        # Yield all segments below the horizontal cross line.
        for _ in range(height - 1 - self.y):
            yield vertical_bar_segment
            yield Segment.line()


if __name__ == "__main__":
    from rich.console import Console

    console = Console(width=10, height=5)
    console.print(Crosshairs(1, 1, "black on white"))
