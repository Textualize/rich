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
from ._tools import iter_last


@dataclass
class Column:

    title: Optional[RenderableType] = None
    width: Optional[int] = None
    renderables: List[RenderableType] = field(default_factory=list)


class Table:
    columns: List[Column]

    def __init__(
        self, *headers: Union[Column, str], box: Optional[Box] = None, fit: bool = False
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
        remaining_width = options.max_width
        if self.box:
            remaining_width -= len(self.columns) + 2

        min_widths: List[int] = []
        max_widths: List[int] = []

        for column in self.columns:
            if column.width is None:
                column_min_widths: List[int] = []
                column_max_widths: List[int] = []
                append_min = column_min_widths.append
                append_max = column_max_widths.append
                for renderable in column.renderables:
                    _min_width, _max_width = RenderWidth.get(
                        renderable, options.max_width
                    )
                    append_min(_min_width)
                    append_max(_max_width)
                min_widths.append(max(column_min_widths))
                max_widths.append(max(column_max_widths))
            else:
                min_widths.append(column.width)
                max_widths.append(column.width)

        print(min_widths, max_widths)

        widths = max_widths[:]
        table_width = sum(widths)
        if not self.fit:
            if table_width > options.max_width:
                flexible_widths = [
                    _max - _min for _min, _max in zip(min_widths, max_widths)
                ]
                total_flexible = sum(flexible_widths)
            elif table_width < options.max_width:
                column_count = len(widths)
                for index in range(options.max_width - table_width):
                    widths[index % column_count] += 1

        yield Segment("-" * options.max_width)
        yield Segment("\n")
        for index, width in enumerate(widths):
            yield Segment(str(index) * width)
        yield "\n"


if __name__ == "__main__":

    for w in range(10, 20):
        c = Console(width=w)
        table = Table("Column1", "Column2", "Column3")

        table.add_row(
            Text("This column contains text with" * 2),
            Text("This column contains text with" * 3),
            "Hello",
        )
        from .markdown import Markdown

        table.add_row(Markdown("Hello *World*!"), "More text", "Hello WOrld")

        c.print(table)
