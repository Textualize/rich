from typing import TYPE_CHECKING

from typing_extensions import Literal
from .jupyter import JupyterMixin
from .measure import Measurement
from .segment import Segment
from .style import StyleType


if TYPE_CHECKING:
    from .console import Console, ConsoleOptions, RenderResult, RenderableType

AlignValues = Literal["left", "center", "right"]


class Align(JupyterMixin):
    """Align a renderable by adding spaces if necessary.

    Args:
        renderable (RenderableType): A console renderable.
        align (AlignValues): One of "left", "center", or "right""
        style (StyleType, optional): An optional style to apply to the renderable.

    Raises:
        ValueError: if ``align`` is not one of the expected values.
    """

    def __init__(
        self, renderable: "RenderableType", align: AlignValues, style: StyleType = None
    ) -> None:
        if align not in ("left", "center", "right"):
            raise ValueError(
                f'invalid value for align, expected "left", "center", "right" (not {align!r})'
            )
        self.renderable = renderable
        self.align = align
        self.style = style

    @classmethod
    def left(cls, renderable: "RenderableType", style: StyleType = None) -> "Align":
        """Align a renderable to the left."""
        return cls(renderable, "left", style=style)

    @classmethod
    def center(cls, renderable: "RenderableType", style: StyleType = None) -> "Align":
        """Align arenderable to the center."""
        return cls(renderable, "center", style=style)

    @classmethod
    def right(cls, renderable: "RenderableType", style: StyleType = None) -> "Align":
        """Align a renderable to the right."""
        return cls(renderable, "right", style=style)

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":

        align = self.align
        rendered = console.render(self.renderable, options)
        lines = list(Segment.split_lines(rendered))
        width, height = Segment.get_shape(lines)
        lines = Segment.set_shape(lines, width, height)
        new_line = Segment.line()
        excess_space = options.max_width - width

        def generate_segments():
            if excess_space <= 0:
                # Exact fit
                for line in lines:
                    yield from line
                    yield new_line

            elif align == "left":
                # Pad on the right
                pad = Segment(" " * excess_space)
                for line in lines:
                    yield from line
                    yield pad
                    yield new_line

            elif align == "center":
                # Pad left and right
                left = excess_space // 2
                pad = Segment(" " * left)
                pad_right = Segment(" " * (excess_space - left))
                for line in lines:
                    if left:
                        yield pad
                    yield from line
                    if pad_right:
                        yield pad_right
                    yield new_line

            elif align == "right":
                # Padding on left
                pad = Segment(" " * excess_space)
                for line in lines:
                    yield pad
                    yield from line
                    yield new_line

        iter_segments = generate_segments()
        if self.style is not None:
            style = console.get_style(self.style)
            iter_segments = Segment.apply_style(iter_segments, style)
        return iter_segments

    def __rich_measure__(self, console: "Console", max_width: int) -> Measurement:
        measurement = Measurement.get(console, self.renderable, max_width)
        return measurement


if __name__ == "__main__":  # pragma: no cover
    from rich.console import Console

    console = Console()

    for align in ["left", "center", "right"]:
        console.print(Align("Hello\nWorld!\nWorld!!!", align))  # type: ignore
