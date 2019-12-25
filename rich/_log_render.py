from datetime import datetime
from typing import Any, Iterable, List, Optional, TYPE_CHECKING

from .text import Text

if TYPE_CHECKING:
    from .console import Console, ConsoleRenderable, RenderableType
    from table import Table


class LogRender:
    def __init__(
        self,
        show_time: bool = True,
        show_path: bool = True,
        time_format: str = "[%x %X] ",
    ) -> None:
        self.show_time = show_time
        self.show_path = show_path
        self.time_format = time_format
        self._last_time: Optional[str] = None

    def __call__(
        self,
        console: "Console",
        renderables: Iterable["ConsoleRenderable"],
        log_time: datetime = None,
        path: str = None,
        line_no: int = None,
    ) -> "Table":
        from .containers import Renderables
        from .table import Table

        output = Table(show_header=False, expand=True, box=None, padding=0)
        if self.show_time:
            output.add_column(style="log.time")
        output.add_column(ratio=1, style="log.message")
        if self.show_path and path:
            output.add_column(style="log.path")
        row: List["RenderableType"] = []
        if self.show_time:
            if log_time is None:
                log_time = datetime.now()
            log_time_display = log_time.strftime(self.time_format)
            if log_time_display == self._last_time:
                row.append(Text(" " * len(log_time_display)))
            else:
                row.append(log_time_display)
                self._last_time = log_time_display
        row.append(Renderables(renderables))
        if self.show_path and path:
            if line_no is None:
                row.append(Text(path))
            else:
                row.append(Text(f"{path}:{line_no}"))
        output.add_row(*row)
        return output


if __name__ == "__main__":  # pragma: no cover
    from .console import Console

    console = Console()
    print(console)
    logger = Logger(console)

    from .markdown import Markdown
    from .syntax import Syntax

    s = Syntax(
        '''\
@classmethod
def get(cls, renderable: RenderableType, max_width: int) -> RenderWidth:
    """Get desired width for a renderable."""
    if hasattr(renderable, "__console__"):
        get_console_width = getattr(renderable, "__console_width__", None)
        if get_console_width is not None:
            render_width = get_console_width(max_width).with_maximum(max_width)
            return render_width.normalize()
        else:
            return RenderWidth(1, max_width)
    elif isinstance(renderable, Segment):
        text, _style = renderable
        width = min(max_width, len(text))
        return RenderWidth(width, width)
    elif isinstance(renderable, str):
        text = renderable.rstrip()
        return RenderWidth(len(text), len(text))
    else:
        raise errors.NotRenderableError(
            f"Unable to get render width for {renderable!r}; "
            "a str, Segment, or object with __console__ method is required"
        )
        ''',
        "python",
        theme="monokai",
    )

    logger(
        "Hello", path="foo.py", line_no=20,
    )
    logger(
        "World!", path="foo.py", line_no=20,
    )
