from datetime import datetime
from typing import Iterable, List, Optional, TYPE_CHECKING, Union, Callable


from .text import Text, TextType

if TYPE_CHECKING:
    from .console import Console, ConsoleRenderable, RenderableType
    from .table import Table

FormatTimeCallable = Callable[[datetime], Text]



BRANCH_COVERAGE = {

    "B1": False,
    "B2": False,
    "B3": False,
    "B4": False,
    "B5": False,
    "B6": False,
    "B7": False,
    "B8": False,
    "B9": False,
    "B10": False,
    "B11": False,
    "B12": False,
    "B13": False,
    "B14": False,
    "B15": False,
    "B16": False,
    "B17": False,
    "B18": False

}


class LogRender:
    def __init__(
        self,
        show_time: bool = True,
        show_level: bool = False,
        show_path: bool = True,
        time_format: Union[str, FormatTimeCallable] = "[%x %X]",
        omit_repeated_times: bool = True,
        level_width: Optional[int] = 8,
    ) -> None:
        self.show_time = show_time
        self.show_level = show_level
        self.show_path = show_path
        self.time_format = time_format
        self.omit_repeated_times = omit_repeated_times
        self.level_width = level_width
        self._last_time: Optional[Text] = None

    def __call__(
        self,
        console: "Console",
        renderables: Iterable["ConsoleRenderable"],
        log_time: Optional[datetime] = None,
        time_format: Optional[Union[str, FormatTimeCallable]] = None,
        level: TextType = "",
        path: Optional[str] = None,
        line_no: Optional[int] = None,
        link_path: Optional[str] = None,
    ) -> "Table":
        from .containers import Renderables
        from .table import Table

        output = Table.grid(padding=(0, 1))
        output.expand = True

        # --- Columns ---
        if self.show_time:
            BRANCH_COVERAGE["B1"] = True
            output.add_column(style="log.time")
        else:
            BRANCH_COVERAGE["B2"] = True

        if self.show_level:
            BRANCH_COVERAGE["B3"] = True
            output.add_column(style="log.level", width=self.level_width)
        else:
            BRANCH_COVERAGE["B4"] = True

        output.add_column(ratio=1, style="log.message", overflow="fold")

        if self.show_path and path:
            BRANCH_COVERAGE["B5"] = True
            output.add_column(style="log.path")
        else:
            BRANCH_COVERAGE["B6"] = True

        row: List["RenderableType"] = []

        # --- Time block ---
        if self.show_time:
            BRANCH_COVERAGE["B7"] = True
            log_time = log_time or console.get_datetime()
            time_format = time_format or self.time_format

            if callable(time_format):
                BRANCH_COVERAGE["B9"] = True
                log_time_display = time_format(log_time)
            else:
                BRANCH_COVERAGE["B10"] = True
                log_time_display = Text(log_time.strftime(time_format))

            if log_time_display == self._last_time and self.omit_repeated_times:
                BRANCH_COVERAGE["B11"] = True
                row.append(Text(" " * len(log_time_display)))
            else:
                BRANCH_COVERAGE["B12"] = True
                row.append(log_time_display)
                self._last_time = log_time_display
        else:
            BRANCH_COVERAGE["B8"] = True

        # --- Level in row ---
        if self.show_level:
            BRANCH_COVERAGE["B13"] = True
            row.append(level)
        else:
            BRANCH_COVERAGE["B14"] = True

        row.append(Renderables(renderables))

        # --- Path text ---
        if self.show_path and path:
            BRANCH_COVERAGE["B15"] = True
            path_text = Text()
            path_text.append(path, style=f"link file://{link_path}" if link_path else "")

            if line_no:
                BRANCH_COVERAGE["B17"] = True
                path_text.append(":")
                path_text.append(
                    f"{line_no}",
                    style=f"link file://{link_path}#{line_no}" if link_path else "",
                )
            else:
                BRANCH_COVERAGE["B18"] = True

            row.append(path_text)
        else:
            BRANCH_COVERAGE["B16"] = True

        output.add_row(*row)
        return output


if __name__ == "__main__":  
    from rich.console import Console

    c = Console()
    c.print("[on blue]Hello", justify="right")
    c.log("[on blue]hello", justify="right")