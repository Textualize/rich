from __future__ import annotations

import re
from dataclasses import dataclass
from enum import IntEnum
from functools import lru_cache
from math import sqrt
from typing import Iterable, List, NamedTuple, Sequence, Tuple, Optional


STANDARD_COLORS_NAMES = {
    "black": 0,
    "red": 1,
    "green": 2,
    "yellow": 3,
    "blue": 4,
    "magenta": 5,
    "cyan": 6,
    "white": 7,
}

STANDARD_COLORS = (
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (255, 255, 0),
    (0, 0, 255),
    (255, 0, 255),
    (0, 255, 255),
    (255, 255, 255),
)

EIGHT_BIT_COLORS = [
    (0, 0, 0),
    (128, 0, 0),
    (0, 128, 0),
    (128, 128, 0),
    (0, 0, 128),
    (128, 0, 128),
    (0, 128, 128),
    (192, 192, 192),
    (128, 128, 128),
    (255, 0, 0),
    (0, 255, 0),
    (255, 255, 0),
    (0, 0, 255),
    (255, 0, 255),
    (0, 255, 255),
    (255, 255, 255),
    (0, 0, 0),
    (0, 0, 95),
    (0, 0, 135),
    (0, 0, 175),
    (0, 0, 215),
    (0, 0, 255),
    (0, 95, 0),
    (0, 95, 95),
    (0, 95, 135),
    (0, 95, 175),
    (0, 95, 215),
    (0, 95, 255),
    (0, 135, 0),
    (0, 135, 95),
    (0, 135, 135),
    (0, 135, 175),
    (0, 135, 215),
    (0, 135, 255),
    (0, 175, 0),
    (0, 175, 95),
    (0, 175, 135),
    (0, 175, 175),
    (0, 175, 215),
    (0, 175, 255),
    (0, 215, 0),
    (0, 215, 95),
    (0, 215, 135),
    (0, 215, 175),
    (0, 215, 215),
    (0, 215, 255),
    (0, 255, 0),
    (0, 255, 95),
    (0, 255, 135),
    (0, 255, 175),
    (0, 255, 215),
    (0, 255, 255),
    (95, 0, 0),
    (95, 0, 95),
    (95, 0, 135),
    (95, 0, 175),
    (95, 0, 215),
    (95, 0, 255),
    (95, 95, 0),
    (95, 95, 95),
    (95, 95, 135),
    (95, 95, 175),
    (95, 95, 215),
    (95, 95, 255),
    (95, 135, 0),
    (95, 135, 95),
    (95, 135, 135),
    (95, 135, 175),
    (95, 135, 215),
    (95, 135, 255),
    (95, 175, 0),
    (95, 175, 95),
    (95, 175, 135),
    (95, 175, 175),
    (95, 175, 215),
    (95, 175, 255),
    (95, 215, 0),
    (95, 215, 95),
    (95, 215, 135),
    (95, 215, 175),
    (95, 215, 215),
    (95, 215, 255),
    (95, 255, 0),
    (95, 255, 95),
    (95, 255, 135),
    (95, 255, 175),
    (95, 255, 215),
    (95, 255, 255),
    (135, 0, 0),
    (135, 0, 95),
    (135, 0, 135),
    (135, 0, 175),
    (135, 0, 215),
    (135, 0, 255),
    (135, 95, 0),
    (135, 95, 95),
    (135, 95, 135),
    (135, 95, 175),
    (135, 95, 215),
    (135, 95, 255),
    (135, 135, 0),
    (135, 135, 95),
    (135, 135, 135),
    (135, 135, 175),
    (135, 135, 215),
    (135, 135, 255),
    (135, 175, 0),
    (135, 175, 95),
    (135, 175, 135),
    (135, 175, 175),
    (135, 175, 215),
    (135, 175, 255),
    (135, 215, 0),
    (135, 215, 95),
    (135, 215, 135),
    (135, 215, 175),
    (135, 215, 215),
    (135, 215, 255),
    (135, 255, 0),
    (135, 255, 95),
    (135, 255, 135),
    (135, 255, 175),
    (135, 255, 215),
    (135, 255, 255),
    (175, 0, 0),
    (175, 0, 95),
    (175, 0, 135),
    (175, 0, 175),
    (175, 0, 215),
    (175, 0, 255),
    (175, 95, 0),
    (175, 95, 95),
    (175, 95, 135),
    (175, 95, 175),
    (175, 95, 215),
    (175, 95, 255),
    (175, 135, 0),
    (175, 135, 95),
    (175, 135, 135),
    (175, 135, 175),
    (175, 135, 215),
    (175, 135, 255),
    (175, 175, 0),
    (175, 175, 95),
    (175, 175, 135),
    (175, 175, 175),
    (175, 175, 215),
    (175, 175, 255),
    (175, 215, 0),
    (175, 215, 95),
    (175, 215, 135),
    (175, 215, 175),
    (175, 215, 215),
    (175, 215, 255),
    (175, 255, 0),
    (175, 255, 95),
    (175, 255, 135),
    (175, 255, 175),
    (175, 255, 215),
    (175, 255, 255),
    (215, 0, 0),
    (215, 0, 95),
    (215, 0, 135),
    (215, 0, 175),
    (215, 0, 215),
    (215, 0, 255),
    (215, 95, 0),
    (215, 95, 95),
    (215, 95, 135),
    (215, 95, 175),
    (215, 95, 215),
    (215, 95, 255),
    (215, 135, 0),
    (215, 135, 95),
    (215, 135, 135),
    (215, 135, 175),
    (215, 135, 215),
    (215, 135, 255),
    (215, 175, 0),
    (215, 175, 95),
    (215, 175, 135),
    (215, 175, 175),
    (215, 175, 215),
    (215, 175, 255),
    (215, 215, 0),
    (215, 215, 95),
    (215, 215, 135),
    (215, 215, 175),
    (215, 215, 215),
    (215, 215, 255),
    (215, 255, 0),
    (215, 255, 95),
    (215, 255, 135),
    (215, 255, 175),
    (215, 255, 215),
    (215, 255, 255),
    (255, 0, 0),
    (255, 0, 95),
    (255, 0, 135),
    (255, 0, 175),
    (255, 0, 215),
    (255, 0, 255),
    (255, 95, 0),
    (255, 95, 95),
    (255, 95, 135),
    (255, 95, 175),
    (255, 95, 215),
    (255, 95, 255),
    (255, 135, 0),
    (255, 135, 95),
    (255, 135, 135),
    (255, 135, 175),
    (255, 135, 215),
    (255, 135, 255),
    (255, 175, 0),
    (255, 175, 95),
    (255, 175, 135),
    (255, 175, 175),
    (255, 175, 215),
    (255, 175, 255),
    (255, 215, 0),
    (255, 215, 95),
    (255, 215, 135),
    (255, 215, 175),
    (255, 215, 215),
    (255, 215, 255),
    (255, 255, 0),
    (255, 255, 95),
    (255, 255, 135),
    (255, 255, 175),
    (255, 255, 215),
    (255, 255, 255),
    (8, 8, 8),
    (18, 18, 18),
    (28, 28, 28),
    (38, 38, 38),
    (48, 48, 48),
    (58, 58, 58),
    (68, 68, 68),
    (78, 78, 78),
    (88, 88, 88),
    (98, 98, 98),
    (108, 108, 108),
    (118, 118, 118),
    (128, 128, 128),
    (138, 138, 138),
    (148, 148, 148),
    (158, 158, 158),
    (168, 168, 168),
    (178, 178, 178),
    (188, 188, 188),
    (198, 198, 198),
    (208, 208, 208),
    (218, 218, 218),
    (228, 228, 228),
    (238, 238, 238),
]


