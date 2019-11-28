from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Sequence, Union

from .box import Box, SQUARE
from .console import (
    Console,
    ConsoleOptions,
    ConsoleRenderable,
    RenderableType,
    RenderResult,
)
from .text import Text
from ._tools import iter_last


@dataclass
class Column:

    label: Optional[RenderableType] = None
    width: Optional[int] = None
    ratio: int = 1


class Table:
    columns: List[Column]
    _rows: List[Sequence[Optional[RenderableType]]]

    def __init__(
        self, *headers: Union[Column, str], box: Optional[Box] = SQUARE
    ) -> None:
        self.box = box
        self.columns = [
            (Column(header) if isinstance(header, str) else header)
            for header in headers
        ]
        self._rows = []

    def add_row(self, *renderables: Optional[RenderableType]) -> None:

        row: List[Optional[ConsoleRenderable]] = []
        for index, renderable in enumerate(renderables):
            if index == len(self.columns):
                self.columns.append(Column(ratio=1))
            if isinstance(renderable, ConsoleRenderable):
                row.append(renderable)
            elif renderable is None:
                row.append(Text(""))
            else:
                row.append(Text(str(renderable)))
        self._rows.append(row)

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        width = options.max_width
        has_border = self.box is not None
        fixed_width = sum(
            column.width for column in self.columns if column.width is not None
        )
        if self.box:
            fixed_width += len(self.columns) + 1

        variable_width = width - fixed_width
        variable_ratio = sum(
            column.ratio for column in self.columns if column.width is None
        )

        ratio_width = (width - fixed_width) / variable_ratio_total

        remaining_width = width
        remaining_variable = width - fixed_width
        if has_border:
            remaining_width -= len(self.columns) + 1

        for last, column in iter_last(self.columns):

            if column.width is None:
                cell_width = (column.ratio / variable_ratio) * remaining_variable
                variable_ratio = column.ratio
            else:
                cell_width = column.width
            remaining_width -= cell_width


if __name__ == "__main_":
    c = Console()
    table = Table("Column1", "Column2", "Column3")

    table.add_row("This column contains text", "More text", "Hello")
    from .markdown import Markdown

    table.add_row(Markdown("Hello, *World*!"), "More text", "Hello")

    c.print(table)
