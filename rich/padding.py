from __future__ import annotations

from typing import Tuple, Union

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


PaddingType = Union[int, Tuple[int], Tuple[int, int], Tuple[int, int, int, int]]


class Padding:
    """Draw space around a console renderable."""

    def __init__(
        self,
        renderable: RenderableType,
        pad: PaddingType,
        *,
        style: Union[str, Style] = "none",
    ):
        self.renderable = renderable
        self.top, self.right, self.bottom, self.left = self.unpack(pad)
        self.style = style

    @classmethod
    def unpack(cls, pad: Union[int, Tuple[int, ...]]) -> Tuple[int, int, int, int]:
        """Unpack padding specified in CSS style."""
        if isinstance(pad, int):
            return (pad, pad, pad, pad)
        if len(pad) == 1:
            _pad = pad[0]
            return (_pad, _pad, _pad, _pad)
        if len(pad) == 2:
            pad_top, pad_right = pad
            return (pad_top, pad_right, pad_top, pad_right)
        if len(pad) == 3:
            raise ValueError(
                f"1, 2 or 4 integers required for padding; {len(pad)} given"
            )
        if len(pad) == 4:
            top, right, bottom, left = pad
            return (top, right, bottom, left)
        raise ValueError(f"1, 2 or 4 integers required for padding; {len(pad)} given")

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

