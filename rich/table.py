from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Sequence, Tuple, Union

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

    title: Optional[RenderableType] = None
    width: Optional[int] = None
    ratio: Optional[int] = None
    renderables: List[RenderableType] = field(default_factory=list)

    def measure(self, max_width: int) -> Tuple[int, int]:
        column_min_widths: List[int] = []
        column_max_widths: List[int] = []
        append_min = column_min_widths.append
        append_max = column_max_widths.append
        get_render_width = RenderWidth.get
        for renderable in self.renderables:
            _min_width, _max_width = get_render_width(renderable, max_width)
            append_min(_min_width)
            append_max(_max_width)
        return max(column_min_widths), max(column_max_widths)


class Table:
    columns: List[Column]

    def __init__(
        self, *headers: Union[Column, str], box: Optional[Box] = None, fit: bool = True
    ) -> None:
        self.box = box
        self.columns = [
            (Column(header) if isinstance(header, str) else header)
            for header in headers
        ]
        self.fit = fit

    def add_row(self, *renderables: Optional[RenderableType]) -> None:

        for index, renderable in enumerate(renderables):
            if index == len(self.columns):
                self.columns.append(Column())
            column = self.columns[index]
            if isinstance(renderable, ConsoleRenderable):
                column.renderables.append(renderable)
            elif renderable is None:
                column.renderables.append("")
            else:
                column.renderables.append(str(renderable))

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        max_width = options.max_width
        if self.box:
            max_width -= len(self.columns) + 2

        columns = self.columns
        # Fixed width
        render_widths: List[Optional[Tuple[int, int]]] = [
            (column.width, column.width) if column.width else None for column in columns
        ]

        for index, (width, column) in enumerate(zip(render_widths, columns)):
            if width is None:
                render_widths[index] = column.measure(max_width)

        table_width = sum(_max for _min, _max in render_widths)

        if self.fit:
            widths = [_max for _min, _max in render_widths]

        yield Segment("-" * max_width)
        yield Segment.new_line()
        print(widths)
        for index, width in enumerate(widths):
            yield Segment(str(index) * width)
        yield Segment.new_line()


if __name__ == "__main__":

    c = Console(width=60)
    table = Table("Column1", "Column2", "Column3")

    table.add_row(
        Text("This column contains text with" * 2),
        Text("This column contains text with" * 3),
        "Hello",
    )
    from .markdown import Markdown

    table.add_row(Markdown("Hello *World*!"), "More text", "Hello WOrld")

    c.print(table)
