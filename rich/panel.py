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
        expand: bool = True,
        style: Union[str, Style] = "none",
    ) -> None:
        """A console renderable that draws a border around its contents.
        
        Args:
            renderable (ConsoleRenderable): A console renderable objects.
            box (Box, optional): A Box instance that defines the look of the border.
                Defaults to box.SQUARE.
            expand (bool, optional): If True the panel will stretch to fill the console 
                width, otherwise it will be sized to fit the contents. Defaults to False.
            style (str, optional): The style of the border. Defaults to "none".
        """
        self.renderable = (
            Text.from_markup(renderable) if isinstance(renderable, str) else renderable
        )
        self.box = box
        self.expand = expand
        self.style = style

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:

        style = console.get_style(self.style)
        width = options.max_width

        if self.expand:
            child_width = width - 2
        else:
            print(self.renderable)
            child_width = RenderWidth.get(self.renderable, width - 2).maximum
            print(child_width)

        width = child_width + 2
        child_options = options.update(width=child_width)
        lines = console.render_lines(self.renderable, child_options)

        box = self.box
        line_start = Segment(box.mid_left, style)
        line_end = Segment(f"{box.mid_right}\n", style)
        yield Segment(box.get_top([width - 2]), style)
        for line in lines:
            yield line_start
            yield from line
            yield line_end
        yield Segment(box.get_bottom([width - 2]), style)

    def __console_width__(self, max_width: int) -> RenderWidth:
        if self.expand:
            return RenderWidth(max_width, max_width)
        width = RenderWidth.get(self.renderable, max_width - 2).maximum + 2
        return RenderWidth.get(width, width)


if __name__ == "__main__":
    from .console import Console

    c = Console()

    from .padding import Padding
    from .box import ROUNDED

    p = Panel(
        Panel(
            Padding(Text.from_markup("[bold magenta]Hello World!"), (1, 8)),
            box=ROUNDED,
            expand=False,
        )
    )

    print(p)
    c.print(p)
