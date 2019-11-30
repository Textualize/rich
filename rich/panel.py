from __future__ import annotations

from typing import Tuple, Union

from .box import Box, SQUARE
from .console import (
    Console,
    ConsoleOptions,
    ConsoleRenderable,
    RenderableType,
    RenderResult,
    RenderWidth,
)
from .style import Style
from .text import Text
from .segment import Segment


class Panel:
    def __init__(
        self,
        renderable: Union[str, ConsoleRenderable],
        box: Box = SQUARE,
        fit: bool = False,
        style: Union[str, Style] = "none",
    ) -> None:
        """A console renderable that draws a border around its contents.
        
        Args:
            renderable (ConsoleRenderable): A console renderable objects.
            box (Box, optional): A Box instance that defines the look of the border.
                Defaults to box.SQUARE.
            fit (bool, optional): If True the panel will attempt to fit its contents,
                otherwise it will expand to the available width. Defaults to False.
            style (str, optional): The style of the border. Defaults to "none".
        """
        self.renderable = (
            Text(renderable) if isinstance(renderable, str) else renderable
        )
        self.box = box
        self.fit = fit
        self.style = style

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:

        style = console.get_style(self.style)
        width = options.max_width

        if self.fit:
            child_width = RenderWidth.get(self.renderable, width - 2).maximum
        else:
            child_width = width - 2

        width = child_width + 2
        child_options = options.with_width(child_width)
        lines = console.render_lines(self.renderable, child_options)

        box = self.box
        line_start = Segment(box.mid_left, style)
        line_end = Segment(f"{box.mid_right}\n", style)
        yield Segment(box.get_top(width), style)
        for line in lines:
            yield line_start
            yield from line
            yield line_end
        yield Segment(box.get_bottom(width), style)


if __name__ == "__main__":
    from .console import Console

    c = Console()

    from .padding import Padding
    from .box import ROUNDED

    p = Panel(Panel(Padding("Hello World! ", 2), box=ROUNDED, fit=True))

    print(p)
    c.print(p)

