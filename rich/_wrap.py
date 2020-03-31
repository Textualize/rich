import re
from typing import Iterable, List, Tuple

from .cells import cell_len, chop_cells
from ._loop import loop_last

re_word = re.compile(r"\s*\S+\s*")


def words(text: str) -> Iterable[Tuple[int, int, str]]:
    position = 0
    word_match = re_word.match(text, position)
    while word_match is not None:
        start, end = word_match.span()
        word = word_match.group(0)
        yield start, end, word
        word_match = re_word.match(text, end)


def divide_line(text: str, width: int) -> List[int]:
    divides: List[int] = []
    append = divides.append
    line_position = 0
    for start, _end, word in words(text):
        word_length = cell_len(word.rstrip())
        if line_position + word_length > width:
            if word_length > width:
                for last, line in loop_last(
                    chop_cells(word, width, position=line_position)
                ):
                    if last:
                        line_position = cell_len(line)
                    else:
                        start += len(line)
                        append(start)
            elif line_position and start:
                append(start)
                line_position = cell_len(word)
        else:
            line_position += cell_len(word)
    return divides


if __name__ == "__main__":  # pragma: no cover
    from .console import Console

    console = Console(width=10)
    console.print("12345 abcdefghijklmnopqrstuvwyxzABCDEFGHIJKLMNOPQRSTUVWXYZ 12345")
    print(chop_cells("abcdefghijklmnopqrstuvwxyz", 10, position=2))
