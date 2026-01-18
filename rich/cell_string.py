from typing import Callable, Generator, Iterator, NamedTuple, Sequence

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

# A set of characters that are a single cell wide
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
    narrow_to_wide: frozenset[int]

    def get_cell_size(self, character: str) -> None:
        pass


def get_character_cell_size(character: str, cell_table: CellTable | None) -> int:
    """Get the cell size of a character.

    Args:
        character (str): A single character.

    Returns:
        int: Number of cells (0, 1 or 2) occupied by that character.
    """
    codepoint = ord(character)
    _table = CELL_WIDTHS
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


def _bisearch(codepoint: int, table: Sequence[tuple[int, int, int]]) -> int:
    """Binary search a codepoint table.

    Args:
        codepoint: The codepoint of a character.
        table: A codepoint table.

    """
    lbound = 0
    ubound = len(table) - 1

    if codepoint < table[0][0] or codepoint > table[ubound][1]:
        return 0
    while ubound >= lbound:
        mid = (lbound + ubound) // 2
        if codepoint > table[mid][1]:
            lbound = mid + 1
        elif codepoint < table[mid][0]:
            ubound = mid - 1
        else:
            return 1

    return 0


def _binary_search(character: str) -> int:
    """Get the cell size of a character.

    Args:
        character (str): A single character.

    Returns:
        int: Number of cells (0, 1 or 2) occupied by that character.
    """
    codepoint = ord(character)
    _table = CELL_WIDTHS
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


class Span(NamedTuple):
    """Defines a range of a single grapheme."""

    start: int
    end: int
    cell_length: int


class CellString:
    """A string-like object that takes graphemes into account."""

    def __init__(
        self,
        text: str,
        *,
        cell_length: int | None = None,
        spans: list[Span] | None = None,
    ):
        """

        Args:
            text: The plain text.
            cell_length: The cell length (as it appears in the terminal), if known.
            spans: List of spans which divide the text in to atomic units (single glyphs).
        """
        self._text = text
        self._singles: bool = _is_single_cell_widths(text)
        if cell_length is None:
            self._cell_length = len(text) if self._singles else None
        else:
            self._cell_length = cell_length
        self._spans: list[Span] | None = spans

    @property
    def text(self) -> str:
        """The raw text."""
        return self._text

    @property
    def spans(self) -> list[Span]:
        if self._spans is not None:
            if self._singles:
                self._spans = [
                    Span(index, index + 1, 1) for index in range(len(self._text))
                ]
            else:
                # TODO:
                self._spans = []

        return self._spans

    @property
    def cell_length(self) -> int:
        if self._cell_length is None:
            self._cell_length = sum([cell_length for _, _, cell_length in self.spans])
        return self._cell_length

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
        spans: list[Span] | None
        if self._spans is not None and other._spans is not None:
            self_length = len(self._text)
            spans = [
                *self._spans,
                *[
                    Span(start + self_length, end + self_length, cell_length)
                    for start, end, cell_length in other.spans
                ],
            ]
        else:
            spans = None
        return CellString(self._text + other._text, spans=spans)

    def __iter__(self) -> Iterator[str]:
        if self._singles:
            return iter(self._text)

        def iterate_text(text: str, spans: list[Span]) -> Generator[str]:
            """Generator for the"""
            for start, end, _ in spans:
                yield text[start:end]

        return iter(iterate_text(self._text, self.spans))

    def __reversed__(self) -> Iterator[str]:
        if self._singles:
            return reversed(self._text)

        def iterate_text(text: str, spans: list[Span]):
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
            start_offset = self.spans[start]
            stop_offset = self.spans[stop]
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
