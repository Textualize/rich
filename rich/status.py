from typing import Optional

from .console import Console
from .progress import Progress, SpinnerColumn, RenderableColumn
from .spinner import Spinner
from .style import StyleType
from .text import TextType


class Status:
    def __init__(
        self,
        status: str,
        spinner: str = "dots",
        spinner_style: StyleType = "progress.spinner",
        speed: float = 1.0,
    ):
        self.status = status
        self.spinner = spinner
        self.spinner_style = spinner_style
        self.speed = speed
        self._spinner_column = SpinnerColumn(spinner, style=spinner_style)
        self._renderable_column = RenderableColumn(self.status)
        self._progress = Progress(
            self._spinner_column,
            self._renderable_column,
            refresh_per_second=12.5,
            transient=True,
        )
        self._task_id = self._progress.add_task(status)
        self.update(
            status=status, spinner=spinner, spinner_style=spinner_style, speed=speed
        )

    @property
    def console(self) -> "Console":
        return self._progress.console

    def update(
        self,
        *,
        status: Optional[str] = None,
        spinner: Optional[str] = None,
        spinner_style: Optional[StyleType] = None,
        speed: Optional[float] = None,
    ):
        if status is not None:
            self._renderable_column.renderable = status
        if spinner is not None:
            self.spinner = spinner
        if spinner_style is not None:
            self.spinner_style = spinner_style
        if speed is not None:
            self.speed = speed
        self._spinner_column.spinner = Spinner(
            self.spinner,
            style=self.spinner_style or "progress.spinner",
            speed=self.speed,
        )
        self._progress.refresh()

    def start(self) -> None:
        self._progress.start()

    def stop(self) -> None:
        self._progress.stop()

    def __enter__(self) -> "Status":
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.stop()


if __name__ == "__main__":  # pragma: no cover

    from time import sleep

    with Status("[green]Working") as status:

        def example_text():
            status.console.print(
                "[dim]Don't pay this any attention, look at the spinner"
            )
            sleep(1)
            status.console.print([1, 2, 3])
            sleep(1)
            status.console.print({"foo": "bar"})
            sleep(1)

        example_text()
        status.update(
            status="[cyan]Reticulating [i]splines[/i]",
            spinner="dots2",
            spinner_style="yellow",
        )
        example_text()
        status.update(status="[blink red]Scanning...", spinner="earth")
        example_text()
        status.update(
            status="[bold red]Beautiful is better than ugly.\n[bold blue]Explicit is better than implicit.\n[bold yellow]Simple is better than complex.",
            spinner="arrow2",
        )
        example_text()
        status.update(
            spinner="dots9", spinner_style="magenta", status="That's all folks!"
        )
        example_text()
