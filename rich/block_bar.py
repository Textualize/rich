from typing import Optional, Union

from .color import Color
from .console import Console, ConsoleOptions, RenderResult
from .jupyter import JupyterMixin
from .measure import Measurement
from .segment import Segment
from .style import Style

# There are left-aligned characters for 1/8 to 7/8, but
# the right-aligned characters exist only for 1/8 and 4/8.
BEGIN_BLOCK_ELEMS = ["█", "█", "█", "▐", "▐", "▐", "▕", "▕"]
END_BLOCK_ELEMS = [" ", "▏", "▎", "▍", "▌", "▋", "▊", "▉"]
FULL_BLOCK = "█"


class BlockBar(JupyterMixin):
    """Renders a solid block bar.

    Args:
        size (float): Value for the end of the bar.
        begin (float): Begin point (between 0 and size, inclusive).
        end (float): End point (between 0 and size, inclusive).
        width (int, optional): Width of the bar, or ``None`` for maximum width. Defaults to None.
        color (Union[Color, str], optional): Color of the bar. Defaults to "default".
        bgcolor (Union[Color, str], optional): Color of bar background. Defaults to "default".
    """

    def __init__(
        self,
        size: float,
        begin: float,
        end: float,
        width: int = None,
        color: Union[Color, str] = "default",
        bgcolor: Union[Color, str] = "default",
    ):
        self.size = size
        self.begin = max(begin, 0)
        self.end = min(end, size)
        self.width = width
        self.style = Style(color=color, bgcolor=bgcolor)

    def __repr__(self) -> str:
        return f"<BlockBar {self.begin!r}..{self.end!r} of {self.size!r}>"

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:

        width = min(self.width or options.max_width, options.max_width)

        if self.begin >= self.end:
            yield Segment(" " * width, self.style)
            return

        prefix_complete_eights = int(width * 8 * self.begin / self.size)
        prefix_bar_count = prefix_complete_eights // 8
        prefix_eights_count = prefix_complete_eights % 8

        body_complete_eights = int(width * 8 * self.end / self.size)
        body_bar_count = body_complete_eights // 8
        body_eights_count = body_complete_eights % 8

        # When start and end fall into the same cell, we ideally should render
        # a symbol that's "center-aligned", but there is no good symbol in Unicode.
        # In this case, we fall back to right-aligned block symbol for simplicity.

        prefix = " " * prefix_bar_count
        if prefix_eights_count:
            prefix += BEGIN_BLOCK_ELEMS[prefix_eights_count]

        body = FULL_BLOCK * body_bar_count
        if body_eights_count:
            body += END_BLOCK_ELEMS[body_eights_count]

        suffix = " " * (width - len(body))

        yield Segment(prefix + body[len(prefix) :] + suffix, self.style)

    def __rich_measure__(self, console: Console, max_width: int) -> Measurement:
        return (
            Measurement(self.width, self.width)
            if self.width is not None
            else Measurement(4, max_width)
        )


if __name__ == "__main__":  # pragma: no cover
    console = Console()

    import time

    console.show_cursor(False)
    for n in range(0, 101):
        block_bar = BlockBar(size=100, begin=0, end=n, width=10)
        console.print(block_bar)
        console.file.write("\r")
        time.sleep(0.05)
    console.print()
    for n in range(0, 101):
        block_bar = BlockBar(size=100, begin=n, end=100, width=10)
        console.print(block_bar)
        console.file.write("\r")
        time.sleep(0.05)
    console.print()
    for n in range(0, 51):
        block_bar = BlockBar(size=100, begin=50 - n, end=50 + n, width=10)
        console.print(block_bar)
        console.file.write("\r")
        time.sleep(0.05)
    console.show_cursor(True)
    console.print()
