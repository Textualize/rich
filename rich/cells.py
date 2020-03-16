from functools import lru_cache
from itertools import takewhile
from typing import List, Tuple

from ._cell_widths import CELL_WIDTHS


def cell_len(text: str) -> int:
    """Get the number of cells required to display text.
    
    Args:
        text (str): Text to display.
    
    Returns:
        int: Number of cells required to display the text.
    """
    _get_size = get_character_cell_size
    return sum(_get_size(character) for character in text)


@lru_cache(maxsize=5000)
def get_character_cell_size(character: str, _table=CELL_WIDTHS) -> int:
    """Get the cell size of a character.
    
    Args:
        character (str): A single character.
    
    Returns:
        int: Number of cells (0, 1 or 2) occupied by that character.
    """
    assert len(character) == 1, "'character' should have a length of 1"

    codepoint = ord(character)
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
    while excess > 0:
        excess -= pop()
    text = text[: len(character_sizes)]
    if excess == -1:
        text += " "
    return text


def chop_cells(text: str, max_size: int) -> List[str]:
    _get_character_cell_size = get_character_cell_size
    characters = [
        (character, _get_character_cell_size(character)) for character in text
    ][::-1]
    total_size = 0
    lines: List[List[str]] = [[]]

    pop = characters.pop
    while characters:
        character, size = characters.pop()
        if total_size + size > max_size:
            lines.append([character])
            total_size = size
        else:
            total_size += size
            lines[-1].append(character)
    return ["".join(line) for line in lines]


if __name__ == "__main__":

    print(get_character_cell_size("😽"))
    for line in chop_cells("""这是对亚洲语言支持的测试。面对模棱两可的想法，拒绝猜测的诱惑。""", 8):
        print(line)
    for n in range(80, 1, -1):
        print(set_cell_size("""这是对亚洲语言支持的测试。面对模棱两可的想法，拒绝猜测的诱惑。""", n) + "|")
        print("x" * n)

