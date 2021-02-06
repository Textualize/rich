from typing import Optional

from .console import Console, RenderableType
from .jupyter import JupyterMixin
from .live import Live
from .spinner import Spinner
from .style import StyleType
from .table import Table


class Status(JupyterMixin):
    """Displays a status indicator with a 'spinner' animation.

    Args:
        status (RenderableType): A status renderable (str or Text typically).
        console (Console, optional): Console instance to use, or None for global console. Defaults to None.
        spinner (str, optional): Name of spinner animation (see python -m rich.spinner). Defaults to "dots".
        spinner_style (StyleType, optional): Style of spinner. Defaults to "status.spinner".
        speed (float, optional): Speed factor for spinner animation. Defaults to 1.0.
        refresh_per_second (float, optional): Number of refreshes per second. Defaults to 12.5.
    """

    def __init__(
        self,
        status: RenderableType,
        *,
        console: Console = None,
        spinner: str = "dots",
        spinner_style: StyleType = "status.spinner",
        speed: float = 1.0,
        refresh_per_second: float = 12.5,
    ):
        self.status = status
        self.spinner = spinner
        self.spinner_style = spinner_style
        self.speed = speed
        self._spinner = Spinner(spinner, style=spinner_style, speed=speed)
        self._live = Live(
            self.renderable,
            console=console,
            refresh_per_second=refresh_per_second,
            transient=True,
        )
        self.update(
            status=status, spinner=spinner, spinner_style=spinner_style, speed=speed
        )

    @property
    def renderable(self) -> Table:
        """Get the renderable for the status (a table with spinner and status)."""
        table = Table.grid(padding=1)
        table.add_row(self._spinner, self.status)
        return table

    @property
    def console(self) -> "Console":
        """Get the Console used by the Status objects."""
        return self._live.console

    def update(
        self,
        status: Optional[RenderableType] = None,
        *,
        spinner: Optional[str] = None,
        spinner_style: Optional[StyleType] = None,
        speed: Optional[float] = None,
    ):
        """Update status.

        Args:
            status (Optional[RenderableType], optional): New status renderable or None for no change. Defaults to None.
            spinner (Optional[str], optional): New spinner or None for no change. Defaults to None.
            spinner_style (Optional[StyleType], optional): New spinner style or None for no change. Defaults to None.
            speed (Optional[float], optional): Speed factor for spinner animation or None for no change. Defaults to None.
        """
        if status is not None:
            self.status = status
        if spinner is not None:
            self.spinner = spinner
        if spinner_style is not None:
            self.spinner_style = spinner_style
        if speed is not None:
            self.speed = speed
        self._spinner = Spinner(
            self.spinner, style=self.spinner_style, speed=self.speed
        )
        self._live.update(self.renderable, refresh=True)

    def start(self) -> None:
        """Start the status animation."""
        self._live.start()

    def stop(self) -> None:
        """Stop the spinner animation."""
        self._live.stop()

    def __rich__(self) -> RenderableType:
        return self.renderable

    def __enter__(self) -> "Status":
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.stop()


if __name__ == "__main__":  # pragma: no cover

    from time import sleep

    from .console import Console

    console = Console()
    with console.status("[magenta]Covid detector booting up") as status:
        sleep(3)
        console.log("Importing advanced AI")
        sleep(3)
        console.log("Advanced Covid AI Ready")
        sleep(3)
        status.update(status="[bold blue] Scanning for Covid", spinner="earth")
        sleep(3)
        console.log("Found 10,000,000,000 copies of Covid32.exe")
        sleep(3)
        status.update(
            status="[bold red]Moving Covid32.exe to Trash",
            spinner="bouncingBall",
            spinner_style="yellow",
        )
        sleep(5)
    console.print("[bold green]Covid deleted successfully")
