import sys
from threading import Event, RLock, Thread
from typing import IO, Any, List, Optional

from typing_extensions import Literal

from .__init__ import get_console
from ._loop import loop_last
from .console import (
    Console,
    ConsoleOptions,
    ConsoleRenderable,
    RenderableType,
    RenderHook,
    RenderResult,
)
from .control import Control
from .file_proxy import FileProxy
from .jupyter import JupyterMixin
from .live_render import LiveRender
from .segment import Segment
from .style import Style
from .text import Text

VerticalOverflowMethod = Literal["crop", "ellipsis", "visible"]


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
            with self.live._lock:
                self.live.refresh()


class _LiveRender(LiveRender):
    def __init__(self, live: "Live", renderable: RenderableType) -> None:
        self._live = live
        self.renderable = renderable
        self._shape: Optional[Tuple[int, int]] = None

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        with self._live._lock:
            lines = console.render_lines(self.renderable, options, pad=False)

            shape = Segment.get_shape(lines)
            _, height = shape
            if height > console.size.height:
                if self._live.vertical_overflow == "crop":
                    lines = lines[: console.size.height]
                    shape = Segment.get_shape(lines)
                elif self._live.vertical_overflow == "ellipsis":
                    lines = lines[: (console.size.height - 1)]
                    lines.append(
                        list(
                            console.render(
                                Text(
                                    "...",
                                    overflow="crop",
                                    justify="center",
                                    end="",
                                    style="live.ellipsis",
                                )
                            )
                        )
                    )
                    shape = Segment.get_shape(lines)

            self._shape = shape

            for last, line in loop_last(lines):
                yield from line
                if not last:
                    yield Segment.line()


class Live(JupyterMixin, RenderHook):
    """Renders an auto-updating live display of any given renderable.

    Args:
        renderable (RenderableType, optional): [The renderable to live display. Defaults to displaying nothing.
        console (Console, optional): Optional Console instance. Default will an internal Console instance writing to stdout.
        auto_refresh (bool, optional): Enable auto refresh. If disabled, you will need to call `refresh()` or `update()` with refresh flag. Defaults to True
        refresh_per_second (float, optional): Number of times per second to refresh the live display. Defaults to 1.
        transient (bool, optional): Clear the renderable on exit. Defaults to False.
        redirect_stdout (bool, optional): Enable redirection of stdout, so ``print`` may be used. Defaults to True.
        redirect_stderr (bool, optional): Enable redirection of stderr. Defaults to True.
        vertical_overflow (VerticalOverflowMethod, optional): How to handle renderable when it is too tall for the console. Defaults to "ellipsis".
    """

    def __init__(
        self,
        renderable: RenderableType = "",
        *,
        console: Console = None,
        auto_refresh: bool = True,
        refresh_per_second: float = 4,
        transient: bool = False,
        redirect_stdout: bool = True,
        redirect_stderr: bool = True,
        vertical_overflow: VerticalOverflowMethod = "ellipsis",
    ) -> None:
        assert refresh_per_second > 0, "refresh_per_second must be > 0"
        self.console = console if console is not None else get_console()
        self._live_render = _LiveRender(self, renderable)

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

        self.vertical_overflow = vertical_overflow
        # cant store just clear_control as the live_render shape is lazily computed on render

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
                    self._refresh_thread.join()
                    self._refresh_thread = None
                # allow it to fully render on the last even if overflow
                self.vertical_overflow = "visible"
                if not self.console.is_jupyter:
                    self.refresh()
                if self.console.is_terminal:
                    self.console.line()
            finally:
                self._disable_redirect_io()
                self.console.pop_render_hook()
                self.console.show_cursor(True)

            if self.transient:
                self.console.control(self._live_render.restore_cursor())
            if self.ipy_widget is not None:  # pragma: no cover
                if self.transient:
                    self.ipy_widget.close()
                else:
                    # jupyter last refresh must occur after console pop render hook
                    # i am not sure why this is needed
                    self.refresh()

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
                sys.stdout = FileProxy(self.console, sys.stdout)
            if self._redirect_stderr:
                self._restore_stderr = sys.stderr
                sys.stderr = FileProxy(self.console, sys.stderr)

    @property
    def renderable(self) -> RenderableType:
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
        elif (
            not self._started and not self.transient
        ):  # if it is finished allow files or dumb-terminals to see final result
            with self.console:
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
                # determine the control command needed to clear previous rendering
                renderables = [
                    self._live_render.position_cursor(),
                    *renderables,
                    self._live_render,
                ]
        elif (
            not self._started and not self.transient
        ):  # if it is finished render the final output for files or dumb_terminals
            renderables = [*renderables, self._live_render]

        return renderables


if __name__ == "__main__":  # pragma: no cover
    import random
    import time
    from itertools import cycle
    from typing import Dict, List, Tuple

    from .console import Console
    from .live import Live
    from .panel import Panel
    from .rule import Rule
    from .syntax import Syntax
    from .table import Table

    console = Console()

    syntax = Syntax(
        '''def loop_last(values: Iterable[T]) -> Iterable[Tuple[bool, T]]:
    """Iterate and generate a tuple with a flag for last value."""
    iter_values = iter(values)
    try:
        previous_value = next(iter_values)
    except StopIteration:
        return
    for value in iter_values:
        yield False, previous_value
        previous_value = value
    yield True, previous_value''',
        "python",
        line_numbers=True,
    )

    table = Table("foo", "bar", "baz")
    table.add_row("1", "2", "3")

    progress_renderables = [
        "You can make the terminal shorter and taller to see the live table hide"
        "Text may be printed while the progress bars are rendering.",
        Panel("In fact, [i]any[/i] renderable will work"),
        "Such as [magenta]tables[/]...",
        table,
        "Pretty printed structures...",
        {"type": "example", "text": "Pretty printed"},
        "Syntax...",
        syntax,
        Rule("Give it a try!"),
    ]

    examples = cycle(progress_renderables)

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

            for exchange in exchanges:
                if exchange == select_exchange:
                    continue
                time.sleep(0.4)
                if random.randint(0, 10) < 1:
                    console.log(next(examples))
                exchange_rate_dict[(select_exchange, exchange)] = 200 / (
                    (random.random() * 320) + 1
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
                            f"{exchange_rate:.4f}",
                            style="red" if exchange_rate < 1.0 else "green",
                        ),
                    )

                live_table.update(table)
