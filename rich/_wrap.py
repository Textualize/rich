import re
from typing import Iterable, List, Tuple

re_word = re.compile(r"\s*\S+\s*")


def words(text: str) -> Iterable[Tuple[int, str]]:
    position = 0
    word_match = re_word.match(text, position)
    while word_match is not None:
        start, position = word_match.span()
        word = word_match.group(0)
        yield start, word
        word_match = re_word.match(text, position)


def divide_line(text: str, width: int) -> List[int]:
    divides: List[int] = []
    append = divides.append
    line_size = 0
    for position, word in words(text):
        if line_size + len(word.rstrip()) > width:
            if position:
                append(position)
            line_size = 0
        line_size += len(word)
    return divides


if __name__ == "__main__":  # pragma: no cover
    test = "      Where there is a Will there is a way. Hello World. There   can be only one."

    boundaries = [0, *wrap(test, 10), len(test)]
    print(boundaries)
    for start, end in zip(boundaries, boundaries[1:]):
        line = test[start:end]
        print(f"{len(line)}\t", repr(line))

