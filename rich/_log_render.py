from datetime import datetime
from typing import Any, Iterable, List, Optional, TYPE_CHECKING, Union


from .text import Text

if TYPE_CHECKING:
    from .console import Console, ConsoleRenderable, RenderableType
    from .table import Table


class LogRender:
    def __init__(
        self,
        show_time: bool = True,
        show_level: bool = False,
        show_path: bool = True,
        time_format: str = "[%x %X]",
    ) -> None:
        self.show_time = show_time
        self.show_level = show_level
        self.show_path = show_path
        self.time_format = time_format
        self._last_time: Optional[str] = None

    def __call__(
        self,
        console: "Console",
        renderables: Iterable["ConsoleRenderable"],
        log_time: datetime = None,
        time_format: str = None,
        level: Union[str, Text] = "",
        path: str = None,
        line_no: int = None,
    ) -> "Table":
        from .containers import Renderables
        from .table import Table

        output = Table(show_header=False, expand=True, box=None, padding=(0, 1, 0, 0))
        if self.show_time:
            output.add_column(style="log.time")
        if self.show_level:
            output.add_column(style="log.level", width=8)
        output.add_column(ratio=1, style="log.message", justify=None)
        if self.show_path and path:
            output.add_column(style="log.path")
        row: List["RenderableType"] = []
        if self.show_time:
            if log_time is None:
                log_time = datetime.now()
            log_time_display = log_time.strftime(time_format or self.time_format)
            if log_time_display == self._last_time:
                row.append(Text(" " * len(log_time_display)))
            else:
                row.append(Text(log_time_display))
                self._last_time = log_time_display
        if self.show_level:
            row.append(level)

        row.append(Renderables(renderables))
        if self.show_path and path:
            row.append(Text(f"{path}:{line_no}" if line_no else path))

        output.add_row(*row)
        return output
