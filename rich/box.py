from __future__ import annotations


class Box:
    """Defines characters to render boxes."""

    def __init__(self, box: str) -> None:
        box = box.strip().replace("\n", "")
        (
            self.top_left,
            self.top,
            self.top_cross,
            self.top_right,
            self.left,
            _,
            self.mid_vertical,
            self.right,
            self.mid_left,
            self.mid_horizontal,
            self.cross,
            self.mid_right,
            self.bottom_left,
            self.bottom,
            self.bottom_cross,
            self.bottom_right,
        ) = box

    def __repr__(self) -> str:
        border_str = str(self).replace("\n", r"\n")
        return f'Border("{border_str}")'

    def __str__(self) -> str:
        return (
            f"{self.top_left}{self.top}{self.top_cross}{self.top}{self.top_right}\n"
            f"{self.left} {self.mid_vertical} {self.right}\n"
            f"{self.mid_left}{self.mid_horizontal}{self.cross}{self.mid_horizontal}{self.mid_right}\n"
            f"{self.left} {self.mid_vertical} {self.right}\n"
            f"{self.bottom_left}{self.bottom}{self.bottom_cross}{self.bottom}{self.bottom_right}"
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
+-++
| ||
+-++
+-++
"""
)

SQUARE = Box(
    """
┌─┬┐
│ ││
├─┼┤
└─┴┘
"""
)

ROUNDED = Box(
    """
╭─┬╮
│ ││
├─┼┤
╰─┴╯
"""
)

HEAVY = Box(
    """
┏━┳┓
┃ ┃┃
┣━╋┫
┗━┻┛
"""
)

HEAVY_EDGE = Box(
    """
┏━┯┓
┃ │┃
┠─┼┨
┗━┷┛
"""
)

DOUBLE = Box(
    """
╔═╦╗
║ ║║
╠═╬╣
╚═╩╝   
"""
)


DOUBLE_EDGE = Box(
    """
╔═╤╗
║ │║
╟─┼╢
╚═╧╝
"""
)

if __name__ == "__main__":
    print(ASCII)
    print(SQUARE)
    print(ROUNDED)
    print(HEAVY)
    print(HEAVY_EDGE)
    print(DOUBLE)
    print(DOUBLE_EDGE)
