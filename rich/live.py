import sys
from threading import Event, RLock, Thread
from typing import IO, Any, List, Optional

from .__init__ import get_console
from .console import Console, ConsoleRenderable, RenderableType, RenderHook
from .control import Control
from .jupyter import JupyterMixin
from .live_render import LiveRender
from .progress import _FileProxy
from .segment import Segment


class _RefreshThread(Thread):
    """A thread that calls refresh() at regular intervals."""

    def __init__(self, live: "Live", refresh_per_second: float) -> None:
        self.live = live
        self.refresh_per_second = refresh_per_second
        self.done = Event()
        super().__init__()

    def stop(self) -> None:
        self.done.set()

    def run(self) -> None:
        while not self.done.wait(1 / self.refresh_per_second):
            self.live.refresh()


class Live(JupyterMixin, RenderHook):
    def __init__(
        self,
        renderable: RenderableType = "",
        *,
        console: Console = None,
        auto_refresh: bool = True,
        refresh_per_second: float = 1,
        transient: bool = False,
        redirect_stdout: bool = True,
        redirect_stderr: bool = True,
        hide_overflow: bool = True,
    ) -> None:
        """Renders an auto-updating live display of any given renderable.

        Args:
            renderable (RenderableType, optional): [The renderable to live display. Defaults to displaying nothing.
            console (Console, optional): Optional Console instance. Default will an internal Console instance writing to stdout.
            auto_refresh (bool, optional): Enable auto refresh. If disabled, you will need to call `refresh()` or `update()` with refresh flag. Defaults to True
            refresh_per_second (float, optional): Number of times per second to refresh the live display. Defaults to 1.
            transient (bool, optional): Clear the renderable on exit. Defaults to False.
            redirect_stdout (bool, optional): Enable redirection of stdout, so ``print`` may be used. Defaults to True.
            redirect_stderr (bool, optional): Enable redirection of stderr. Defaults to True.
            hide_overflow (bool, optional): Checks that the renderable isn't too large for terminal and auto-hides. Defaults to True.
        """
        assert refresh_per_second > 0, "refresh_per_second must be > 0"
        self.console = console if console is not None else get_console()
        self._live_render = LiveRender(renderable)

        self._redirect_stdout = redirect_stdout
        self._redirect_stderr = redirect_stderr
        self._restore_stdout: Optional[IO[str]] = None
        self._restore_stderr: Optional[IO[str]] = None

        self._lock = RLock()
        self.ipy_widget: Optional[Any] = None
        self.auto_refresh = auto_refresh
        self._started: bool = False
        self.transient = transient

        self._refresh_thread: Optional[_RefreshThread] = None
        self.refresh_per_second = refresh_per_second

        self.hide_overflow = hide_overflow
        self._is_overflowing = False
        self._hide_render = LiveRender("Terminal too small\n")

    def start(self) -> None:
        """Start live rendering display."""
        with self._lock:
            if self._started:
                return

            self.console.show_cursor(False)
            self._enable_redirect_io()
            self.console.push_render_hook(self)
            self._started = True

            if self.auto_refresh:
                self._refresh_thread = _RefreshThread(self, self.refresh_per_second)
                self._refresh_thread.start()

    def stop(self) -> None:
        """Stop live rendering display."""
        with self._lock:
            if not self._started:
                return
            self._started = False
            try:
                if self.auto_refresh and self._refresh_thread is not None:
                    self._refresh_thread.stop()
                self.refresh()
                if self.console.is_terminal:
                    self.console.line()
            finally:
                self._disable_redirect_io()
                self.console.pop_render_hook()
                self.console.show_cursor(True)

            if self.transient:
                self.console.control(self._live_render.restore_cursor())
            if self.ipy_widget is not None and self.transient:  # pragma: no cover
                self.ipy_widget.clear_output()
                self.ipy_widget.close()

    def __enter__(self) -> "Live":
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.stop()

    def _enable_redirect_io(self):
        """Enable redirecting of stdout / stderr."""
        if self.console.is_terminal:
            if self._redirect_stdout:
                self._restore_stdout = sys.stdout
                sys.stdout = _FileProxy(self.console, sys.stdout)
            if self._redirect_stderr:
                self._restore_stderr = sys.stderr
                sys.stdout = _FileProxy(self.console, sys.stdout)

    @property
    def item(self) -> RenderableType:
        """Get the renderable that is being displayed

        Returns:
            RenderableType: Displayed renderable.
        """
        with self._lock:
            return self._live_render.renderable

    def update(self, renderable: RenderableType, *, refresh: bool = False) -> None:
        """Update the renderable that is being displayed

        Args:
            renderable (RenderableType): New renderable to use.
            refresh (bool, optional): Refresh the display. Defaults to False.
        """
        with self._lock:
            self._live_render.set_renderable(renderable)
            if refresh:
                self.refresh()

    def refresh(self) -> None:
        """Update the display of the Live Render."""
        if self.console.is_jupyter:  # pragma: no cover
            try:
                from IPython.display import display
                from ipywidgets import Output
            except ImportError:
                import warnings

                warnings.warn('install "ipywidgets" for Jupyter support')
            else:
                with self._lock:
                    if self.ipy_widget is None:
                        self.ipy_widget = Output()
                        display(self.ipy_widget)

                    with self.ipy_widget:
                        self.ipy_widget.clear_output(wait=True)
                        self.console.print(self._live_render.renderable)
        elif self.console.is_terminal and not self.console.is_dumb_terminal:
            with self._lock, self.console:
                self.console.print(Control(""))

    def _disable_redirect_io(self):
        """Disable redirecting of stdout / stderr."""
        if self._restore_stdout:
            sys.stdout = self._restore_stdout
            self._restore_stdout = None
        if self._restore_stderr:
            sys.stderr = self._restore_stderr
            self._restore_stderr = None

    def process_renderables(
        self, renderables: List[ConsoleRenderable]
    ) -> List[ConsoleRenderable]:
        """Process renderables to restore cursor and display progress."""
        if self.console.is_terminal:
            # lock needs acquiring as user can modify live_render renerable at any time unlike in Progress.
            with self._lock:
                # check that renderable doesn't overflow terminal height or it will
                if (
                    self.hide_overflow
                    and self._started  # on non-transient allow the final live render to be displayed
                ):
                    # determine height of renderable
                    lines = self.console.render_lines(
                        self._live_render.renderable, pad=False
                    )
                    renderable_height = Segment.get_shape(lines)[1]
                    if renderable_height >= self.console.size.height:
                        # continued overflow re-render terminal too small
                        if self._is_overflowing:
                            return [
                                self._hide_render.position_cursor(),
                                *renderables,
                                self._hide_render,
                            ]
                        else:
                            # on first overflow clear the live-render and display terminal too small message
                            self._is_overflowing = True
                            return [
                                self._live_render.position_cursor(),
                                *renderables,
                                self._hide_render,
                            ]
                self._is_overflowing = False
                return [
                    self._live_render.position_cursor(),
                    *renderables,
                    self._live_render,
                ]
        return renderables


