from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Sequence, Union

from .box import Box, SQUARE
from .console import (
    Console,
    ConsoleOptions,
    ConsoleRenderable,
    get_render_width,
    RenderableType,
    RenderResult,
)
from .text import Text
from ._tools import iter_last


@dataclass
class Column:

    label: Optional[RenderableType] = None
    width: Optional[int] = None
    ratio: Optional[int] = 1
    renderables: List[ConsoleRenderable] = []


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

        widths = []

        for index, column in enumerate(self.columns):
            if column.width is not None:
                widths.append((column.width, column.width))
            elif column.ratio is not None:
                widths.append((1, options.max_width))
            else:
                min_widths: List[int] = []
                max_widths: List[int] = []
                for renderable in column.renderables:
                    _min_width, _max_width = get_render_width(options, renderable)

                    min_widths.append(_min_width)
                    max_widths.append(_max_width)
                min_width = max(min_widths)
                max_width = max(max_widths)


if __name__ == "__main_":
    c = Console()
    table = Table("Column1", "Column2", "Column3")

    table.add_row("This column contains text", "More text", "Hello")
    from .markdown import Markdown

    table.add_row(Markdown("Hello, *World*!"), "More text", "Hello")

    c.print(table)
