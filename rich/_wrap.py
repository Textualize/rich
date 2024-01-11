from __future__ import annotations

import re
from typing import Iterable

from ._loop import loop_last
from .cells import cell_len, chop_cells

re_chunk = re.compile(r"\s*\S+\s*")


def chunks(text: str) -> Iterable[tuple[int, int, str]]:
    """Yields each "chunk" from the text as a tuple containing (start_index, end_index, chunk_content).
    A "chunk" in this context refers to a word and any whitespace around it.

    Args:
        text: The text to split into chunks.

    Returns:
        Yields tuples containing the start, end and content for each chunk.
    """
    position = 0
    chunk_match = re_chunk.match(text, position)
    while chunk_match is not None:
        start, end = chunk_match.span()
        chunk = chunk_match.group(0)
        yield start, end, chunk
        chunk_match = re_chunk.match(text, end)


def divide_line(
    text: str, width: int, fold: bool = True, keep_whitespace: bool = False
) -> list[int]:
    """Given a string of text, and a width (measured in cells), return a list
    of codepoint indices which the string should be split at in order for it to fit
    within the given width.

    Args:
        text: The text to examine.
        width: The available cell width.
        fold: If True, words longer than `width` will be folded onto a new line.
        keep_whitespace: If True, consecutive spaces will not be collapsed at line ends.

    Returns:
        A list of indices to break the line at.
    """
    break_positions: list[int] = []  # offsets to insert the breaks at
    append = break_positions.append
    cell_offset = 0
    _cell_len = cell_len

    for start, _end, chunk in chunks(text):
        word_width = _cell_len(chunk)
        if keep_whitespace:
            chunk_width = word_width
            width_contribution = chunk_width
        else:
            chunk_width = _cell_len(chunk.rstrip())
            width_contribution = word_width

        remaining_space = width - cell_offset
        chunk_fits = remaining_space >= chunk_width

        if chunk_fits:
            # Simplest case - the word fits within the remaining width for this line.
            cell_offset += width_contribution
        else:
            # Not enough space remaining for this word on the current line.
            if chunk_width > width:
                # The word doesn't fit on any line, so we can't simply
                # place it on the next line...
                if fold:
                    # Fold the word across multiple lines.
                    folded_word = chop_cells(chunk, width=width)
                    for last, line in loop_last(folded_word):
                        if start:
                            append(start)
                        if last:
                            cell_offset = _cell_len(line)
                        else:
                            start += len(line)
                else:
                    # Folding isn't allowed, so crop the word.
                    if start:
                        append(start)
                    cell_offset = width_contribution
            elif cell_offset and start:
                # The word doesn't fit within the remaining space on the current
                # line, but it *can* fit on to the next (empty) line.
                append(start)
                cell_offset = width_contribution

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
