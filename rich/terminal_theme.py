from typing import List, Tuple

from .color_triplet import ColorTriplet
from .palette import Palette

_ColorTuple = Tuple[int, int, int]


class TerminalTheme:
    """A color theme used when exporting console content."""

    def __init__(
        self,
        background: _ColorTuple,
        foreground: _ColorTuple,
        normal: List[_ColorTuple],
        bright: List[_ColorTuple] = None,
    ) -> None:
        self.background_color = ColorTriplet(*background)
        self.foreground_color = ColorTriplet(*foreground)
        self.ansi_colors = Palette(normal + (bright or normal))


DEFAULT_TERMINAL_THEME = TerminalTheme(
    (255, 255, 255),
    (0, 0, 0),
    [
        (0, 0, 0),
        (128, 0, 0),
        (0, 128, 0),
        (128, 128, 0),
        (0, 0, 128),
        (128, 0, 128),
        (0, 128, 128),
        (192, 192, 192),
    ],
    [
        (128, 128, 128),
        (255, 0, 0),
        (0, 255, 0),
        (255, 255, 0),
        (0, 0, 255),
        (255, 0, 255),
        (0, 255, 255),
        (255, 255, 255),
    ],
)
