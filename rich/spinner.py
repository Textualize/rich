from typing import cast, List, Optional, TYPE_CHECKING

from ._spinners import SPINNERS
from .console import Console
from .measure import Measurement
from .style import StyleType
from .text import Text, TextType

if TYPE_CHECKING:
    from .console import Console, ConsoleOptions, RenderResult


class Spinner:
    def __init__(
        self, name: str, text: TextType = "", *, style: StyleType = None, speed=1.0
    ) -> None:
        """A spinner animation.

        Args:
            name (str): Name of spinner (run python -m rich.spinner).
            text (TextType, optional): Text to display at the right of the spinner. Defaults to "".
            style (StyleType, optional): Style for sinner amimation. Defaults to None.
            speed (float, optional): Speed factor for animation. Defaults to 1.0.

        Raises:
            KeyError: If name isn't one of the supported spinner animations.
        """
        try:
            spinner = SPINNERS[name]
        except KeyError:
            raise KeyError(f"no spinner called {name!r}")
        self.text = text
        self.frames = cast(List[str], spinner["frames"])[:]
        self.interval = cast(float, spinner["interval"])
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

    def __rich_measure__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> Measurement:
        text = self.render(0)
        return Measurement.get(console, options, text)

    def render(self, time: float) -> Text:
        """Render the spinner for a given time.

        Args:
            time (float): Time in seconds.

        Returns:
            Text: A Text instance containing animation frame.
        """
        frame_no = int((time * self.speed) / (self.interval / 1000.0))
        frame = Text(self.frames[frame_no % len(self.frames)], style=self.style or "")
        return Text.assemble(frame, " ", self.text) if self.text else frame


if __name__ == "__main__":  # pragma: no cover
    from time import sleep

    from .columns import Columns
    from .panel import Panel
    from .live import Live

    all_spinners = Columns(
        [
            Spinner(spinner_name, text=Text(repr(spinner_name), style="green"))
            for spinner_name in sorted(SPINNERS.keys())
        ],
        column_first=True,
        expand=True,
    )

    with Live(
        Panel(all_spinners, title="Spinners", border_style="blue"),
        refresh_per_second=20,
    ) as live:
        while True:
            sleep(0.1)
