from __future__ import annotations

import re
from typing import Iterable

from .cells import cell_len, chop_cells, get_character_cell_size

re_word = re.compile(r"\s*\S+\s*")


def words(text: str) -> Iterable[tuple[int, int, str]]:
    """Yields each word from the text as a tuple
    containing (start_index, end_index, word). A "word" in this context may
    include the actual word and any whitespace to the right.
    """
    position = 0
    word_match = re_word.match(text, position)
    while word_match is not None:
        start, end = word_match.span()
        word = word_match.group(0)
        yield start, end, word
        word_match = re_word.match(text, end)


def divide_line(
    text: str,
    width: int,
    fold: bool = True,
    continuation_indent: int = 0,
) -> list[int]:
    """Given a string of text, and a width (measured in cells), return a list
    of cell offsets which the string should be split at in order for it to fit
    within the given width.

    If indent is provided, the all lines after the first will be divided to
    length width - indent to leave space for continuation indents.

    Args:
        text: The text to examine.
        width: The available cell width.
        fold: If True, words longer than `width` will be folded onto a new line.
        continuation_indent: The cell width of a continuation indent to account for.

    Returns:
        A list of indices to break the line at.
    """
    break_positions: list[int] = []  # offsets to insert the breaks at
    append = break_positions.append
    cell_offset = 0
    _cell_len = cell_len

    for start, _end, word in words(text):
        word_length = _cell_len(word)
        word_stripped = word.rstrip()
        word_stripped_length = _cell_len(word_stripped)
        remaining_space = width - cell_offset

        if remaining_space >= word_stripped_length:
            # Simplest case - the word fits within the remaining width for this line.
            cell_offset += word_length

        elif width >= continuation_indent + word_stripped_length:
            # The word doesn't fit within the remaining space on the current
            # line, but it *can* fit on to the next (empty) line.
            append(start)
            cell_offset = continuation_indent + word_length

        # The word doesn't fit on any line, so we can't simply
        # place it on the next line...

        elif fold:
            # Immediately break the current line.
            if start:
                append(start)
                cell_offset = continuation_indent

            # Fold the word across multiple lines. Whitespace shouldn't be
            # included because the line is already broken.
            for character in word_stripped:
                cell_count = get_character_cell_size(character)

                # If we've exceeded the number of cells we can put on this
                # line, we need to append a break and reset counters.
                if cell_offset + cell_count > width:
                    append(start)
                    cell_offset = continuation_indent

                start += 1
                cell_offset += cell_count

            # Adjust for lost whitespace at the end of the word.
            cell_offset += word_length - word_stripped_length

        else:
            # Folding isn't allowed, so crop the word.
            if start:
                append(start)
                cell_offset = continuation_indent + word_length

    return break_positions


if __name__ == "__main__":  # pragma: no cover
    from .console import Console

    console = Console(width=10)
    console.print("12345 abcdefghijklmnopqrstuvwyxzABCDEFGHIJKLMNOPQRSTUVWXYZ 12345")
    print(chop_cells("abcdefghijklmnopqrstuvwxyz", 10))

    console = Console(width=20)
    console.rule()
    console.print("TextualはPythonの高速アプリケーション開発フレームワークです")

    console.rule()
    console.print("アプリケーションは1670万色を使用でき")
