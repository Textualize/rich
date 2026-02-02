from __future__ import annotations

from functools import lru_cache
from typing import Callable, Tuple

from wcwidth import clip, iter_graphemes, wcwidth
from wcwidth import width as wcwidth_width

CellSpan = Tuple[int, int, int]

# Ranges of unicode ordinals that produce a 1-cell wide character
# This is non-exhaustive, but covers most common Western characters
_SINGLE_CELL_UNICODE_RANGES: list[tuple[int, int]] = [
    (0x20, 0x7E),  # Latin (excluding non-printable)
    (0xA0, 0xAC),
    (0xAE, 0x002FF),
    (0x00370, 0x00482),  # Greek / Cyrillic
    (0x02500, 0x025FC),  # Box drawing, box elements, geometric shapes
    (0x02800, 0x028FF),  # Braille
]

# A frozen set of characters that are a single cell wide
_SINGLE_CELLS = frozenset(
    [
        character
        for _start, _end in _SINGLE_CELL_UNICODE_RANGES
        for character in map(chr, range(_start, _end + 1))
    ]
)

# When called with a string this will return True if all
# characters are single-cell, otherwise False
_is_single_cell_widths: Callable[[str], bool] = _SINGLE_CELLS.issuperset


@lru_cache(maxsize=4096)
def get_character_cell_size(character: str, unicode_version: str = "auto") -> int:
    """Get the cell size of a character.

    Args:
        character (str): A single character.
        unicode_version: Unicode version, `"auto"` to auto detect, `"latest"` for the latest unicode version.

    Returns:
        int: Number of cells (0, 1 or 2) occupied by that character.
    """
    return max(0, wcwidth(character))


@lru_cache(4096)
def cached_cell_len(text: str, unicode_version: str = "auto") -> int:
    """Get the number of cells required to display text.

    This method always caches, which may use up a lot of memory. It is recommended to use
    `cell_len` over this method.

    Args:
        text (str): Text to display.
        unicode_version: Unicode version, `"auto"` to auto detect, `"latest"` for the latest unicode version.

    Returns:
        int: Get the number of cells required to display text.
    """
    return _cell_len(text, unicode_version)


def cell_len(text: str, unicode_version: str = "auto") -> int:
    """Get the cell length of a string (length as it appears in the terminal).

    Args:
        text: String to measure.
        unicode_version: Unicode version, `"auto"` to auto detect, `"latest"` for the latest unicode version.

    Returns:
        Length of string in terminal cells.
    """
    if len(text) < 512:
        return cached_cell_len(text, unicode_version)
    return _cell_len(text, unicode_version)


def _cell_len(text: str, unicode_version: str) -> int:
    """Get the cell length of a string (length as it appears in the terminal).

    Args:
        text: String to measure.
        unicode_version: Unicode version, `"auto"` to auto detect, `"latest"` for the latest unicode version.

    Returns:
        Length of string in terminal cells.
    """

    if _is_single_cell_widths(text):
        return len(text)

    return wcwidth_width(text, control_codes="ignore")


def split_graphemes(
    text: str, unicode_version: str = "auto"
) -> "tuple[list[CellSpan], int]":
    """Divide text into spans that define a single grapheme.

    Args:
        text: String to split.
        unicode_version: Unicode version, `"auto"` to auto detect, `"latest"` for the latest unicode version.

    Returns:
        List of spans.
    """

    total_width = 0
    spans: list[tuple[int, int, int]] = []
    pos = 0
    for grapheme in iter_graphemes(text):
        grapheme_len = len(grapheme)
        grapheme_width = wcwidth_width(grapheme, control_codes="ignore")
        if grapheme_width > 0 or spans:
            if grapheme_width > 0:
                spans.append((pos, pos + grapheme_len, grapheme_width))
                total_width += grapheme_width
            elif spans:
                start, _end, cell_length = spans[-1]
                spans[-1] = (start, pos + grapheme_len, cell_length)
        pos += grapheme_len

    return (spans, total_width)


def split_text(
    text: str, cell_position: int, unicode_version: str = "auto"
) -> tuple[str, str]:
    """Split text by cell position.

    If the cell position falls within a double width character, it is converted to two spaces.

    Args:
        text: Text to split.
        cell_position Offset in cells.
        unicode_version: Unicode version, `"auto"` to auto detect, `"latest"` for the latest unicode version.

    Returns:
        Tuple to two split strings.
    """
    if cell_position <= 0:
        return "", text
    if _is_single_cell_widths(text):
        return text[:cell_position], text[cell_position:]
    total = wcwidth_width(text, control_codes="ignore")
    left = clip(text, 0, cell_position)
    right = clip(text, cell_position, total)
    return left, right


def set_cell_size(text: str, total: int, unicode_version: str = "auto") -> str:
    """Adjust a string by cropping or padding with spaces such that it fits within the given number of cells.

    Args:
        text: String to adjust.
        total: Desired size in cells.
        unicode_version: Unicode version.

    Returns:
        A string with cell size equal to total.
    """
    if _is_single_cell_widths(text):
        size = len(text)
        if size < total:
            return text + " " * (total - size)
        return text[:total]
    if total <= 0:
        return ""
    cell_size = cell_len(text)
    if cell_size == total:
        return text
    if cell_size < total:
        return text + " " * (total - cell_size)
    text, _ = split_text(text, total, unicode_version)
    return text


def chop_cells(text: str, width: int, unicode_version: str = "auto") -> list[str]:
    """Split text into lines such that each line fits within the available (cell) width.

    Args:
        text: The text to fold such that it fits in the given width.
        width: The width available (number of cells).

    Returns:
        A list of strings such that each string in the list has cell width
        less than or equal to the available width.
    """
    if _is_single_cell_widths(text):
        return [text[index : index + width] for index in range(0, len(text), width)]
    spans, _ = split_graphemes(text, unicode_version)
    line_size = 0  # Size of line in cells
    lines: list[str] = []
    line_offset = 0  # Offset (in codepoints) of start of line
    for start, end, cell_size in spans:
        if line_size + cell_size > width:
            lines.append(text[line_offset:start])
            line_offset = start
            line_size = 0
        line_size += cell_size
    if line_size:
        lines.append(text[line_offset:])

    return lines
