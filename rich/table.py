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
from .text import Text
from ._tools import iter_last


@dataclass
class Column:

    title: Optional[RenderableType] = None
    width: Optional[int] = None
    renderables: List[ConsoleRenderable] = field(default_factory=list)


class Table:
    columns: List[Column]

    def __init__(
        self, *headers: Union[Column, str], box: Optional[Box] = SQUARE
    ) -> None:
        self.box = box
        self.columns = [
            (Column(header) if isinstance(header, str) else header)
            for header in headers
        ]

    def add_row(self, *renderables: Optional[RenderableType]) -> None:
        row: List[Optional[ConsoleRenderable]] = []
        for index, renderable in enumerate(renderables):
            if index == len(self.columns):
                self.columns.append(Column(ratio=1))
            column = self.columns[index]
            if isinstance(renderable, ConsoleRenderable):
                column.renderables.append(renderable)
            elif renderable is None:
                column.renderables.append(Text(""))
            else:
                column.renderables.append(Text(str(renderable)))

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        remaining_width = options.max_width
        if self.box:
            remaining_width -= len(self.columns) + 2

        max_width = options.max_width
        width_ranges: List[Tuple[int, int]] = []

        for column in self.columns:

            if column.width is not None:
                width_ranges.append((column.width, column.width))
            else:
                min_widths: List[int] = []
                max_widths: List[int] = []
                append_min = min_widths.append
                append_max = max_widths.append
                for renderable in column.renderables:
                    _min_width, _max_width = RenderWidth.get(renderable, max_width)
                    append_min(_min_width)
                    append_max(_max_width)
                width_ranges.append((max(min_widths), max(max_widths)))


if __name__ == "__main__":
    c = Console()
    table = Table("Column1", "Column2", "Column3")

    table.add_row("This column contains text", "More text", "Hello")
    from .markdown import Markdown

    table.add_row(Markdown("Hello, *World*!"), "More text", "Hello")

    c.print(table)
