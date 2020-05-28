import io
from typing import Any, Iterable, IO, List, Optional, TYPE_CHECKING, Union

# from .console import Console as BaseConsole
from .segment import Segment
from .style import Style
from .terminal_theme import DEFAULT_TERMINAL_THEME

if TYPE_CHECKING:
    from .console import Console

JUPYTER_HTML_FORMAT = """\
<pre style="white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">{code}</pre>
"""


_console: Optional["Console"] = None


def get_console() -> "Console":
    from .console import Console

    global _console
    if _console is None:
        _console = Console(width=100)
    return _console


def is_jupyter() -> bool:
    """Check if we're running in a Jupyter notebook."""
    try:
        get_ipython  # type: ignore
    except NameError:
        return False
    shell = get_ipython().__class__.__name__  # type: ignore
    if shell == "ZMQInteractiveShell":
        return True  # Jupyter notebook or qtconsole
    elif shell == "TerminalInteractiveShell":
        return False  # Terminal running IPython
    else:
        return False  # Other type (?)


class JupyterRenderable:
    """A shim to write html to Jupyter notebook."""

    def __init__(self, html: str) -> None:
        self.html = html

    @classmethod
    def render(self, rich_renderable) -> str:
        console = get_console()
        segments = console.render(rich_renderable, console.options)
        html = _render_segments(segments)
        return html

    def _repr_html_(self) -> str:
        return self.html


class JupyterMixin:
    """Add to an Rich renderable to make it render in Jupyter notebook."""

    def _repr_html_(self) -> str:
        console = get_console()
        segments = list(console.render(self, console.options))  # type: ignore
        html = _render_segments(segments)
        return html


def _render_segments(segments: Iterable[Segment]) -> str:
    def escape(text: str) -> str:
        """Escape html."""
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    fragments: List[str] = []
    append_fragment = fragments.append
    theme = DEFAULT_TERMINAL_THEME
    for text, style, is_control in Segment.simplify(segments):
        if is_control:
            continue
        text = escape(text)
        if style:
            rule = style.get_html_style(theme)
            text = f'<span style="{rule}">{text}</span>' if rule else text
            if style.link:
                text = f'<a href="{style.link}">{text}</a>'
        append_fragment(text)

    code = "".join(fragments)
    html = JUPYTER_HTML_FORMAT.format(code=code)

    return html


def display(segments: Iterable[Segment]) -> None:
    """Render segments to Jupyter."""
    from IPython.display import display as ipython_display

    html = _render_segments(segments)
    jupyter_renderable = JupyterRenderable(html)
    ipython_display(jupyter_renderable)
