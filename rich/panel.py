from __future__ import annotations

from typing import Tuple

from .box import Box, SQUARE
from .console import Console, ConsoleOptions, RenderableType, RenderResult
from .text import Text
from .segment import Segment


class Panel:
    def __init__(
        self, *contents: RenderableType, box: Box = SQUARE, style: str = "none",
    ) -> None:
        """A console renderable that draws a border around its contents.
        
        Args:
            *contents (ConsoleRenderable): One or more console renderable objects.
            box (Box, optional): A Box instance that defines the look of the border.
                Defaults to box.SQUARE.
            style (str, optional): The style of the border. Defaults to "none".
        """
        self.contents: Tuple[RenderableType, ...] = contents
        self.box = box
        self.style = style

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:

        style = console.get_style(self.style)
        width = options.max_width
        child_options = options.copy()
        child_options.max_width = width - 2

        lines = console.render_lines(self.contents, child_options)
        box = self.box
        line_start = Segment(box.left, style)
        line_end = Segment(f"{box.right}\n", style)
        yield Segment(box.get_top(width), style)
        for line in lines:
            yield line_start
            yield from line
            yield line_end
        yield Segment(box.get_bottom(width), style)


if __name__ == "__main__":
    from .console import Console

    c = Console()

    c.print(Panel("Hello"))
