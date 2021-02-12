from .console import Console, ConsoleOptions, RenderResult, RenderableType
from .segment import Segment
from .style import StyleType
from ._loop import loop_last


class Screen:
    def __init__(self, renderable: RenderableType, style: StyleType = None) -> None:
        """A renderable that fills the terminal screen.

        Args:
            renderable (RenderableType): Child renderable.
            style (StyleType, optional): Optional background style. Defaults to None.
        """
        self.renderable = renderable
        self.style = style

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        width, height = console.size
        style = console.get_style(self.style) if self.style else None
        render_options = options.update(width=width, height=height)
        lines = console.render_lines(
            self.renderable, render_options, style=style, pad=True
        )
        lines = Segment.set_shape(lines, width, height, style=style)
        new_line = Segment.line()
        for last, line in loop_last(lines):
            yield from line
            if not last:
                yield new_line
