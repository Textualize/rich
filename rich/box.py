from __future__ import annotations

from typing import List

from ._tools import iter_last


class Box:
    """Defines characters to render boxes.
    
    ┌─┬┐ top
    │ ││ head
    ├─┴┤ head_row
    │ ││ mid
    ├─┼┤ row
    ├─┬┤ foot_row
    │ ││ foot
    └─┴┘ bottom

    
    """

    def __init__(self, box: str) -> None:
        (
            line1,
            line2,
            line3,
            line4,
            line5,
            line6,
            line7,
            line8,
        ) = box.strip().splitlines()
        self.top_left, self.top, self.top_divider, self.top_right = line1
        self.head_left, _, self.head_vertical, self.head_right = line2
        (
            self.head_row_left,
            self.head_row_horizontal,
            self.head_row_divider,
            self.head_row_right,
        ) = line3

        self.mid_left, _, self.mid_vertical, self.mid_right = line4
        self.row_left, self.row_horizontal, self.row_cross, self.row_right = line5

        (
            self.foot_row_left,
            self.foot_row_horizontal,
            self.foot_row_divider,
            self.foot_row_right,
        ) = line6
        self.foot_left, _, self.foot_vertical, self.foot_right = line7
        self.bottom_left, self.bottom, self.bottom_divider, self.bottom_right = line8

    def __repr__(self) -> str:
        border_str = str(self).replace("\n", r"\n")
        return f'Border("{border_str}")'

    def __str__(self) -> str:
        return (
            f"{self.top_left}{self.top}{self.top_divider}{self.top}{self.top_right}\n"
            f"{self.head_left} {self.head_vertical} {self.head_right}\n"
            f"{self.row_left}{self.row_horizontal}{self.row_cross}{self.row_horizontal}{self.row_right}\n"
            f"{self.foot_left} {self.foot_vertical} {self.foot_right}\n"
            f"{self.bottom_left}{self.bottom}{self.bottom_divider}{self.bottom}{self.bottom_right}"
        )

    def get_top(self, *widths: int) -> str:
        """Get the top of a simple box.
        
        Args:
            *width (int): Widths of columns.
        
        Returns:
            str: A string of box characters.
        """

        parts: List[str] = []
        append = parts.append
        append(self.top_left)
        for last, width in iter_last(widths):
            append(self.top * width)
            if not last:
                append(self.top_divider)
        append(self.top_right)
        append("\n")
        return "".join(parts)

    def get_row(self, *widths: int) -> str:
        """Get the top of a simple box.
        
        Args:
            *width (int): Widths of columns.
        
        Returns:
            str: A string of box characters.
        """

        parts: List[str] = []
        append = parts.append
        append(self.head_row_left)
        for last, width in iter_last(widths):
            append(self.head_row_horizontal * width)
            if not last:
                append(self.row_cross)
        append(self.head_row_right)
        append("\n")
        return "".join(parts)

    def get_bottom(self, *widths: int) -> str:
        """Get the top of a simple box.
        
        Args:
            *width (int): Widths of columns.
        
        Returns:
            str: A string of box characters.
        """

        parts: List[str] = []
        append = parts.append
        append(self.bottom_left)
        for last, width in iter_last(widths):
            append(self.bottom * width)
            if not last:
                append(self.bottom_divider)
        append(self.bottom_right)
        append("\n")
        return "".join(parts)


ASCII = Box(
    """
+--+
| ||
|-+|
| ||
|-+|
|-+|
| ||
+--+
"""
)

SQUARE = Box(
    """
┌─┬┐
│ ││
├─┴┤
│ ││
├─┼┤
├─┬┤
│ ││
└─┴┘
"""
)

HORIZONTALS = Box(
    """
────
    
────
    
────
────
    
────
"""
)

ROUNDED = Box(
    """
╭─┬╮
│ ││
├─┴┤
│ ││
├─┼┤
├─┬┤
│ ││
╰─┴╯
"""
)

HEAVY = Box(
    """
┏━┳┓
┃ ┃┃
┣━┻┫
┃ ┃┃
┣━╋┫
┣━┳┫
┃ ┃┃
┗━┻┛
"""
)

HEAVY_EDGE = Box(
    """
┏━┯┓
┃ │┃
┠─┴┨
┃ │┃
┠─┼┨
┠─┬┨
┃ │┃
┗━┷┛
"""
)

DOUBLE = Box(
    """
╔═╦╗
║ ║║
╠═╩╣
║ ║║
╠═╬╣
╠═╦╣
║ ║║
╚═╩╝
"""
)

DOUBLE_EDGE = Box(
    """
╔═╤╗
║ │║
╟─┴╢
║ │║
╟─┼╢
╟─┬╢
║ │║
╚═╧╝
"""
)


if __name__ == "__main__":
    print("ASCII")
    print(ASCII)

    print("SQUARE")
    print(SQUARE)

    print("HORIZONTALS")
    print(HORIZONTALS)

    print("ROUNDED")
    print(ROUNDED)

    print("HEAVY")
    print(HEAVY)

    print("HEAVY_EDGE")
    print(HEAVY_EDGE)

    print("DOUBLE")
    print(DOUBLE)

    print("DOUBLE_EDGE")
    print(DOUBLE_EDGE)
