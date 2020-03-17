from typing import Union

from .console import Console, ConsoleOptions, RenderResult
from .measure import Measurement
from .segment import Segment
from .style import StyleType


class Bar:
    """Renders a (progress) bar.
        
    Args:
        total (float, optional): Number of steps in the bar. Defaults to 100.
        completed (float, optional): Number of steps completed. Defaults to 0.
        width (int, optional): Width of the bar, or ``None`` for maximum width. Defaults to None.
        style (StyleType, optional): Style for the bar background. Defaults to "bar.back".
        complete_style (StyleType, optional): Style for the completed bar. Defaults to "bar.complete".
        finished_style (StyleType, optional): Style for a finished bar. Defaults to "bar.done".
    """

    def __init__(
        self,
        total: float = 100,
        completed: float = 0,
        width: int = None,
        style: StyleType = "bar.back",
        complete_style: StyleType = "bar.complete",
        finished_style: StyleType = "bar.finished",
    ):
        self.total = total
        self.completed = completed
        self.width = width
        self.style = style
        self.complete_style = complete_style
        self.finished_style = finished_style

    def __repr__(self) -> str:
        return f"<Bar {self.completed!r} of {self.total!r}>"

    @property
    def percentage_completed(self) -> float:
        """Calculate percentage complete."""
        completed = (self.completed / self.total) * 100.0
        completed = min(100, max(0.0, completed))
        return completed

    def update_progress(self, completed: float, total: float = None) -> None:
        """Update progress with new values.
        
        Args:
            completed (float): Number of steps completed.
            total (float, optional): Total number of steps, or ``None`` to not change. Defaults to None.
        """
        self.completed = completed
        self.total = total if total is not None else self.total

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        completed = min(self.total, max(0, self.completed))
        width = min(self.width or options.max_width, options.max_width)
        bar = "━"
        half_bar_right = "╸"
        half_bar_left = "╺"
        complete_halves = int(width * 2 * completed / self.total)
        bar_count = complete_halves // 2
        half_bar_count = complete_halves % 2
        style = console.get_style(self.style)
        complete_style = console.get_style(
            self.complete_style if self.completed < self.total else self.finished_style
        )
        if bar_count:
            yield Segment(bar * bar_count, complete_style)
        if half_bar_count:
            yield Segment(half_bar_right * half_bar_count, complete_style)

        remaining_bars = width - bar_count - half_bar_count
        if remaining_bars:
            if not half_bar_count and bar_count:
                yield Segment(half_bar_left, style)
                remaining_bars -= 1
            if remaining_bars:
                yield Segment(bar * remaining_bars, style)

    def __measure__(self, console: Console, max_width: int) -> Measurement:
        if self.width is not None:
            return Measurement(self.width, self.width)
        return Measurement(4, max_width)


if __name__ == "__main__":
    console = Console()
    bar = Bar(width=50, total=100)

    import time

    console.show_cursor(False)
    for n in range(0, 101, 1):
        bar.update_progress(n)
        console.print(bar)
        console.file.write("\r")
        time.sleep(0.05)
    console.show_cursor(True)
    console.print()