class Palette:
    def __init__(self, colors: Sequence[Tuple[int, int, int]]):
        self._colors = colors

    def __getitem__(self, number: int) -> Tuple[int, int, int]:
        return self._color[number]

    @lru_cache(maxsize=1000)
    def match(self, color: ColorTriplet) -> int:
        """Find a color from a palette that most closely matches a given color"""
        red1, green1, blue1 = color
        _sqrt = sqrt

        def get_color_distance(color: Tuple[int, int, int]) -> float:
            """Get the distance to a color."""
            red2, green2, blue2 = color
            red_mean = int((red1 + red2) / 2)
            red = int(red1 - red2)
            green = int(green1 - green2)
            blue = int(blue1 - blue2)
            return _sqrt(
                (((512 + red_mean) * red * red) >> 8)
                + 4 * green * green
                + (((767 - red_mean) * blue * blue) >> 8)
            )

        # def get_color_distance(color: Tuple[int, int, int]) -> float:
        #     """Get the distance to a color."""
        #     red2, green2, blue2 = color
        #     distance = _sqrt(
        #         (red2 - red1) * (red2 - red1)
        #         + (green2 - green1) * (green2 - green1)
        #         + (blue2 - blue1) * (blue2 - blue1)
        #     )
        #     return distance

        min_index, _min_color = min(
            enumerate(self._colors), key=lambda _color: get_color_distance(_color[1]),
        )
        return min_index


