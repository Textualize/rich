import sys
from threading import Event, RLock, Thread
from typing import IO, Any, List, Optional, Text

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
        transient: bool = False,
        redirect_stdout: bool = True,
        redirect_stderr: bool = True,
        auto_refresh: bool = True,
        refresh_per_second: float = 1.0,
        hide_overflow: bool = True
    ) -> None:
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
        with self._lock:
            return self._live_render.renderable

    def update(self, renderable: RenderableType, *, refresh: bool = False) -> None:
        with self._lock:
            self._live_render.set_renderable(renderable)
            if refresh:
                self.refresh()

    def refresh(self) -> None:
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
