import typing
from typing import Optional

from .console import Console
from .measure import Measurement
from .style import StyleType
from .text import Text, TextType
from ._spinners import SPINNERS

if typing.TYPE_CHECKING:
    from .console import Console, ConsoleOptions, RenderResult


class Spinner:
    """Base class for a spinner."""

    def __init__(
        self, name: str, text: TextType = "", style: StyleType = None, speed=1.0
    ) -> None:
        try:
            spinner = SPINNERS[name]
        except KeyError:
            raise KeyError(f"no spinner called {name!r}")
        self.text = text
        self.frames = spinner["frames"][:]
        self.interval = spinner["interval"]
        self.start_time: Optional[float] = None
        self.style = style
        self.speed = speed
        self.time = 0.0

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":
        time = console.get_time()
        if self.start_time is None:
            self.start_time = time
        text = self.render(time - self.start_time)
        yield text

    def __rich_measure__(self, console: "Console", max_width: int) -> Measurement:
        text = self.render(0)
        return Measurement.get(console, text, max_width)

    def render(self, time: float) -> Text:
        frame_no = int((time * self.speed) / (self.interval / 1000.0)) % len(
            self.frames
        )
        frame = Text(self.frames[frame_no])
        if self.style is not None:
            frame.stylize(self.style)
        return Text.assemble(frame, " ", self.text) if self.text else frame


if __name__ == "__main__":  # pragma: no cover
    from .live import Live
    from time import sleep

    from .columns import Columns

    all_spinners = Columns(
        [
            Spinner(spinner_name, text=Text(repr(spinner_name), style="green"))
            for spinner_name in SPINNERS.keys()
        ]
    )

    with Live(all_spinners, refresh_per_second=20) as live:
        while True:
            sleep(0.1)
            live.refresh()
