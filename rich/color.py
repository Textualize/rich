from __future__ import annotations

import re
from colorsys import rgb_to_hls
from dataclasses import dataclass
from enum import IntEnum
from functools import lru_cache
from math import sqrt
from typing import Iterable, List, NamedTuple, Optional, Sequence, Tuple
from ._palette import STANDARD_PALETTE, EIGHT_BIT_PALETTE


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
        return f"{red:02x}{green:02x}{blue:02x}"


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
        """Get the native color system for this color."""
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
            Color: Default color.
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
                raise ColorParseError(
                    f"color components must be <= 0xff (255) in {color!r}"
                )
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

    @lru_cache(maxsize=1000)
    def get_ansi_codes(self, foreground: bool = True) -> List[str]:
        """Get the ANSI escape codes for this color."""
        _type = self.type
        if _type == ColorType.DEFAULT:
            return ["39" if foreground else "49"]

        elif _type == ColorType.STANDARD:
            number = self.number
            assert number is not None
            return [str(30 + number if foreground else 40 + number)]

        elif _type == ColorType.EIGHT_BIT:
            assert self.number is not None
            return ["38" if foreground else "48", "5", str(self.number)]

        else:  # self.standard == ColorStandard.TRUECOLOR:
            assert self.triplet is not None
            red, green, blue = self.triplet
            return ["38" if foreground else "48", "2", str(red), str(green), str(blue)]

    @lru_cache(maxsize=1000)
    def downgrade(self, system: ColorSystem) -> Color:
        """Downgrade a color system to a system with fewer colors."""
        if system >= self.system:
            return self

        # Convert to 8-bit color from truecolor color
        if system == ColorSystem.EIGHT_BIT and self.system == ColorSystem.TRUECOLOR:
            # color_number = EIGHT_BIT_PALETTE.match(self.triplet)
            # return Color(self.name, ColorType.EIGHT_BIT, number=color_number)

            assert self.triplet is not None
            red, green, blue = self.triplet
            _h, l, s = rgb_to_hls(red / 255, green / 255, blue / 255)

            # If saturation is under 10% assume it is grayscale
            if s < 0.1:
                gray = int(round(l * 25))
                if gray == 0:
                    color_number = 0
                elif gray == 25:
                    color_number = 15
                else:
                    color_number = 231 + gray
                return Color(self.name, ColorType.EIGHT_BIT, number=color_number)

            ansi_red = 36 * round(red / 255.0 * 5.0)
            ansi_green = 6 * round(green / 255.0 * 5.0)
            ansi_blue = round(blue / 255.0 * 5.0)
            color_number = 16 + ansi_red + ansi_green + ansi_blue
            return Color(self.name, ColorType.EIGHT_BIT, number=color_number)

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
    assert len(hex_color) == 6, "must be 6 characters"
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

    c = Color.parse("#ff0000")
    print(c.downgrade(ColorSystem.STANDARD))

    # print(Color.parse("default"))
    # print(Color.parse("red"))
    # print(Color.parse("#ff0000"))
    # print(Color.parse("0"))
    # print(Color.parse("100"))
    # print(Color.parse("rgb(  12, 130, 200)"))

    # color = Color.parse("#339a2e")
    # print(color)
    # print(color.downgrade(ColorSystem.EIGHT_BIT))
    # print(color.downgrade(ColorSystem.STANDARD))
    # import sys

    # sys.stdout.write(Color.parse("#00ffff").foreground_sequence + "Hello")
