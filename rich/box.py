from __future__ import annotations


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
            self.head_row_left_row,
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

    def get_top(self, width: int) -> str:
        """Get the top of a simple box.
        
        Args:
            width (int): The width of the box (including corners)
        
        Returns:
            str: A string of box characters.
        """
        non_corner_width = width - 2
        return f"{self.top_left}{self.top * non_corner_width}{self.top_right}\n"

    def get_bottom(self, width: int) -> str:
        """Get the bottom of a simple box.
        
        Args:
            width (int): The width of the box (including corners)
        
        Returns:
            str: A string of box characters.
        """
        non_corner_width = width - 2
        return (
            f"{self.bottom_left}{self.bottom * non_corner_width}{self.bottom_right}\n"
        )


ASCII = Box(
    """
+--+
| ||
|-+|
|-+|
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

HEAVY_HEADER = Box(
    """
┏━┳┓
┃ ┃┃
┡━┻┩
│ ││
┡━╇┩
├─┬┤
│ ││
└─┴┘
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

    print("ROUNDED")
    print(ROUNDED)

    print("HEAVY")
    print(HEAVY)

    print("HEAVY_EDGE")
    print(HEAVY_EDGE)

    print("HEAVY_HEADER")
    print(HEAVY_HEADER)

    print("DOUBLE")
    print(DOUBLE)

    print("DOUBLE_EDGE")
    print(DOUBLE_EDGE)
