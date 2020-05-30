from collections import defaultdict
from operator import itemgetter
from typing import Dict, Iterable, List, Optional, Tuple

from .console import Console, ConsoleOptions, RenderableType, RenderResult
from .measure import Measurement
from .padding import Padding, PaddingDimensions
from .table import Table
from .jupyter import JupyterMixin


class Columns(JupyterMixin):
    """Display renderables in neat columns.

    Args:
        renderables (Iterable[RenderableType]): Any number of Rich renderables (including str),
        padding (PaddingDimensions, optional): Optional padding around cells. Defaults to (0, 1).
    """

    def __init__(
        self,
        renderables: Iterable[RenderableType],
        padding: PaddingDimensions = (0, 1),
        expand: bool = False,
        equal: bool = False,
        column_first: bool = False,
    ) -> None:
        self.renderables = list(renderables)
        self.padding = padding
        self.expand = expand
        self.equal = equal
        self.column_first = column_first

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        render_str = console.render_str
        renderables = [
            render_str(renderable) if isinstance(renderable, str) else renderable
            for renderable in self.renderables
        ]

        _top, right, _bottom, left = Padding.unpack(self.padding)
        width_padding = max(left, right)

        max_width = options.max_width

        widths: Dict[int, int] = defaultdict(int)
        column_count = len(renderables)

        get_measurement = Measurement.get
        renderable_widths = [
            get_measurement(console, renderable, max_width).maximum
            for renderable in renderables
        ]

        def iter_renderables(
            column_count: int,
        ) -> Iterable[Tuple[int, Optional[RenderableType]]]:
            if self.column_first:
                width_renderables = list(zip(renderable_widths, renderables))
                row_count = (len(renderables) + column_count - 1) // column_count
                for index in range(row_count * column_count):
                    _index = ((index % row_count) * column_count) + index // row_count
                    try:
                        yield width_renderables[_index]
                    except IndexError:
                        yield 0, None
            else:
                yield from zip(renderable_widths, renderables)

        table = Table.grid(padding=self.padding, collapse_padding=True, pad_edge=False)
        table.expand = self.expand

        if self.equal:
            maximum_column = max(renderable_widths)
            column_count = max_width // maximum_column
            for _ in range(column_count):
                table.add_column(ratio=1)
        else:
            while column_count > 1:
                widths.clear()
                column_no = 0
                for renderable_width, renderable in iter_renderables(column_count):
                    widths[column_no] = max(widths[column_no], renderable_width)
                    total_width = sum(widths.values()) + width_padding * (
                        len(widths) - 1
                    )
                    if total_width > max_width:
                        column_count = len(widths) - 1
                        break
                    else:
                        column_no = (column_no + 1) % column_count
                else:
                    break
            column_count = max(column_count, 1)

        add_row = table.add_row
        get_renderable = itemgetter(1)
        _renderables = [
            get_renderable(_renderable)
            for _renderable in iter_renderables(column_count)
        ]
        for start in range(0, len(_renderables), column_count):
            add_row(*_renderables[start : start + column_count])
        yield table


if __name__ == "__main__":
    import os

    console = Console()

    from rich.panel import Panel

    files = [s for s in sorted(os.listdir())]
    columns = Columns(files, padding=(0, 1), expand=True, equal=True)
    console.print(columns)
    console.rule()
    columns.column_first = True
    console.print(columns)
