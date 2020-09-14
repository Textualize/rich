from typing import cast, Tuple, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .console import (
        Console,
        ConsoleOptions,
        RenderableType,
        RenderResult,
    )
from .jupyter import JupyterMixin
from .measure import Measurement
from .style import Style
from .segment import Segment


PaddingDimensions = Union[int, Tuple[int], Tuple[int, int], Tuple[int, int, int, int]]


class Padding(JupyterMixin):
    """Draw space around content.

    Example:
        >>> print(Padding("Hello", (2, 4), style="on blue"))

    Args:
        renderable (RenderableType): String or other renderable.
        pad (Union[int, Tuple[int]]): Padding for top, right, bottom, and left borders.
            May be specified with 1, 2, or 4 integers (CSS style).
        style (Union[str, Style], optional): Style for padding characters. Defaults to "none".
        expand (bool, optional): Expand padding to fit available width. Defaults to True.
    """

    def __init__(
        self,
        renderable: "RenderableType",
        pad: "PaddingDimensions" = (0, 0, 0, 0),
        *,
        style: Union[str, Style] = "none",
        expand: bool = True,
    ):
        self.renderable = renderable
        self.top, self.right, self.bottom, self.left = self.unpack(pad)
        self.style = style
        self.expand = expand

    @classmethod
    def indent(cls, renderable: "RenderableType", level: int) -> "Padding":
        """Make padding instance to render an indent.

        Args:
            renderable (RenderableType): String or other renderable.
            level (int): Number of characters to indent.

        Returns:
            Padding: A Padding instance.
        """

        return Padding(renderable, pad=(0, 0, 0, level), expand=False)

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
        if len(pad) == 4:
            top, right, bottom, left = cast(Tuple[int, int, int, int], pad)
            return (top, right, bottom, left)
        raise ValueError(f"1, 2 or 4 integers required for padding; {len(pad)} given")

    def __repr__(self) -> str:
        return f"Padding({self.renderable!r}, ({self.top},{self.right},{self.bottom},{self.left}))"

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":

        style = console.get_style(self.style)
        if self.expand:
            width = options.max_width
        else:
            width = min(
                Measurement.get(console, self.renderable, options.max_width).maximum
                + self.left
                + self.right,
                options.max_width,
            )
        child_options = options.update(width=width - self.left - self.right)
        lines = console.render_lines(
            self.renderable, child_options, style=style, pad=False
        )
        lines = Segment.set_shape(lines, child_options.max_width, style=style)

        blank_line = Segment(" " * width + "\n", style)
        top = [blank_line] * self.top
        bottom = [blank_line] * self.bottom
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

    def __rich_measure__(self, console: "Console", max_width: int) -> "Measurement":
        extra_width = self.left + self.right
        if max_width - extra_width < 1:
            return Measurement(max_width, max_width)
        measure_min, measure_max = Measurement.get(
            console, self.renderable, max(0, max_width - extra_width)
        )
        measurement = Measurement(measure_min + extra_width, measure_max + extra_width)
        measurement = measurement.with_maximum(max_width)
        return measurement
