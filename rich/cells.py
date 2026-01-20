from __future__ import annotations

from functools import lru_cache
from operator import itemgetter
from typing import Callable, Generator, Iterator, NamedTuple, Sequence, Tuple

from rich._unicode_data import load as load_cell_table

CellSpan = Tuple[int, int, int]

_span_get_cell_len = itemgetter(2)

# Ranges of unicode ordinals that produce a 1-cell wide character
# This is non-exhaustive, but covers most common Western characters
_SINGLE_CELL_UNICODE_RANGES: list[tuple[int, int]] = [
    (0x20, 0x7E),  # Latin (excluding non-printable)
    (0xA0, 0xAC),
    (0xAE, 0x002FF),
    (0x00370, 0x00482),  # Greek / Cyrillic
    (0x02500, 0x025FC),  # Box drawing, box elements, geometric shapes
    (0x02800, 0x028FF),  # Braille
]

# A frozen set of characters that are a single cell wide
_SINGLE_CELLS = frozenset(
    [
        character
        for _start, _end in _SINGLE_CELL_UNICODE_RANGES
        for character in map(chr, range(_start, _end + 1))
    ]
)

# When called with a string this will return True if all
# characters are single-cell, otherwise False
_is_single_cell_widths: Callable[[str], bool] = _SINGLE_CELLS.issuperset


class CellTable(NamedTuple):
    """Contains unicode data required to measure the cell widths of glyphs."""

    unicode_version: str
    widths: Sequence[tuple[int, int, int]]
    narrow_to_wide: frozenset[str]

    def __hash__(self) -> int:
        return hash(self.unicode_version)


@lru_cache(maxsize=4096)
def get_character_cell_size(character: str, unicode_version: str = "auto") -> int:
    """Get the cell size of a character.

    Args:
        character (str): A single character.
        unicode_version: Unicode version, `"auto"` to auto detect, `"latest"` for the latest unicode version.

    Returns:
        int: Number of cells (0, 1 or 2) occupied by that character.
    """
    codepoint = ord(character)
    table = load_cell_table(unicode_version).widths
    if codepoint < table[0][0] or codepoint > table[-1][1]:
        return 0
    lower_bound = 0
    upper_bound = len(table) - 1
    index = (lower_bound + upper_bound) // 2
    while True:
        start, end, width = table[index]
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


@lru_cache(4096)
def cached_cell_len(text: str) -> int:
    """Get the number of cells required to display text.

    This method always caches, which may use up a lot of memory. It is recommended to use
    `cell_len` over this method.

    Args:
        text (str): Text to display.

    Returns:
        int: Get the number of cells required to display text.
    """
    if _is_single_cell_widths(text):
        return len(text)
    return sum(map(get_character_cell_size, text))


def cell_len(text: str, unicode_version: str = "auto") -> int:
    """Get the cell length of a string (length as it appears in the terminal).

    Args:
        text: String to measure.
        unicode_version: Unicode version, `"auto"` to auto detect, `"latest"` for the latest unicode version.

    Returns:
        Length of string in terminal cells.
    """

    if _is_single_cell_widths(text):
        return len(text)

    # "\u200d" is zero width joiner
    # "\ufe0f" is variation selector 16
    if "\u200d" not in text and "\ufe0f" not in text:
        # Simplest case with no unicode stuff that changes the size
        return sum(
            get_character_cell_size(character, unicode_version) for character in text
        )

    cell_table = load_cell_table(unicode_version)
    codepoint_count = len(text)
    total_width = 0
    index = 0
    last_measured_character: str | None = None

    SPECIAL = {"\u200d", "\ufe0f"}

    while index < codepoint_count:
        if (character := text[index]) in SPECIAL:
            if character == "\u200d":
                index += 2
            elif last_measured_character:
                total_width += last_measured_character in cell_table.narrow_to_wide
                last_measured_character = None
                index += 1
        else:
            if character_width := get_character_cell_size(character, unicode_version):
                last_measured_character = character
                total_width += character_width
            index += 1

    return total_width


