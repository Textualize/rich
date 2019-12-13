from datetime import datetime
from typing import Any, List, Optional

from .console import Console, ConsoleRenderable, RenderableType
from .containers import Renderables
from .table import Table
from .text import Text


class Logger:
    def __init__(
        self,
        console: Console,
        show_time: bool = True,
        show_path: bool = True,
        time_format: str = "[%x %X] ",
    ) -> None:
        self.console = console
        self.show_time = show_time
        self.show_path = show_path
        self.time_format = time_format
        self._last_time: Optional[datetime] = None

    def __call__(
        self,
        *objects: Any,
        log_time: datetime = None,
        path: str = None,
        line_no: int = None,
    ) -> None:
        output = Table(show_header=False, expand=True, box=None, padding=0)
        if self.show_time:
            output.add_column(style="log.time")
        output.add_column(ratio=1, style="log.message")
        if self.show_path and path:
            output.add_column(style="log.path")
        row: List[RenderableType] = []
        if self.show_time:
            if log_time is None:
                log_time = datetime.now()
            row.append(Text(log_time.strftime(self.time_format)))
        row.append(Renderables(objects))
        if self.show_path and path:
            if line_no is None:
                row.append(Text(path))
            else:
                row.append(Text(f"{path}:{line_no}"))
        output.add_row(*row)

        self.console.print(output)


if __name__ == "__main__":
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
        s, path="foo.py", line_no=20,
    )