if __name__ == "__main__":
    import random
    import time
    from typing import Dict, List, Tuple

    from .console import Console, RenderGroup
    from .live import Live
    from .panel import Panel
    from .table import Table
    from .text import Text

    console = Console()

    def table_example() -> None:
        Data = List[List[int]]

        def generate_table(data: Data) -> Table:
            table = Table()
            for data_row in data:
                table.add_row(*[hex(data_cell) for data_cell in data_row])

            return table

        def generate_data() -> Data:
            return [
                [random.randint(0, 20) for _ in range(random.randint(0, 8))]
                for _ in range(random.randint(12, 20))
            ]

        with Live(console=console, refresh_per_second=1, transient=True) as live_table:
            for _ in range(20):
                data = generate_data()
                time.sleep(0.5)
                console.print("hello")
                live_table.update(generate_table(data))

    def panel_example() -> None:

        with Live(auto_refresh=False) as live_panel:
            for index in range(20):
                panel = Panel(f"Hello, [red]World! {index}\n" * index, title="Welcome")
                live_panel.update(panel, refresh=True)
                time.sleep(0.2)

    def table_example2() -> None:
        exchanges = [
            "SGD",
            "MYR",
            "EUR",
            "USD",
            "AUD",
            "JPY",
            "CNH",
            "HKD",
            "CAD",
            "INR",
            "DKK",
            "GBP",
            "RUB",
            "NZD",
            "MXN",
            "IDR",
            "TWD",
            "THB",
            "VND",
        ]
        with Live(console=console) as live_table:
            exchange_rate_dict: Dict[Tuple[str, str], float] = {}

            for index in range(100):
                select_exchange = exchanges[index % len(exchanges)]
                time.sleep(0.1)
                console.log("can still log")
                for exchange in exchanges:
                    if exchange == select_exchange:
                        continue

                    exchange_rate_dict[(select_exchange, exchange)] = 20 / (
                        (random.random() * 40) + 1
                    )
                    if len(exchange_rate_dict) > len(exchanges) - 1:
                        exchange_rate_dict.pop(list(exchange_rate_dict.keys())[0])
                    table = Table(title="Exchange Rates")

                    table.add_column("Source Currency")
                    table.add_column("Destination Currency")
                    table.add_column("Exchange Rate")

                    for ((soure, dest), exchange_rate) in exchange_rate_dict.items():
                        table.add_row(
                            soure,
                            dest,
                            Text(
                                repr(exchange_rate),
                                style="red" if exchange_rate < 1.0 else "green",
                            ),
                        )

                    live_table.update(table)

    table_example()
    table_example2()
    panel_example()
