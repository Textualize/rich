from typing import Optional, Union

from .box import get_safe_box, Box, SQUARE, ROUNDED

from .console import (
    Console,
    ConsoleOptions,
    RenderableType,
    RenderResult,
    Measurement,
)
from .jupyter import JupyterMixin
from .padding import Padding, PaddingDimensions
from .style import Style, StyleType
from .text import Text
from .segment import Segment


class Panel(JupyterMixin):
    """A console renderable that draws a border around its contents.
    
    Example::
        >>> console.print(Panel("Hello, World!"))

    Args:
        renderable (RenderableType): A console renderable object.
        box (Box, optional): A Box instance that defines the look of the border (see :ref:`appendix_box`.
            Defaults to box.ROUNDED.
        safe_box (bool, optional): Disable box characters that don't display on windows legacy terminal with *raster* fonts. Defaults to True.
        expand (bool, optional): If True the panel will stretch to fill the console 
            width, otherwise it will be sized to fit the contents. Defaults to True.
        style (str, optional): The style of the panel (border and contents). Defaults to "none".
        border_style (str, optional): The style of the border. Defaults to "none".
        width (Optional[int], optional): Optional width of panel. Defaults to None to auto-detect.
        padding (Optional[PaddingDimensions]): Optional padding around renderable. Defaults to 0.
    """

    def __init__(
        self,
        renderable: RenderableType,
        box: Box = ROUNDED,
        *,
        safe_box: Optional[bool] = None,
        expand: bool = True,
        style: StyleType = "none",
        border_style: StyleType = "none",
        width: Optional[int] = None,
        padding: PaddingDimensions = 0,
    ) -> None:
        self.renderable = renderable
        self.box = box
        self.safe_box = safe_box
        self.expand = expand
        self.style = style
        self.border_style = border_style
        self.width = width
        self.padding = padding

    @classmethod
    def fit(
        cls,
        renderable: RenderableType,
        box: Box = ROUNDED,
        *,
        safe_box: Optional[bool] = None,
        style: StyleType = "none",
        border_style: StyleType = "none",
        width: Optional[int] = None,
        padding: PaddingDimensions = 0,
    ):
        """An alternative constructor that sets expand=False."""
        return cls(
            renderable,
            box,
            safe_box=safe_box,
            style=style,
            border_style=border_style,
            width=width,
            padding=padding,
            expand=False,
        )

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        _padding = Padding.unpack(self.padding)
        renderable = (
            Padding(self.renderable, _padding) if any(_padding) else self.renderable
        )
        style = console.get_style(self.style)
        border_style = style + console.get_style(self.border_style)
        width = (
            options.max_width
            if self.width is None
            else min(self.width, options.max_width)
        )
        child_width = (
            width - 2
            if self.expand
            else Measurement.get(console, renderable, width - 2).maximum
        )
        width = child_width + 2
        child_options = options.update(width=child_width)
        lines = console.render_lines(renderable, child_options, style=style)
        safe_box: bool = console.safe_box if self.safe_box is None else self.safe_box  # type: ignore

        box = get_safe_box(self.box, console.legacy_windows) if safe_box else self.box
        line_start = Segment(box.mid_left, border_style)
        line_end = Segment(f"{box.mid_right}", border_style)
        new_line = Segment.line()
        yield Segment(box.get_top([width - 2]), border_style)
        yield new_line
        for line in lines:
            yield line_start
            yield from line
            yield line_end
            yield new_line
        yield Segment(box.get_bottom([width - 2]), border_style)
        yield new_line

    def __rich_measure__(self, console: "Console", max_width: int) -> Measurement:
        width = Measurement.get(console, self.renderable, max_width - 2).maximum + 2
        return Measurement(width, width)


if __name__ == "__main__":  # pragma: no cover
    from .console import Console

    c = Console()

    from .padding import Padding
    from .box import ROUNDED

    p = Panel(
        Panel.fit(
            Text.from_markup("[bold magenta]Hello World!"),
            box=ROUNDED,
            safe_box=True,
            style="on red",
        ),
        border_style="on blue",
    )

    print(p)
    c.print(p)
