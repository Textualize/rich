from typing import Iterable, Optional, Tuple

from .console import Console, ConsoleOptions, RenderableType, RenderResult
from .control import Control
from .segment import Segment
from .style import StyleType
from ._loop import loop_last


class LiveRender:
    def __init__(self, renderable: RenderableType, style: StyleType = "") -> None:
        self.renderable = renderable
        self.style = style
        self._shape: Optional[Tuple[int, int]] = None

    def set_renderable(self, renderable: RenderableType) -> None:
        self.renderable = renderable

    def position_cursor(self) -> Control:
        """Get control codes to move cursor to beggining of live render.

        Returns:
            str: String containing control codes.
        """
        if self._shape is not None:
            _, height = self._shape
            if height > 1:
                return Control(f"\r\x1b[{height - 1}A\x1b[2K")
            else:
                return Control("\r\x1b[2K")
        return Control("")

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        style = console.get_style(self.style)
        lines = console.render_lines(self.renderable, options, style, pad=False)

        shape = Segment.get_shape(lines)
        if self._shape is None:
            self._shape = shape
        else:
            width1, height1 = shape
            width2, height2 = self._shape
            self._shape = (
                max(width1, min(options.max_width, width2)),
                max(height1, height2),
            )

        width, height = self._shape
        lines = Segment.set_shape(lines, width, height)
        for last, line in loop_last(lines):
            yield from line
            if not last:
                yield Segment.line()
