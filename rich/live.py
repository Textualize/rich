import sys
from threading import Event, RLock, Thread
from types import TracebackType
from typing import IO, Any, Callable, List, Optional, TextIO, Type, cast
import contextlib
import time
import signal
import atexit
import os

from . import get_console
from .console import Console, ConsoleRenderable, RenderableType, RenderHook
from .control import Control
from .file_proxy import FileProxy
from .jupyter import JupyterMixin
from .live_render import LiveRender, VerticalOverflowMethod
from .screen import Screen
from .text import Text


class _RefreshThread(Thread):
    """A thread that calls refresh() at regular intervals."""

    def __init__(self, live: "Live", refresh_per_second: float) -> None:
        self.live = live
        self.refresh_per_second = refresh_per_second
        self.done = Event()
        super().__init__(daemon=True)

    def stop(self) -> None:
        self.done.set()

    def run(self) -> None:
        while not self.done.wait(1 / self.refresh_per_second):
            with self.live._lock:
                if not self.done.is_set():
                    self.live.refresh()


class Live(JupyterMixin, RenderHook):
    """Renders an auto-updating live display of any given renderable.

    Args:
        renderable (RenderableType, optional): The renderable to live display. Defaults to displaying nothing.
        console (Console, optional): Optional Console instance. Defaults to an internal Console instance writing to stdout.
        screen (bool, optional): Enable alternate screen mode. Defaults to False.
        auto_refresh (bool, optional): Enable auto refresh. If disabled, you will need to call `refresh()` or `update()` with refresh flag. Defaults to True
        refresh_per_second (float, optional): Number of times per second to refresh the live display. Defaults to 4.
        transient (bool, optional): Clear the renderable on exit (has no effect when screen=True). Defaults to False.
        redirect_stdout (bool, optional): Enable redirection of stdout, so ``print`` may be used. Defaults to True.
        redirect_stderr (bool, optional): Enable redirection of stderr. Defaults to True.
        vertical_overflow (VerticalOverflowMethod, optional): How to handle renderable when it is too tall for the console. Defaults to "ellipsis".
        get_renderable (Callable[[], RenderableType], optional): Optional callable to get renderable. Defaults to None.
    """

    def __init__(
        self,
        renderable: Optional[RenderableType] = None,
        *,
        console: Optional[Console] = None,
        screen: bool = False,
        auto_refresh: bool = True,
        refresh_per_second: float = 4,
        transient: bool = False,
        redirect_stdout: bool = True,
        redirect_stderr: bool = True,
        vertical_overflow: VerticalOverflowMethod = "ellipsis",
        get_renderable: Optional[Callable[[], RenderableType]] = None,
    ) -> None:
        assert refresh_per_second > 0, "refresh_per_second must be > 0"
        self._renderable = renderable
        self.console = console if console is not None else get_console()
        self._screen = screen
        self._alt_screen = False

        self._redirect_stdout = redirect_stdout
        self._redirect_stderr = redirect_stderr
        self._restore_stdout: Optional[IO[str]] = None
        self._restore_stderr: Optional[IO[str]] = None

        self._lock = RLock()
        self.ipy_widget: Optional[Any] = None
        self.auto_refresh = auto_refresh
        self._started: bool = False
        self.transient = True if screen else transient

        self._refresh_thread: Optional[_RefreshThread] = None
        self.refresh_per_second = refresh_per_second

        self.vertical_overflow = vertical_overflow
        self._get_renderable = get_renderable
        self._live_render = LiveRender(
            self.get_renderable(), vertical_overflow=vertical_overflow
        )

        self._start_time: Optional[float] = None
        self._stop_time: Optional[float] = None
        self._refresh_count = 0
        self._refresh_queue: List[Tuple[float, RenderableType]] = []
        self._print_queue: List[Tuple[RenderableType, dict]] = []
        self._queued_writes = True
        self._closed = False
        self._original_sigint_handler = None
        self._exit_handler_added = False

    @property
    def is_started(self) -> bool:
        """Check if live display has been started."""
        return self._started

    def get_renderable(self) -> RenderableType:
        renderable = (
            self._get_renderable()
            if self._get_renderable is not None
            else self._renderable
        )
        return renderable or ""

    def _handle_sigint(self, sig, frame):
        """Handle SIGINT (Ctrl+C) to ensure cursor is shown."""
        # Restore cursor
        if self.console.is_terminal:
            self.console.show_cursor(True)
        # Re-raise KeyboardInterrupt to allow program to exit
        raise KeyboardInterrupt()

    def _ensure_cursor_visible_at_exit(self):
        """Ensure cursor is visible when program exits."""
        if self.console.is_terminal:
            self.console.show_cursor(True)

    def start(self, refresh: bool = False) -> "Live":
        """Start live rendering display.

        Args:
            refresh (bool, optional): Also refresh. Defaults to False.

        Returns:
            Live: This instance
        """
        with self._lock:
            if self._closed:
                raise LiveError("Live display has been closed")
            if self._started:
                return self
            # Set up signal handler for Ctrl+C
            if not self._exit_handler_added:
                atexit.register(self._ensure_cursor_visible_at_exit)
                self._exit_handler_added = True
            # Only set up SIGINT handler on platforms that support it (not Windows)
            if os.name != "nt" and hasattr(signal, "SIGINT"):
                self._original_sigint_handler = signal.signal(signal.SIGINT, self._handle_sigint)
            
            self._started = True
            self._start_time = self.console.get_time()
            self.console.set_live(self)
            self._alt_screen = self.console.set_alt_screen(True)
            self.console.show_cursor(False)
            self._enable_redirect_io()
            self.console.push_render_hook(self)
            self._live_render.set_renderable(self.renderable)
            self.console.begin_live(
                self._live_render, refresh=refresh, screen=self._screen, transient=True
            )
            if self._redirect_stdout:
                self._stdout = Redirect(self.console, stdout=True, stderr=False)
                self._stdout.__enter__()
            if self._redirect_stderr:
                self._stderr = Redirect(self.console, stdout=False, stderr=True)
                self._stderr.__enter__()

            if self.auto_refresh and not self._refresh_thread:
                self._refresh_thread = _RefreshThread(self, self.refresh_per_second)
                self._refresh_thread.start()
            return self

    def stop(self) -> None:
        """Stop live rendering display."""
        try:
            with self._lock:
                if not self._started:
                    return
                self._started = False
                self._stop_time = self.console.get_time()

                if self._redirect_stdout:
                    self._stdout.__exit__(None, None, None)
                    self._stdout = None  # type: ignore
                if self._redirect_stderr:
                    self._stderr.__exit__(None, None, None)
                    self._stderr = None  # type: ignore

                if self.console.is_jupyter:  # pragma: no cover
                    try:
                        import IPython.display

                        if self.ipy_widget:
                            IPython.display.display(IPython.display.Pretty(self.renderable))
                    except ImportError:
                        pass
                else:
                    cursor = self.console.show_cursor(True)
                    if self.transient:
                        self.console.end_live()
                    else:
                        # Set renderable to transient so it
                        # will be displayed with refresh
                        self.console.end_live(self.renderable)
                
                # Restore original signal handler
                if os.name != "nt" and hasattr(signal, "SIGINT") and self._original_sigint_handler is not None:
                    signal.signal(signal.SIGINT, self._original_sigint_handler)
                    self._original_sigint_handler = None
        except:
            # Ensure cursor is visible even if an exception occurs during stop
            if self.console.is_terminal:
                self.console.show_cursor(True)
            raise

    def __enter__(self) -> "Live":
        self.start(refresh=self._renderable is not None)
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.stop()

    def _enable_redirect_io(self) -> None:
        """Enable redirecting of stdout / stderr."""
        if self.console.is_terminal or self.console.is_jupyter:
            if self._redirect_stdout and not isinstance(sys.stdout, FileProxy):
                self._restore_stdout = sys.stdout
                sys.stdout = cast("TextIO", FileProxy(self.console, sys.stdout))
            if self._redirect_stderr and not isinstance(sys.stderr, FileProxy):
                self._restore_stderr = sys.stderr
                sys.stderr = cast("TextIO", FileProxy(self.console, sys.stderr))

    def _disable_redirect_io(self) -> None:
        """Disable redirecting of stdout / stderr."""
        if self._restore_stdout:
            sys.stdout = cast("TextIO", self._restore_stdout)
            self._restore_stdout = None
        if self._restore_stderr:
            sys.stderr = cast("TextIO", self._restore_stderr)
            self._restore_stderr = None

    @property
    def renderable(self) -> RenderableType:
        """Get the renderable that is being displayed

        Returns:
            RenderableType: Displayed renderable.
        """
        renderable = self.get_renderable()
        return Screen(renderable) if self._alt_screen else renderable

    def update(self, renderable: RenderableType, *, refresh: bool = False) -> None:
        """Update the renderable that is being displayed

        Args:
            renderable (RenderableType): New renderable to use.
            refresh (bool, optional): Refresh the display. Defaults to False.
        """
        if isinstance(renderable, str):
            renderable = self.console.render_str(renderable)
        with self._lock:
            self._renderable = renderable
            if refresh:
                self.refresh()

    def refresh(self) -> None:
        """Update the display of the Live Render."""
        with self._lock:
            self._live_render.set_renderable(self.renderable)
            if self.console.is_jupyter:  # pragma: no cover
                try:
                    from IPython.display import display
                    from ipywidgets import Output
                except ImportError:
                    import warnings

                    warnings.warn('install "ipywidgets" for Jupyter support')
                else:
                    if self.ipy_widget is None:
                        self.ipy_widget = Output()
                        display(self.ipy_widget)

                    with self.ipy_widget:
                        self.ipy_widget.clear_output(wait=True)
                        self.console.print(self._live_render.renderable)
            elif self.console.is_terminal and not self.console.is_dumb_terminal:
                with self.console:
                    self.console.print(Control())
            elif (
                not self._started and not self.transient
            ):  # if it is finished allow files or dumb-terminals to see final result
                with self.console:
                    self.console.print(Control())

    def process_renderables(
        self, renderables: List[ConsoleRenderable]
    ) -> List[ConsoleRenderable]:
        """Process renderables to restore cursor and display progress."""
        self._live_render.vertical_overflow = self.vertical_overflow
        if self.console.is_interactive:
            # lock needs acquiring as user can modify live_render renderable at any time unlike in Progress.
            with self._lock:
                reset = (
                    Control.home()
                    if self._alt_screen
                    else self._live_render.position_cursor()
                )
                renderables = [reset, *renderables, self._live_render]
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

    from .align import Align
    from .console import Console
    from .live import Live as Live
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

                for (source, dest), exchange_rate in exchange_rate_dict.items():
                    table.add_row(
                        source,
                        dest,
                        Text(
                            f"{exchange_rate:.4f}",
                            style="red" if exchange_rate < 1.0 else "green",
                        ),
                    )

                live_table.update(Align.center(table))
