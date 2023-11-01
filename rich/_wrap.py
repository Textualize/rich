from __future__ import annotations

import re
from typing import Iterable, List, Tuple

from ._loop import loop_last
from .cells import cell_len, fit_to_width

re_word = re.compile(r"\s*\S+\s*")


def words(text: str) -> Iterable[Tuple[int, int, str]]:
    """Yields each word from the text as a tuple containing (start_index, end_index, word)."""
    position = 0
    word_match = re_word.match(text, position)
    while word_match is not None:
        start, end = word_match.span()
        word = word_match.group(0)
        yield start, end, word
        word_match = re_word.match(text, end)


def divide_line(text: str, width: int, fold: bool = True) -> List[int]:
    divides: List[int] = []
    append = divides.append
    line_position = 0
    _cell_len = cell_len
    for start, _end, word in words(text):
        word_length = _cell_len(word.rstrip())
        if line_position + word_length > width:
            if word_length > width:
                if fold:
                    chopped_words = fit_to_width(
                        word, available_width=width, position=line_position
                    )
                    for last, line in loop_last(chopped_words):
                        if start:
                            append(start)

                        if last:
                            line_position = _cell_len(line)
                        else:
                            start += len(line)
                else:
                    if start:
                        append(start)
                    line_position = _cell_len(word)
            elif line_position and start:
                append(start)
                line_position = _cell_len(word)
        else:
            line_position += _cell_len(word)
    return divides


def divide_line(text: str, width: int, fold: bool = True) -> list[int]:
    """Given a string of text, and a width (measured in cells), return a list
    of cell offsets which the string should be split at in order for it to fit
    within the given width.

    Args:
        text: The text to examine.
        width: The available cell width.
        fold: If True, words longer than `width` will be folded onto a new line.

    Returns:
        A list of cell offsets to break the line at.
    """

    break_offsets: list[int] = []  # offsets to insert the breaks at
    append = break_offsets.append
    line_position = 0
    _cell_len = cell_len

    for start, _end, word in words(text):
        word_length = _cell_len(word.rstrip())
        remaining_space = width - line_position
        word_fits_remaining_space = remaining_space - word_length >= 0
        if not word_fits_remaining_space:
            if word_length > width:
                # The word doesn't fit on any line, so we can't simply
                # place it on the next line...
                if fold:
                    # ... fold the long word it across multiple lines

                    # We need to fit as much as possible of the word into the remaining
                    # space on the current line.

                    # Take characters from the word until we run out of remaining space.
                    pass


if __name__ == "__main__":  # pragma: no cover
    from .console import Console

    console = Console(width=10)
    console.print("12345 abcdefghijklmnopqrstuvwyxzABCDEFGHIJKLMNOPQRSTUVWXYZ 12345")
    print(fit_to_width("abcdefghijklmnopqrstuvwxyz", 10, position=2))
