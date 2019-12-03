from __future__ import annotations

from dataclasses import dataclass, field
from itertools import chain
from typing import Iterable, List, Optional, Sequence, Tuple, Union

from .box import Box, SQUARE
from .console import (
    Console,
    ConsoleOptions,
    ConsoleRenderable,
    RenderableType,
    RenderResult,
    RenderWidth,
)
from .segment import Segment
from .text import Text
from ._tools import iter_last, ratio_divide


@dataclass
class Column:
    """Defines a column in a table."""

    title: RenderableType = ""
    width: Optional[int] = None
    ratio: Optional[int] = None
    _cells: List[RenderableType] = field(default_factory=list)

    @property
    def cells(self) -> Iterable[RenderableType]:
        """Get all cells in the column, including header."""
        return chain([self.title], self._cells)

    @property
    def flexible(self) -> bool:
        """Check if this column is flexible."""
        return self.ratio is not None

    def measure(self, max_width: int) -> RenderWidth:
        """Get the minimum and maximum width of the column."""
        if self.width is not None:
            # Fixed width column
            return RenderWidth(self.width, self.width)
        # Flexible column, we need to measure contents
        column_min_widths: List[int] = []
        column_max_widths: List[int] = []
        append_min = column_min_widths.append
        append_max = column_max_widths.append
        get_render_width = RenderWidth.get
        for renderable in self.cells:
            _min_width, _max_width = get_render_width(renderable, max_width)
            append_min(_min_width)
            append_max(_max_width)
        return RenderWidth(max(column_min_widths), max(column_max_widths))


class Table:
    columns: List[Column]

    def __init__(
        self,
        *headers: Union[Column, str],
        width: int = None,
        box: Optional[Box] = None,
        expand: bool = False
    ) -> None:
        self.width = width
        self.box = box
        self.columns = [
            (Column(header) if isinstance(header, str) else header)
            for header in headers
        ]
        self.expand = expand

    def add_row(self, *renderables: Optional[RenderableType]) -> None:

        for index, renderable in enumerate(renderables):
            if index == len(self.columns):
                self.columns.append(Column())
            column = self.columns[index]
            if isinstance(renderable, ConsoleRenderable):
                column._cells.append(renderable)
            elif renderable is None:
                column._cells.append("")
            else:
                column._cells.append(str(renderable))

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        columns = self.columns
        max_width = options.max_width
        if self.width is not None:
            max_width = min(self.width, max_width)
        if self.box:
            max_width -= len(self.columns) + 2

        # Fixed width
        width_ranges = [column.measure(max_width) for column in columns]
        widths = [_range.maximum for _range in width_ranges]

        if self.expand:
            widths = [_range.maximum for _range in width_ranges]
            fixed_widths = [_range.minimum for _range in width_ranges]
            flexible_width = max_width - sum(fixed_widths)
            ratios = [col.ratio or 0 for col in columns if col.flexible]
            flex_minimum = [column.width or 1 for column in columns if column.flexible]
            flex_widths = ratio_divide(flexible_width, ratios, flex_minimum)
            iter_flex_widths = iter(flex_widths)
            for index, (column, width) in enumerate(zip(columns, widths)):
                if column.flexible:
                    widths[index] = next(iter_flex_widths)

        table_width = sum(widths)
        if table_width > max_width:
            flex_widths = [_range.span for _range in width_ranges]
            if not any(flex_widths):
                flex_widths = [1] * len(flex_widths)
            excess_width = table_width - max_width
            shrink_widths = ratio_divide(excess_width, flex_widths)
            widths = [_width - shrink for _width, shrink in zip(widths, shrink_widths)]
        elif table_width < max_width and self.expand:
            pad_widths = ratio_divide(max_width - table_width, widths)
            widths = [_width + pad for _width, pad in zip(widths, pad_widths)]

        yield Segment("-" * max_width)
        yield Segment.line()

        for index, width in enumerate(widths):
            yield Segment(str(index) * width)
        yield Segment.line()

    def _render(self, widths: List[int]) -> RenderResult:
        pass


if __name__ == "__main__":

    for w in range(10, 110):
        c = Console(width=w)
        table = Table(
            Column("Column1", ratio=2),
            Column("Column2", ratio=1, width=4),
            "Column3",
            expand=True,
        )

        table.add_row(
            Text("Hello"), Text("world" * 2), "Hello",
        )
        from .markdown import Markdown

        # table.add_row(Markdown("Hello *World*!"), "More text", "Hello WOrld")

        c.print(table)
