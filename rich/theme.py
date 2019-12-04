from typing import List, Tuple

from .color_triplet import ColorTriplet
from .palette import Palette

_ColorTuple = Tuple[int, int, int]


class Theme:
    """A terminal theme."""

    def __init__(
        self, background: _ColorTuple, foreground: _ColorTuple, ansi: List[_ColorTuple]
    ) -> None:
        self.background_color = ColorTriplet(*background)
        self.foreground_color = ColorTriplet(*foreground)
        self.ansi_colors = Palette(ansi)
