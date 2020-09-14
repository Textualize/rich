from functools import lru_cache
from typing import Dict, List

from ._cell_widths import CELL_WIDTHS
from ._lru_cache import LRUCache


def cell_len(text: str, _cache: Dict[str, int] = LRUCache(1024 * 4)) -> int:
    """Get the number of cells required to display text.

    Args:
        text (str): Text to display.

    Returns:
        int: Number of cells required to display the text.
    """
    cached_result = _cache.get(text, None)
    if cached_result is not None:
        return cached_result

    _get_size = get_character_cell_size
    total_size = sum(_get_size(character) for character in text)
    if len(text) <= 64:
        _cache[text] = total_size
    return total_size


def get_character_cell_size(character: str) -> int:
    """Get the cell size of a character.

    Args:
        character (str): A single character.

    Returns:
        int: Number of cells (0, 1 or 2) occupied by that character.
    """

    codepoint = ord(character)
    if 127 > codepoint > 31:
        # Shortcut for ascii
        return 1
    return _get_codepoint_cell_size(codepoint)


@lru_cache(maxsize=4096)
def _get_codepoint_cell_size(codepoint: int) -> int:
    """Get the cell size of a character.

    Args:
        character (str): A single character.

    Returns:
        int: Number of cells (0, 1 or 2) occupied by that character.
    """

    _table = CELL_WIDTHS
    lower_bound = 0
    upper_bound = len(_table) - 1
    index = (lower_bound + upper_bound) // 2
    while True:
        start, end, width = _table[index]
        if codepoint < start:
            upper_bound = index - 1
        elif codepoint > end:
            lower_bound = index + 1
        else:
            return 0 if width == -1 else width
        if upper_bound < lower_bound:
            break
        index = (lower_bound + upper_bound) // 2
    return 1


def set_cell_size(text: str, total: int) -> str:
    """Set the length of a string to fit within given number of cells."""
    cell_size = cell_len(text)
    if cell_size == total:
        return text
    if cell_size < total:
        return text + " " * (total - cell_size)

    _get_character_cell_size = get_character_cell_size
    character_sizes = [_get_character_cell_size(character) for character in text]
    excess = cell_size - total
    pop = character_sizes.pop
    while excess > 0 and character_sizes:
        excess -= pop()
    text = text[: len(character_sizes)]
    if excess == -1:
        text += " "
    return text


def chop_cells(text: str, max_size: int, position: int = 0) -> List[str]:
    """Break text in to equal (cell) length strings."""
    _get_character_cell_size = get_character_cell_size
    characters = [
        (character, _get_character_cell_size(character)) for character in text
    ][::-1]
    total_size = position
    lines: List[List[str]] = [[]]
    append = lines[-1].append

    pop = characters.pop
    while characters:
        character, size = pop()
        if total_size + size > max_size:
            lines.append([character])
            append = lines[-1].append
            total_size = size
        else:
            total_size += size
            append(character)
    return ["".join(line) for line in lines]


if __name__ == "__main__":  # pragma: no cover

    print(get_character_cell_size("😽"))
    for line in chop_cells("""这是对亚洲语言支持的测试。面对模棱两可的想法，拒绝猜测的诱惑。""", 8):
        print(line)
    for n in range(80, 1, -1):
        print(set_cell_size("""这是对亚洲语言支持的测试。面对模棱两可的想法，拒绝猜测的诱惑。""", n) + "|")
        print("x" * n)
