from collections import defaultdict
from operator import itemgetter
from typing import Dict, Iterable, List, Optional, Tuple

from .console import Console, ConsoleOptions, RenderableType, RenderResult
from .measure import Measurement
from .padding import Padding, PaddingDimensions
from .table import Table
from .text import Text
from .jupyter import JupyterMixin


class Columns(JupyterMixin):
    """Display renderables in neat columns.

    Args:
        renderables (Iterable[RenderableType]): Any number of Rich renderables (including str),
        padding (PaddingDimensions, optional): Optional padding around cells. Defaults to (0, 1).
        expand (bool, optional): Expand columns to full width. Defaults to False.
        column_first (bool, optional): Align items from top to bottom (rather than left to right). Defaults to False.
        right_to_left (bool, optional): Start column from right hand side. Defaults to False.
    """

    def __init__(
        self,
        renderables: Iterable[RenderableType],
        padding: PaddingDimensions = (0, 1),
        expand: bool = False,
        equal: bool = False,
        column_first: bool = False,
        right_to_left: bool = False,
    ) -> None:
        self.renderables = list(renderables)
        self.padding = padding
        self.expand = expand
        self.equal = equal
        self.column_first = column_first
        self.right_to_left = right_to_left

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
            item_count = len(renderables)
            if self.column_first:
                width_renderables = list(zip(renderable_widths, renderables))
                column_lengths: List[int] = [item_count // column_count] * column_count
                for col_no in range(item_count % column_count):
                    column_lengths[col_no] += 1
                row = 0
                col = 0
                for _ in width_renderables:
                    yield width_renderables[row * column_count + col]
                    column_lengths[col] -= 1
                    if column_lengths[col]:
                        row += 1
                    else:
                        col += 1
                        row = 0
            else:
                yield from zip(renderable_widths, renderables)
            # Pad odd elements with spaces
            if item_count % column_count:
                for _ in range(column_count - (item_count % column_count)):
                    yield 0, None

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
                for renderable_width, _ in iter_renderables(column_count):
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

        right_to_left = self.right_to_left
        for start in range(0, len(_renderables), column_count):
            row = _renderables[start : start + column_count]
            if right_to_left:
                row = row[::-1]
            add_row(*row)
        yield table


if __name__ == "__main__":
    import os

    console = Console()

    from rich.panel import Panel

    files = [f"{i} {s}" for i, s in enumerate(sorted(os.listdir()))]
    columns = Columns(files, padding=(0, 1), expand=False, equal=False)
    console.print(columns)
    console.rule()
    columns.column_first = True
    console.print(columns)
    columns.right_to_left = True
    console.rule()
    console.print(columns)
    print(len(files))
