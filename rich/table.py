from __future__ import annotations

from dataclasses import dataclass, field
from itertools import chain
from typing import Iterable, List, Optional, Sequence, Tuple, Union

from . import box

from .console import (
    Console,
    ConsoleOptions,
    ConsoleRenderable,
    JustifyValues,
    RenderableType,
    RenderResult,
    RenderWidth,
)
from . import errors
from .padding import Padding, PaddingDimensions
from .segment import Segment
from .style import Style
from .text import Text
from ._tools import iter_first, iter_last, ratio_divide


@dataclass
class Column:
    """Defines a column in a table."""

    title: Union[str, ConsoleRenderable] = ""
    style: Union[str, Style] = "none"
    justify: JustifyValues = "left"
    width: Optional[int] = None
    ratio: Optional[int] = None
    _cells: List[ConsoleRenderable] = field(default_factory=list)

    @property
    def cells(self) -> Iterable[ConsoleRenderable]:
        """Get all cells in the column, not including header."""
        yield from self._cells

    @property
    def flexible(self) -> bool:
        """Check if this column is flexible."""
        return self.ratio is not None

    @property
    def header(self) -> ConsoleRenderable:
        return (
            Text(self.title, style=self.style)
            if isinstance(self.title, str)
            else self.title
        )


class Table:
    columns: List[Column]

    def __init__(
        self,
        *headers: Union[Column, str],
        width: int = None,
        box: box.Box = box.MINIMAL_DOUBLE_HEAD,
        pad: PaddingDimensions = (0, 1),
        expand: bool = False,
        show_header: bool = True,
        style: Union[str, Style] = "none",
        header_style: Union[str, Style] = "bold",
        border_style: Union[str, Style] = "",
    ) -> None:
        self.columns = [
            (Column(header) if isinstance(header, str) else header)
            for header in headers
        ]
        self.width = width
        self.box = box
        self.padding = Padding.unpack(pad)
        self.expand = expand
        self.show_header = show_header
        self.style = style
        self.header_style = header_style
        self.border_style = border_style
        self._row_count = 0

    def add_row(self, *renderables: Optional[Union[str, ConsoleRenderable]]) -> None:
        def add_cell(column: Column, renderable: ConsoleRenderable):
            column._cells.append(renderable)

        for index, renderable in enumerate(renderables):
            if index == len(self.columns):
                column = Column()
                for _ in range(self._row_count):
                    add_cell(column, Text(""))
                self.columns.append(column)
            else:
                column = self.columns[index]
            if isinstance(renderable, ConsoleRenderable):
                add_cell(column, renderable)
            elif renderable is None:
                add_cell(column, Text(""))
            elif isinstance(renderable, str):
                add_cell(column, Text(renderable))
            else:
                raise errors.NotRenderableError(
                    f"unable to render {renderable!r}; str or object with a __console__ method is required"
                )
        self._row_count += 1

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:

        max_width = options.max_width
        if self.width is not None:
            max_width = min(self.width, max_width)
        if self.box:
            max_width -= len(self.columns) + 2
        widths = self._calculate_column_widths(max_width)
        yield from self._render(console, options, widths)

    def _calculate_column_widths(self, max_width: int) -> List[int]:
        """Calculate the widths of each column."""
        columns = self.columns
        width_ranges = [self._measure_column(column, max_width) for column in columns]
        widths = [_range.maximum for _range in width_ranges]
        if self.expand:
            ratios = [col.ratio or 0 for col in columns if col.flexible]
            if any(ratios):
                fixed_widths = [_range.minimum for _range in width_ranges]
                flex_minimum = [
                    column.width or 1 for column in columns if column.flexible
                ]
                flexible_width = max_width - sum(fixed_widths)
                flex_widths = ratio_divide(flexible_width, ratios, flex_minimum)
                iter_flex_widths = iter(flex_widths)
                for index, column in enumerate(columns):
                    if column.flexible:
                        widths[index] = next(iter_flex_widths)
        table_width = sum(widths)

        if table_width > max_width:
            flex_widths = [_range.span for _range in width_ranges]
            if not any(flex_widths):
                flex_widths = [1] * len(flex_widths)
            excess_width = table_width - max_width
            widths = ratio_divide(
                excess_width, flex_widths, [_range.minimum for _range in width_ranges],
            )
        elif table_width < max_width and self.expand:
            pad_widths = ratio_divide(max_width - table_width, widths)
            widths = [_width + pad for _width, pad in zip(widths, pad_widths)]
        return widths

    def _get_cells(self, column: Column) -> Iterable[ConsoleRenderable]:
        """Get all the cells with padding and optional header."""

        padding = self.padding
        if any(padding):
            if self.show_header:
                yield Padding(column.header, padding)
            for cell in column.cells:
                yield Padding(cell, padding)
        else:
            if self.show_header:
                yield column.header
            yield from column.cells

    def _measure_column(self, column: Column, max_width: int) -> RenderWidth:
        """Get the minimum and maximum width of the column."""
        if column.width is not None:
            # Fixed width column
            return RenderWidth(column.width, column.width)
        # Flexible column, we need to measure contents
        min_widths: List[int] = []
        max_widths: List[int] = []
        append_min = min_widths.append
        append_max = max_widths.append
        get_render_width = RenderWidth.get
        for renderable in self._get_cells(column):
            _min, _max = get_render_width(renderable, max_width)
            append_min(_min)
            append_max(_max)
        return RenderWidth(max(min_widths), max(max_widths))

    def _render(
        self, console: Console, options: ConsoleOptions, widths: List[int]
    ) -> RenderResult:
        style = console.get_style(self.style)
        header_style = style + console.get_style(self.header_style)
        border_style = style + console.get_style(self.border_style)
        rows = zip(*(self._get_cells(column) for column in self.columns))
        box = self.box
        new_line = Segment.line()

        if box:
            yield Segment(box.get_top(widths), border_style)
        for first, row in iter_first(rows):
            max_height = 1
            cells: List[List[List[Segment]]] = []
            for width, cell, column in zip(widths, row, self.columns):
                render_options = options.update(width=width, justify=column.justify)
                lines = console.render_lines(
                    cell, render_options, style=header_style if first else style
                )
                max_height = max(max_height, len(lines))
                cells.append(lines)

            cells[:] = [
                Segment.set_shape(cell, width, max_height, style=style)
                for width, cell in zip(widths, cells)
            ]

            if box:
                if first:
                    left = Segment(box.head_left, border_style)
                    right = Segment(box.head_right, border_style)
                    divider = Segment(box.head_vertical, border_style)
                else:
                    left = Segment(box.mid_left, border_style)
                    right = Segment(box.mid_right, border_style)
                    divider = Segment(box.mid_vertical, border_style)
                for line_no in range(max_height):
                    yield left
                    for last, cell in iter_last(cells):
                        yield from cell[line_no]
                        if not last:
                            yield divider
                    yield right
                    yield new_line
            else:
                for line_no in range(max_height):
                    for last, cell in iter_last(cells):
                        yield from cell[line_no]
                    yield new_line
            if box and first:
                yield Segment(box.get_row(widths, "head"), border_style)

        if box:
            yield Segment(box.get_bottom(widths), border_style)


if __name__ == "__main__":

    c = Console()
    table = Table("Foo", "Bar", expand=False, style="on blue")
    table.columns[0].width = 50
    # table.columns[1].ratio = 1

    table.add_row("Hello, World! " * 8, "cake" * 10)
    from .markdown import Markdown

    table.add_row(Markdown("# This is *Markdown*!"), "More text", "Hello WOrld")
    table.columns[0].justify = "center"
    table.columns[1].justify = "right"

    with c.style("on red"):
        c.print(table)
