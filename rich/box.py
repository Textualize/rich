from typing import Iterable, List
from typing_extensions import Literal

from ._tools import iter_last


class Box:
    """Defines characters to render boxes.
    
    ┌─┬┐ top
    │ ││ head
    ├─┼┤ head_row
    │ ││ mid
    ├─┼┤ row
    ├─┼┤ foot_row
    │ ││ foot
    └─┴┘ bottom

    
    """

    def __init__(self, box: str) -> None:
        self._box = box
        (line1, line2, line3, line4, line5, line6, line7, line8,) = box.splitlines()
        # top
        self.top_left, self.top, self.top_divider, self.top_right = line1
        # head
        self.head_left, _, self.head_vertical, self.head_right = line2
        # head_row
        (
            self.head_row_left,
            self.head_row_horizontal,
            self.head_row_cross,
            self.head_row_right,
        ) = line3

        # mid
        self.mid_left, _, self.mid_vertical, self.mid_right = line4
        # row
        self.row_left, self.row_horizontal, self.row_cross, self.row_right = line5
        # foot_row
        (
            self.foot_row_left,
            self.foot_row_horizontal,
            self.foot_row_cross,
            self.foot_row_right,
        ) = line6
        # foot
        self.foot_left, _, self.foot_vertical, self.foot_right = line7
        # bottom
        self.bottom_left, self.bottom, self.bottom_divider, self.bottom_right = line8

    def __repr__(self) -> str:
        border_str = str(self).replace("\n", r"\n")
        return f'Border("{border_str}")'

    def __str__(self) -> str:
        return self._box

    def get_top(self, widths: Iterable[int]) -> str:
        """Get the top of a simple box.
        
        Args:
            widths (List[int]): Widths of columns.
        
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

    def get_row(
        self,
        widths: Iterable[int],
        level: Literal["head", "row", "foot"] = "row",
        edge: bool = True,
    ) -> str:
        """Get the top of a simple box.
        
        Args:
            width (List[int]): Widths of columns.
        
        Returns:
            str: A string of box characters.
        """
        if level == "head":
            left = self.head_row_left
            horizontal = self.head_row_horizontal
            cross = self.head_row_cross
            right = self.head_row_right
        elif level == "row":
            left = self.row_left
            horizontal = self.row_horizontal
            cross = self.row_cross
            right = self.row_right
        elif level == "foot":
            left = self.foot_row_left
            horizontal = self.foot_row_horizontal
            cross = self.foot_row_cross
            right = self.foot_row_right
        else:
            raise ValueError("level must be 'head', 'row' or 'foot'")

        parts: List[str] = []
        append = parts.append
        if edge:
            append(left)
        for last, width in iter_last(widths):
            append(horizontal * width)
            if not last:
                append(cross)
        if edge:
            append(right)
        append("\n")
        return "".join(parts)

    def get_bottom(self, widths: Iterable[int]) -> str:
        """Get the top of a simple box.
        
        Args:
            widths (List[int]): Widths of columns.
        
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
    """\
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
    """\
┌─┬┐
│ ││
├─┼┤
│ ││
├─┼┤
├─┼┤
│ ││
└─┴┘
"""
)


MINIMAL = Box(
    """\
    
  │ 
 ─┼ 
  │ 
 ─┼ 
 ─┼ 
  │ 
    
"""
)


MINIMAL_HEAVY_HEAD = Box(
    """\
    
  │ 
 ━┿ 
  │ 
 ─┼ 
 ─┼ 
  │ 
    
"""
)

MINIMAL_DOUBLE_HEAD = Box(
    """\
    
  │ 
 ═╪ 
  │ 
 ─┼ 
 ─┼ 
  │ 
    
"""
)


SIMPLE = Box(
    """\
    
    
────
    
    
────
    
    
"""
)


SIMPLE_HEAVY = Box(
    """\
    
    
╺━━╸
    
    
╺━━╸
    
    
"""
)


HORIZONTALS = Box(
    """\
────
    
────
    
────
────
    
────
"""
)

ROUNDED = Box(
    """\
╭─┬╮
│ ││
├─┼┤
│ ││
├─┼┤
├─┼┤
│ ││
╰─┴╯
"""
)

HEAVY = Box(
    """\
┏━┳┓
┃ ┃┃
┣━╋┫
┃ ┃┃
┣━╋┫
┣━╋┫
┃ ┃┃
┗━┻┛
"""
)

HEAVY_EDGE = Box(
    """\
┏━┯┓
┃ │┃
┠─┼┨
┃ │┃
┠─┼┨
┠─┼┨
┃ │┃
┗━┷┛
"""
)

HEAVY_HEAD = Box(
    """\
┏━┳┓
┃ ┃┃
┡━╇┩
│ ││
├─┼┤
├─┼┤
│ ││
└─┴┘
"""
)

DOUBLE = Box(
    """\
╔═╦╗
║ ║║
╠═╬╣
║ ║║
╠═╬╣
╠═╬╣
║ ║║
╚═╩╝
"""
)

DOUBLE_EDGE = Box(
    """\
╔═╤╗
║ │║
╟─┼╢
║ │║
╟─┼╢
╟─┼╢
║ │║
╚═╧╝
"""
)


if __name__ == "__main__":  # pragma: no cover
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

    print("HEAVY_HEAD")
    print(HEAVY_HEAD)

    print("DOUBLE")
    print(DOUBLE)

    print("DOUBLE_EDGE")
    print(DOUBLE_EDGE)
