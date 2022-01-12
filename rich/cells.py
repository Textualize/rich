import re
from typing import List

from cells import Cells

# Regex to match sequence of the most common character ranges
_is_single_cell_widths = re.compile("^[\u0020-\u006f\u00a0\u02ff\u0370-\u0482]*$").match
_cells: Cells = Cells()


def cell_len(text: str) -> int:
    """Get the number of cells required to display text.

    Args:
        text (str): Text to display.

    Returns:
        int: Get the number of cells required to display text.
    """
    return _cells.measure(text)


def set_cell_size(text: str, total: int) -> str:
    """Set the length of a string to fit within given number of cells."""

    if _is_single_cell_widths(text):
        size = len(text)
        if size < total:
            return text + " " * (total - size)
        return text[:total]

    if not total:
        return ""
    cell_size = cell_len(text)
    if cell_size == total:
        return text
    if cell_size < total:
        return text + " " * (total - cell_size)

    start = 0
    end = len(text)

    # Binary search until we find the right size
    while True:
        pos = (start + end) // 2
        before = text[: pos + 1]
        before_len = cell_len(before)
        if before_len == total + 1 and cell_len(before[-1]) == 2:
            return before[:-1] + " "
        if before_len == total:
            return before
        if before_len > total:
            end = pos
        else:
            start = pos


# TODO: This is inefficient
# TODO: This might not work with CWJ type characters
def chop_cells(text: str, max_size: int, position: int = 0) -> List[str]:
    """Break text in to equal (cell) length strings."""
    characters = [(character, cell_len(character)) for character in text][::-1]
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

    print(cell_len("😽"))
    for line in chop_cells("""这是对亚洲语言支持的测试。面对模棱两可的想法，拒绝猜测的诱惑。""", 8):
        print(line)
    for n in range(80, 1, -1):
        print(set_cell_size("""这是对亚洲语言支持的测试。面对模棱两可的想法，拒绝猜测的诱惑。""", n) + "|")
        print("x" * n)
