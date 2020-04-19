from math import sqrt
from functools import lru_cache
from typing import List, Sequence, Tuple

from .color_triplet import ColorTriplet


class Palette:
    """A palette of available colors."""

    def __init__(self, colors: Sequence[Tuple[int, int, int]]):
        self._colors = colors

    def __getitem__(self, number: int) -> ColorTriplet:
        return ColorTriplet(*self._colors[number])

    # This is somewhat inefficient and needs caching
    @lru_cache(maxsize=1024)
    def match(self, color: Tuple[int, int, int]) -> int:
        """Find a color from a palette that most closely matches a given color"""
        red1, green1, blue1 = color
        _sqrt = sqrt

        def get_color_distance(color: Tuple[int, int, int]) -> float:
            """Get the distance to a color."""
            red2, green2, blue2 = color
            red_mean = int((red1 + red2) / 2)
            red = red1 - red2
            green = green1 - green2
            blue = blue1 - blue2
            return _sqrt(
                (((512 + red_mean) * red * red) >> 8)
                + 4 * green * green
                + (((767 - red_mean) * blue * blue) >> 8)
            )

        min_index, _min_color = min(
            enumerate(self._colors), key=lambda _color: get_color_distance(_color[1]),
        )
        return min_index
