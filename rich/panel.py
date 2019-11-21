from __future__ import annotations

from typing import Tuple

from .console import Console, ConsoleOptions, ConsoleRenderable, RenderResult
from .text import Text
from .styled import Styled


class Border:
    def __init__(self, border: str) -> None:
        (
            self.top_left,
            self.top,
            self.top_right,
            _,
            self.left,
            _,
            self.right,
            _,
            self.bottom_left,
            self.bottom,
            self.bottom_right,
            *_,
        ) = border.lstrip()

    def __repr__(self) -> str:
        border_str = str(self).replace("\n", r"\n")
        return f'Border("{border_str}")'

    def __str__(self) -> str:
        return (
            f"{self.top_left}{self.top}{self.top_right}\n"
            f"{self.left} {self.right}\n"
            f"{self.bottom_left}{self.bottom}{self.bottom_right}\n"
        )

    def get_top(self, width) -> str:
        non_corner_width = width - 2
        return f"{self.top_left}{self.top * non_corner_width}{self.top_right}\n"

    def get_bottom(self, width) -> str:
        non_corner_width = width - 2
        return (
            f"{self.bottom_left}{self.bottom * non_corner_width}{self.bottom_right}\n"
        )


SQUARE_BORDER = Border(
    """
┌─┐
│ │
└─┘
"""
)

HEAVY_BORDER = Border(
    """
┏━┓
┃ ┃
┗━┛
"""
)

ROUND_BORDER = Border(
    """
╭─╮
│ │
╰─╯
"""
)

DOUBLE_BORDER = Border(
    """
╔═╗
║ ║
╚═╝
"""
)


class Panel:
    def __init__(
        self,
        *contents: ConsoleRenderable,
        border: Border = SQUARE_BORDER,
        style: str = "none",
    ) -> None:
        """A console renderable that draws a border around its contents.
        
        Args:
            *contents (ConsoleRenderable): One or more console renderable objects.
            border (Border, optional): A Border instance that defines the look of the border.
                Defaults to SQUARE_BORDER.
            style (str, optional): The style of the border. Defaults to "none".
        """
        self.contents: Tuple[ConsoleRenderable, ...] = contents
        self.border = border
        self.style = style

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:

        style = console.parse_style(self.style)
        width = options.max_width
        child_options = options.copy()
        child_options.max_width = width - 2

        lines = console.render_lines(self.contents, child_options)
        border = self.border
        line_start = Styled(border.left, style)
        line_end = Styled(f"{border.right}\n", style)
        yield Styled(border.get_top(width), style)
        for line in lines:
            yield line_start
            yield from line
            yield line_end
        yield Styled(border.get_bottom(width), style)
