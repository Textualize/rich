from __future__ import annotations

from typing import Union

from .console import (
    Console,
    ConsoleOptions,
    RenderableType,
    RenderResult,
    RenderWidth,
)
from .style import Style
from .text import Text
from .segment import Segment


class Padding:
    """Draw space around a console renderable."""

    def __init__(
        self,
        renderable: RenderableType,
        all_sides: int = None,
        top: int = None,
        right: int = None,
        bottom: int = None,
        left: int = None,
        style: Union[str, Style] = "none",
    ):
        if (
            all_sides is None
            and top is None
            and right is None
            and bottom is None
            and left is None
        ):
            all_sides = 1
        self.renderable = renderable
        self.top = self.right = self.bottom = self.left = 0
        if all_sides is not None:
            self.top = self.right = self.bottom = self.left = all_sides
        if top is not None:
            self.top = top
        if right is not None:
            self.right = right
        if bottom is not None:
            self.bottom = bottom
        if left is not None:
            self.left = left
        self.style = style

    def __repr__(self) -> str:
        return f"<padding {self.renderable!r} {self.top} {self.right} {self.bottom} {self.left}>"

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:

        style = console.get_style(self.style)
        width = options.max_width
        child_options = options.with_width(width - self.left - self.right)
        lines = console.render_lines(self.renderable, child_options)
        lines = Segment.set_shape(lines, child_options.max_width)

        row = Segment(" " * width + "\n", style)
        left = Segment(" " * self.left, style)
        right = Segment(" " * self.right + "\n", style)
        for _ in range(self.top):
            yield row
        for line in lines:
            if self.left:
                yield left
            yield from line
            if self.right:
                yield right
        for _ in range(self.bottom):
            yield row

    def __console_width__(self, max_width: int) -> RenderWidth:
        extra_width = self.left + self.right
        width = (
            RenderWidth.get(self.renderable, max_width - extra_width).maximum
            + extra_width
        )
        return RenderWidth(width, width)

