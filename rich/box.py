from __future__ import annotations


class Box:
    """Defines characters to render boxes."""

    def __init__(self, box: str) -> None:
        line1, line2, line3, line4, line5, line6 = box.strip().splitlines()
        self.top_left, self.top, self.top_divider, self.top_right = line1

        self.left, _, self.vertical, self.right = line2

        (
            self.left_row,
            self.horizontal,
            self.horizontal_top_divider,
            self.right_row,
        ) = line3

        _, _, self.cross, _ = line4

        _, _, self.horizontal_bottom_divider, self.right_row = line5

        self.bottom_left, self.bottom, self.bottom_divider, self.bottom_right = line6

    def __repr__(self) -> str:
        border_str = str(self).replace("\n", r"\n")
        return f'Border("{border_str}")'

    def __str__(self) -> str:
        return (
            f"{self.top_left}{self.top}{self.top_divider}{self.top}{self.top_right}\n"
            f"{self.left} {self.vertical} {self.right}\n"
            f"{self.left_row}{self.horizontal}{self.cross}{self.horizontal}{self.right_row}\n"
            f"{self.left} {self.vertical} {self.right}\n"
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
+--+
"""
)

SQUARE = Box(
    """
┌─┬┐
│ ││
├─┴┤
├─┼┤
├─┬┤
└─┴┘
"""
)

ROUNDED = Box(
    """
╭─┬╮
│ ││
├─┴┤
├─┼┤
├─┬┤
╰─┴╯
"""
)

HEAVY = Box(
    """
┏━┳┓
┃ ┃┃
┣━┻┫
┣━╋┫
┣━┳┫
┗━┻┛
"""
)

HEAVY_EDGE = Box(
    """
┏━┯┓
┃ │┃
┠─┴┨
┠─┼┨
┠─┬┨
┗━┷┛
"""
)

DOUBLE = Box(
    """
╔═╦╗
║ ║║
╠═╩╣
╠═╬╣
╠═╦╣
╚═╩╝
"""
)

DOUBLE_EDGE = Box(
    """
╔═╤╗
║ │║
╟─┴╢
╟─┼╢
╟─┬╢
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

    print("DOUBLE")
    print(DOUBLE)

    print("DOUBLE_EDGE")
    print(DOUBLE_EDGE)
