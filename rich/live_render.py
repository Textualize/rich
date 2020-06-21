from typing import Optional, Tuple

from .console import Console, ConsoleOptions, RenderableType, RenderResult
from .control import Control
from .segment import Segment
from .style import StyleType
from ._loop import loop_last


class LiveRender:
    """Creates a renderable that may be updated.

    Args:
        renderable (RenderableType): Any renderable object.
        style (StyleType, optional): An optional style to apply to the renderable. Defaults to "".
    """

    def __init__(self, renderable: RenderableType, style: StyleType = "") -> None:
        self.renderable = renderable
        self.style = style
        self._shape: Optional[Tuple[int, int]] = None

    def set_renderable(self, renderable: RenderableType) -> None:
        """Set a new renderable.

        Args:
            renderable (RenderableType): Any renderable object, including str.
        """
        self.renderable = renderable

    def position_cursor(self) -> Control:
        """Get control codes to move cursor to beggining of live render.

        Returns:
            Control: A control instance that may be printed.
        """
        if self._shape is not None:
            _, height = self._shape
            return Control("\r\x1b[2K" + "\x1b[1A\x1b[2K" * (height - 1))
        return Control("")

    def restore_cursor(self) -> Control:
        """Get control codes to clear the render and restore the cursor to its previous position.

        Returns:
            Control: A Control instance that may be printed.
        """
        if self._shape is not None:
            _, height = self._shape
            return Control("\r" + "\x1b[1A\x1b[2K" * height)
        return Control("")

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        style = console.get_style(self.style)
        lines = console.render_lines(self.renderable, options, style=style, pad=False)

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
