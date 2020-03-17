import re
from typing import Iterable, List, Tuple

from .cells import cell_len, chop_cells
from ._tools import iter_last

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
        if line_position + cell_len(word.rstrip()) > width:
            if line_position and start:
                append(start)
                line_position = cell_len(word)
            else:
                for last, line in iter_last(chop_cells(text, width)):
                    if last:
                        line_position = cell_len(line)
                    else:
                        start += len(line)
                        append(start)
        else:
            line_position += cell_len(word)
    return divides
