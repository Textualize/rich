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

    Raises:
        ValueError: if ``align`` is not one of the expected values.
    """

    def __init__(self, renderable: "RenderableType", align: AlignValues) -> None:
        if align not in ("left", "center", "right"):
            raise ValueError(
                f'invalid value for align, expected "left", "center", "right" (not {align!r})'
            )
        self.renderable = renderable
        self.align = align

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":

        align = self.align
        if align == "left":
            yield self.renderable
            return

        rendered = console.render(self.renderable, options)
        lines = list(Segment.split_lines(rendered))
        width, height = Segment.get_shape(lines)
        lines = Segment.set_shape(lines, width, height)
        new_line = Segment.line()

        if width >= options.max_width:
            yield self.renderable

        elif align == "center":
            # Pad left and right
            excess_space = options.max_width - width
            left = excess_space // 2
            pad = Segment(" " * left)
            for line in lines:
                if left:
                    yield pad
                yield from line
                yield new_line
        elif align == "right":
            # Padding on left
            excess_space = options.max_width - width
            pad = Segment(" " * excess_space)

            for line in lines:
                yield pad
                yield from line
                yield new_line


if __name__ == "__main__":  # pragma: no cover
    from rich.console import Console

    console = Console()

    for align in ["left", "center", "right"]:
        console.print(Align("Hello\nWorld!\nWorld!!!", align))  # type: ignore
