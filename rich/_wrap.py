import re
from typing import Iterable, List, Tuple

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
    for start, end, word in words(text):
        if line_position + len(word.rstrip()) > width:
            if line_position and start:
                append(start)
                line_position = len(word)
            else:
                divides.extend(range(start or width, end + 1, width))
                line_position = len(word) % width
        else:
            line_position += len(word)
    return divides