def split_graphemes(
    text: str, unicode_version: str = "auto"
) -> "tuple[list[CellSpan], int]":
    """Divide text in to spans that define a single grapheme.

    Args:
        text: String to split.
        unicode_version: Unicode version, `"auto"` to auto detect, `"latest"` for the latest unicode version.

    Returns:
        List of spans.
    """

    cell_table = load_cell_table(unicode_version)
    codepoint_count = len(text)
    index = 0
    last_measured_character: str | None = None

    total_width = 0
    spans: list[tuple[int, int, int]] = []
    SPECIAL = {"\u200d", "\ufe0f"}
    while index < codepoint_count:
        if (character := text[index]) in SPECIAL:
            if character == "\u200d":
                # zero width joiner
                index += 2
                if spans:
                    start, _end, cell_length = spans[-1]
                    spans[-1] = (start, index, cell_length)
            elif last_measured_character:
                # variation selector 16
                index += 1
                if spans:
                    start, _end, cell_length = spans[-1]
                    if last_measured_character in cell_table.narrow_to_wide:
                        last_measured_character = None
                        cell_length += 1
                        total_width += 1
                    spans[-1] = (start, index, cell_length)
            continue

        if character_width := get_character_cell_size(character, unicode_version):
            last_measured_character = character
            spans.append((index, index := index + 1, character_width))
            total_width += character_width
        elif spans:
            # zero width characters are associated with the previous character
            start, _end, cell_length = spans[-1]
            spans[-1] = (start, index := index + 1, cell_length)

    return (spans, total_width)


def _split_text(
    text: str, cell_position: int, unicode_version: str = "auto"
) -> tuple[str, str]:
    """Split text by cell position.

    If the cell position falls within a double width character, it is converted to two spaces.

    Args:
        text: Text to split.
        cell_position Offset in cells.
        unicode_version: Unicode version, `"auto"` to auto detect, `"latest"` for the latest unicode version.

    Returns:
        Tuple to two split strings.
    """
    if cell_position == 0:
        return "", text

    spans, cell_length = split_graphemes(text, unicode_version)

    # Guess initial offset
    offset = int((cell_position / cell_length) * len(spans))
    left_size = sum(map(_span_get_cell_len, spans[:offset]))

    while True:
        if left_size == cell_position:
            split_index = spans[offset][0]
            return text[:split_index], text[split_index:]
        if left_size < cell_position:
            start, end, cell_size = spans[offset]
            if left_size + cell_size > cell_position:
                return text[:start] + " ", " " + text[end:]
            offset += 1
            left_size += cell_size
        else:
            start, end, cell_size = spans[offset]
            if left_size - cell_size < cell_position:
                return text[:start] + " ", " " + text[end:]
            offset -= 1
            left_size -= cell_size


def split_text(
    text: str, cell_position: int, unicode_version: str = "auto"
) -> tuple[str, str]:
    """Split text by cell position.

    If the cell position falls within a double width character, it is converted to two spaces.

    Args:
        text: Text to split.
        cell_position Offset in cells.
        unicode_version: Unicode version, `"auto"` to auto detect, `"latest"` for the latest unicode version.

    Returns:
        Tuple to two split strings.
    """
    if _is_single_cell_widths(text):
        return text[:cell_position], text[cell_position:]
    return _split_text(text, cell_position, unicode_version)


def set_cell_size(text: str, total: int, unicode_version: str = "auto") -> str:
    """Adjust a string by cropping or padding with spaces such that it fits within the given number of cells.

    Args:
        text: String to adjust.
        total: Desired size in cells.
        unicode_version: Unicode version.

    Returns:
        A string with cell size equal to total.
    """
    if _is_single_cell_widths(text):
        size = len(text)
        if size < total:
            return text + " " * (total - size)
        return text[:total]
    if total <= 0:
        return ""
    cell_size = cell_len(text)
    if cell_size == total:
        return text
    if cell_size < total:
        return text + " " * (total - cell_size)
    text, _ = _split_text(text, total, unicode_version)
    return text


def chop_cells(text: str, width: int, unicode_version: str = "auto") -> list[str]:
    """Split text into lines such that each line fits within the available (cell) width.

    Args:
        text: The text to fold such that it fits in the given width.
        width: The width available (number of cells).

    Returns:
        A list of strings such that each string in the list has cell width
        less than or equal to the available width.
    """
    if _is_single_cell_widths(text):
        return [text[index : index + width] for index in range(0, len(text), width)]
    spans, _ = split_graphemes(text, unicode_version)
    line_size = 0  # Size of line in cells
    lines: list[str] = []
    line_offset = 0  # Offset (in codepoints) of start of line
    for start, end, cell_size in spans:
        if line_size + cell_size > width:
            lines.append(text[line_offset:start])
            line_offset = start
            line_size = 0
        line_size += cell_size
    if line_size:
        lines.append(text[line_offset:])

    return lines


