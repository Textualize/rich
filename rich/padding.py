from typing import cast, Tuple, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .console import (
        Console,
        ConsoleOptions,
        RenderableType,
        RenderResult,
    )
from ._render_width import RenderWidth
from .style import Style
from .text import Text
from .segment import Segment


PaddingDimensions = Union[int, Tuple[int], Tuple[int, int], Tuple[int, int, int, int]]


class Padding:
    """Draw space around a console renderable."""

    def __init__(
        self,
        renderable: "RenderableType",
        pad: "PaddingDimensions",
        *,
        style: Union[str, Style] = "none",
    ):
        self.renderable = renderable
        self.top, self.right, self.bottom, self.left = self.unpack(pad)
        self.style = style

    @staticmethod
    def unpack(pad: "PaddingDimensions") -> Tuple[int, int, int, int]:
        """Unpack padding specified in CSS style."""
        if isinstance(pad, int):
            return (pad, pad, pad, pad)
        if len(pad) == 1:
            _pad = pad[0]
            return (_pad, _pad, _pad, _pad)
        if len(pad) == 2:
            pad_top, pad_right = cast(Tuple[int, int], pad)
            return (pad_top, pad_right, pad_top, pad_right)
        if len(pad) == 3:
            raise ValueError(
                f"1, 2 or 4 integers required for padding; {len(pad)} given"
            )
        if len(pad) == 4:
            top, right, bottom, left = cast(Tuple[int, int, int, int], pad)
            return (top, right, bottom, left)
        raise ValueError(f"1, 2 or 4 integers required for padding; {len(pad)} given")

    def __repr__(self) -> str:
        return f"Padding({self.renderable!r}, ({self.top},{self.right},{self.bottom},{self.left}))"

    def __console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":

        style = console.get_style(self.style)
        width = options.max_width
        child_options = options.update(width=width - self.left - self.right)
        lines = console.render_lines(self.renderable, child_options, style=style)
        lines = Segment.set_shape(lines, child_options.max_width, style=style)

        blank_line = Segment(" " * width + "\n", style)
        top = [blank_line] * self.top
        bottom = [blank_line] * self.top
        left = Segment(" " * self.left, style) if self.left else None
        right = Segment(" " * self.right, style) if self.right else None
        new_line = Segment.line()
        yield from top
        for line in lines:
            if left is not None:
                yield left
            yield from line
            if right is not None:
                yield right
            yield new_line
        yield from bottom

    def __console_width__(self, max_width: int) -> "RenderWidth":
        extra_width = self.left + self.right
        min_width, max_width = RenderWidth.get(
            self.renderable, max(1, max_width - extra_width)
        )
        render_width = RenderWidth(min_width + extra_width, max_width + extra_width)
        return render_width

