import sys
from typing import Any, IO, List, Optional

from .__init__ import get_console
from .console import Console, ConsoleRenderable, RenderableType, RenderHook
from .control import Control
from .jupyter import JupyterMixin
from .live_render import LiveRender
from .progress import _FileProxy


class Live(JupyterMixin, RenderHook):
    def __init__(
        self,
        renderable: RenderableType = "",
        *,
        console: Console = None,
        transient: bool = False,
        redirect_stdout: bool = True,
        redirect_stderr: bool = True,
    ) -> None:
        self.console = console if console is not None else get_console()
        self._live_render = LiveRender(renderable)

        self._redirect_stdout = redirect_stdout
        self._redirect_stderr = redirect_stderr
        self._restore_stdout: Optional[IO[str]] = None
        self._restore_stderr: Optional[IO[str]] = None

        self.ipy_widget: Optional[Any] = None

        self._started: bool = False
        self.transient = transient

    def start(self) -> None:
        if self._started:
            return

        self.console.show_cursor(False)
        self._enable_redirect_io()
        self.console.push_render_hook(self)
        self._started = True

    def stop(self) -> None:
        if not self._started:
            return
        self._started = False

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

    def update(self, renderable: RenderableType, *, refresh: bool = True) -> None:
        self._live_render.set_renderable(renderable)
        if refresh:
            self.refresh()

    def refresh(self) -> None:
        if self.console.is_jupyter:  # pragma: no cover
            try:
                from ipywidgets import Output
                from IPython.display import display
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
            renderables = [
                self._live_render.position_cursor(),
                *renderables,
                self._live_render,
            ]
        return renderables