STANDARD_PALETTE = Palette(STANDARD_COLORS)
EIGHT_BIT_PALETTE = Palette(EIGHT_BIT_COLORS)


class ColorSystem(IntEnum):
    """One of the 3 color system supported by terminals."""

    NONE = 0
    STANDARD = 1
    EIGHT_BIT = 2
    TRUECOLOR = 3


class ColorType(IntEnum):
    """Type of color stored in Color class."""

    DEFAULT = 0
    STANDARD = 1
    EIGHT_BIT = 2
    TRUECOLOR = 3


class ColorTriplet(NamedTuple):
    """The red, green, and blue components of a color."""

    red: int
    green: int
    blue: int

    @property
    def hex(self) -> str:
        """get the color triplet as 6 chars of hex."""
        red, green, blue = self
        return f"{red:02X}{green:02X}{blue:02X}"


class ColorParseError(Exception):
    """The color could not be parsed."""


RE_COLOR = re.compile(
    r"""^
\#([0-9a-f]{6})$|
([0-9]{1,3})$|
rgb\(([\d\s,]+)\)$
""",
    re.VERBOSE,
)


class Color(NamedTuple):
    """Terminal color definition."""

    name: str
    type: ColorType
    number: Optional[int] = None
    triplet: Optional[ColorTriplet] = None

    def __str__(self):
        """Render the color to the terminal."""
        attrs = self.get_ansi_codes(foreground=True)
        return (
            f"<color {self.name!r} ({self.type.name.lower()})>"
            f"\x1b[{';'.join(attrs)}m ⬤ \x1b[0m"
        )

    def __repr__(self) -> str:
        return f"<color {self.name!r} ({self.type.name.lower()})>"

    @property
    def system(self) -> ColorSystem:
        if self.type == ColorType.DEFAULT:
            return ColorSystem.STANDARD
        return ColorSystem(int(self.type))

    @classmethod
    def from_triplet(cls, triplet: ColorTriplet) -> Color:
        """Create a truecolor RGB color from a triplet of values.
        
        Args:
            triplet (ColorTriplet): A color triplet containing red, green and blue components.
        
        Returns:
            Color: A new color object.
        """
        return cls(name=f"#{triplet.hex}", type=ColorType.TRUECOLOR, triplet=triplet)

    @classmethod
    def default(cls) -> Color:
        """Get a Color instance representing the default color.
        
        Returns:
            Color: Default color,.
        """
        return cls(name="default", type=ColorType.DEFAULT)

    @classmethod
    @lru_cache(maxsize=1000)
    def parse(cls, color: str) -> Optional[Color]:
        """Parse a color definition."""
        color = color.lower().strip()

        if color == "default":
            return cls(color, type=ColorType.DEFAULT)

        standard_color_number = STANDARD_COLORS_NAMES.get(color)
        if standard_color_number is not None:
            return cls(color, type=ColorType.STANDARD, number=standard_color_number)

        color_match = RE_COLOR.match(color)
        if color_match is None:
            return None

        color_24, color_8, color_rgb = color_match.groups()
        if color_8:
            return cls(color, ColorType.EIGHT_BIT, number=int(color_8))

        elif color_24:
            triplet = ColorTriplet(
                int(color_24[0:2], 16), int(color_24[2:4], 16), int(color_24[4:6], 16)
            )
            if not all(component <= 255 for component in triplet):
                raise ColorParseError(f"color components must be <= 255 in {color!r}")
            return cls(color, ColorType.TRUECOLOR, triplet=triplet)

        else:  #  color_rgb:
            components = color_rgb.split(",")
            if len(components) != 3:
                raise ColorParseError(f"expected three components in {color!r}")
            red, green, blue = components
            triplet = ColorTriplet(int(red), int(green), int(blue))
            if not all(component <= 255 for component in triplet):
                raise ColorParseError(f"color components must be <= 255 in {color!r}")
            return cls(color, ColorType.TRUECOLOR, triplet=triplet)

    def get_ansi_codes(self, foreground: bool = True) -> List[str]:
        """Get the ANSI escape codes for this color."""
        _type = self.type
        if _type == ColorType.DEFAULT:
            return ["39" if foreground else "49"]

        elif _type == ColorType.STANDARD:
            assert self.number is not None
            return [str(30 + self.number if foreground else 40 + self.number)]

        elif _type == ColorType.EIGHT_BIT:
            assert self.number is not None
            return ["38" if foreground else "48", "5", str(self.number)]

        else:  # self.standard == ColorStandard.TRUECOLOR:
            assert self.triplet is not None
            red, green, blue = self.triplet
            return ["38" if foreground else "48", "2", str(red), str(green), str(blue)]

    def downgrade(self, system: ColorSystem) -> Color:
        """Downgrade a color system to a system with fewer colors."""
        if system >= self.system:
            return self

        # Convert to 8-bit color from truecolor color
        if system == ColorSystem.EIGHT_BIT and self.system == ColorSystem.TRUECOLOR:

            color_number = EIGHT_BIT_PALETTE.match(self.triplet)
            return Color(self.name, ColorType.EIGHT_BIT, number=color_number)

            # assert self.triplet is not None
            # red, green, blue = self.triplet
            # if red == green and green == blue:
            #     if red < 8:
            #         color_number = 16
            #     elif red > 248:
            #         color_number = 231
            #     else:
            #         color_number = round(((red - 8) / 247.0) * 24) + 232
            #     return Color(self.name, ColorType.EIGHT_BIT, number=color_number)
            # ansi_red = 36 * round(red / 255.0 * 5.0)
            # ansi_green = 6 * round(green / 255.0 * 5.0)
            # ansi_blue = round(blue / 255.0 * 5.0)
            # color_number = 16 + ansi_red + ansi_green + ansi_blue
            # return Color(self.name, ColorType.EIGHT_BIT, number=color_number)

        # Convert to standard from truecolor or 8-bit
        elif system == ColorSystem.STANDARD:
            if self.system == ColorSystem.TRUECOLOR:
                assert self.triplet is not None
                triplet = self.triplet
            else:  # self.system == ColorSystem.EIGHT_BUT
                assert self.number is not None
                triplet = ColorTriplet(*EIGHT_BIT_PALETTE[self.number])

            color_number = STANDARD_PALETTE.match(triplet)
            return Color(self.name, ColorType.STANDARD, number=color_number)

        return self


def parse_rgb_hex(hex_color: str) -> ColorTriplet:
    """Parse six hex characters in to RGB triplet."""
    color = ColorTriplet(
        int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    )
    return color


def blend_rgb(
    color1: ColorTriplet, color2: ColorTriplet, cross_fade: float = 0.5
) -> ColorTriplet:
    """Blend one RGB color in to another."""
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    new_color = ColorTriplet(
        int(r1 + (r2 - r1) * cross_fade),
        int(g1 + (g2 - g1) * cross_fade),
        int(b1 + (b2 - b1) * cross_fade),
    )
    return new_color


if __name__ == "__main__":
    print(Color.parse("default"))
    print(Color.parse("red"))
    print(Color.parse("#ff0000"))
    print(Color.parse("0"))
    print(Color.parse("100"))
    print(Color.parse("rgb(  12, 130, 200)"))

    color = Color.parse("#339a2e")
    print(color)
    print(color.downgrade(ColorSystem.EIGHT_BIT))
    print(color.downgrade(ColorSystem.STANDARD))
    import sys

    # sys.stdout.write(Color.parse("#00ffff").foreground_sequence + "Hello")
