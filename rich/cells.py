from __future__ import annotations

import bisect
import re
import sys
from functools import lru_cache
from itertools import accumulate
from typing import Callable

from ._cell_widths import CELL_WIDTHS

# Regex to match sequence of the most common character ranges
_is_single_cell_widths = re.compile("^[\u0020-\u006f\u00a0\u02ff\u0370-\u0482]*$").match


@lru_cache(4096)
def cached_cell_len(text: str) -> int:
    """Get the number of cells required to display text.

    This method always caches, which may use up a lot of memory. It is recommended to use
    `cell_len` over this method.

    Args:
        text (str): Text to display.

    Returns:
        int: Get the number of cells required to display text.
    """
    _get_size = get_character_cell_size
    total_size = sum(_get_size(character) for character in text)
    return total_size


def cell_len(text: str, _cell_len: Callable[[str], int] = cached_cell_len) -> int:
    """Get the number of cells required to display text.

    Args:
        text (str): Text to display.

    Returns:
        int: Get the number of cells required to display text.
    """
    if len(text) < 512:
        return _cell_len(text)
    _get_size = get_character_cell_size
    total_size = sum(_get_size(character) for character in text)
    return total_size


@lru_cache(maxsize=4096)
def get_character_cell_size(character: str) -> int:
    """Get the cell size of a character.

    Args:
        character (str): A single character.

    Returns:
        int: Number of cells (0, 1 or 2) occupied by that character.
    """
    return _get_codepoint_cell_size(ord(character))


@lru_cache(maxsize=4096)
def _get_codepoint_cell_size(codepoint: int) -> int:
    """Get the cell size of a character.

    Args:
        codepoint (int): Codepoint of a character.

    Returns:
        int: Number of cells (0, 1 or 2) occupied by that character.
    """
    # We create the tuple as `(cp, sys.maxunicode + 2)` instead of just (cp,)
    # because we want the index to always be on the right of the range that
    # `cp` belongs to. E.g., `(1,)` won't be placed to the right of `(1, 31, -1)`
    # but `(1, sys.maxunicode + 2)` will.
    idx = bisect.bisect_right(CELL_WIDTHS, (codepoint, sys.maxunicode + 2))
    _start, end, width = CELL_WIDTHS[idx - 1]
    if codepoint <= end:
        return 0 if width == -1 else width
    else:
        return 1


def set_cell_size(text: str, total: int) -> str:
    """Set the length of a string to fit within given number of cells.

    The return value is guaranteed to have no trailing 0-width characters.
    """

    if _is_single_cell_widths(text):
        size = len(text)
        if size < total:
            return text + " " * (total - size)
        return text[:total]

    if total <= 0:
        return ""

    _cell_size = get_character_cell_size
    widths = [_cell_size(char) for char in text]
    lengths = list(accumulate(widths))

    total_length = lengths[-1]
    if total_length == total:
        return text
    if total_length < total:
        return text + " " * (total - total_length)

    idx = bisect.bisect_left(lengths, total)
    if lengths[idx] == total:
        return text[: idx + 1]
    if idx == 0:
        return " " * total
    if lengths[idx - 1] < total:
        return text[:idx] + " "
    return text[:idx]


def chop_cells(
    text: str,
    width: int,
) -> list[str]:
    """Split text into lines such that each line fits within the available (cell) width.

    Args:
        text: The text to fold such that it fits in the given width.
        width: The width available (number of cells).

    Returns:
        A list of strings such that each string in the list has cell width
        less than or equal to the available width.
    """
    _get_character_cell_size = get_character_cell_size
    lines: list[list[str]] = [[]]

    append_new_line = lines.append
    append_to_last_line = lines[-1].append

    total_width = 0

    for character in text:
        cell_width = _get_character_cell_size(character)
        char_doesnt_fit = total_width + cell_width > width

        if char_doesnt_fit:
            append_new_line([character])
            append_to_last_line = lines[-1].append
            total_width = cell_width
        else:
            append_to_last_line(character)
            total_width += cell_width

    return ["".join(line) for line in lines]


if __name__ == "__main__":  # pragma: no cover
    print(get_character_cell_size("😽"))
    for line in chop_cells("""这是对亚洲语言支持的测试。面对模棱两可的想法，拒绝猜测的诱惑。""", 8):
        print(line)
    for n in range(80, 1, -1):
        print(set_cell_size("""这是对亚洲语言支持的测试。面对模棱两可的想法，拒绝猜测的诱惑。""", n) + "|")
        print("x" * n)