class CellString:
    """A string-like object that takes graphemes into account."""

    def __init__(
        self,
        text: str,
        *,
        cell_length: int | None = None,
        spans: "list[CellSpan] | None" = None,
        unicode_version: str = "auto",
    ):
        """

        Args:
            text: The plain text.
            cell_length: The cell length (as it appears in the terminal), if known.
            spans: List of spans which divide the text in to atomic units (single glyphs).
            unicode_version: Unicode version, `"auto"` to auto detect, `"latest"` for the latest unicode version.
        """
        self._text = text
        self._singles: bool = _is_single_cell_widths(text)
        if cell_length is None:
            self._cell_length = len(text) if self._singles else None
        else:
            self._cell_length = cell_length
        self._spans: "list[CellSpan] | None" = spans
        self._unicode_version = unicode_version

    @property
    def text(self) -> str:
        """The raw text."""
        return self._text

    @property
    def spans(self) -> "list[CellSpan]":
        if self._spans is None:
            if self._singles:
                self._spans = [
                    (index, index + 1, 1) for index in range(len(self._text))
                ]
            else:
                self._spans, self._cell_length = split_graphemes(
                    self._text, self._unicode_version
                )
        return self._spans

    @property
    def cell_length(self) -> int:
        """The 'cell' length (length as displayed in the terminal)."""
        if self._cell_length is None:
            self._cell_length = cell_len(self._text)
        return self._cell_length

    @property
    def glyphs(self) -> list[str]:
        """List of strings that make up atomic glyph."""
        text = self._text
        glyphs = [text[start:end] for start, end, _ in self.spans]
        return glyphs

    @property
    def glyph_widths(self) -> list[tuple[str, int]]:
        """List of strings that make up atomic glyph, and corresponding cell width."""
        text = self._text
        glyph_widths = [
            (text[start:end], cell_length) for start, end, cell_length in self.spans
        ]
        return glyph_widths

    def __bool__(self) -> bool:
        return bool(self._text)

    def __hash__(self) -> int:
        return hash(self._text)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CellString):
            return self._text == other._text
        return NotImplemented

    def __add__(self, other: "CellString") -> "CellString":
        if self._singles and other._singles:
            return CellString(self._text + other._text)
        spans: "list[CellSpan] | None"
        if self._spans is not None and other._spans is not None:
            self_length = len(self._text)
            spans = [
                *self._spans,
                *[
                    (start + self_length, end + self_length, cell_length)
                    for start, end, cell_length in other.spans
                ],
            ]
        else:
            spans = None
        return CellString(self._text + other._text, spans=spans)

    def __iter__(self) -> Iterator[str]:
        if self._singles:
            return iter(self._text)

        def iterate_text(text: str, spans: "list[CellSpan]") -> Generator[str]:
            """Generator for the"""
            for start, end, _ in spans:
                yield text[start:end]

        return iter(iterate_text(self._text, self.spans))

    def __reversed__(self) -> Iterator[str]:
        if self._singles:
            return reversed(self._text)

        def iterate_text(text: str, spans: "list[CellSpan]") -> Generator[str]:
            for start, end, _ in reversed(spans):
                yield text[start:end]

        return iter(iterate_text(self._text, self.spans))

    def __getitem__(self, index: int | slice) -> str:
        if self._singles:
            # Trivial case of single cell character strings
            return self._text[index]
        if isinstance(index, int):
            # Single span is easy
            start, end, _cell_length = self.spans[index]
            return self._text[start:end]

        start, stop, stride = index.indices(len(self.spans))
        if stride == 1:
            # Fast path for a stride of 1
            start_offset = self.spans[start][0]
            stop_offset = self.spans[stop][1]
            return self._text[start_offset:stop_offset]
        else:
            # More involved case of a stride > 1
            span_offset = start
            output: list[str] = []
            while span_offset <= stop:
                start_offset, end_offset, _ = self.spans[span_offset]
                output.append(self._text[start_offset:end_offset])
                span_offset += stride
            return "".join(output)


if __name__ == "__main__":
    from rich import print

    print(CellString("Hello World").glyphs)

    print(CellString("Female mechanic: 👩\u200d🔧").glyphs)
    print(CellString("Female mechanic: 👩\u200d🔧").glyph_widths)

    left, right = split_text("Hello 👩\u200d🔧 World", 9)
    print(repr(left))
    print(repr(right))
    print(left)
    print(right)
