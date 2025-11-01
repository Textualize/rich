from itertools import zip_longest
import re
from typing import (
    TYPE_CHECKING,
    Iterable,
    Iterator,
    List,
    Optional,
    TypeVar,
    Union,
    overload,
)

if TYPE_CHECKING:
    from .console import (
        Console,
        ConsoleOptions,
        JustifyMethod,
        OverflowMethod,
        RenderResult,
        RenderableType,
    )
    from .text import Text

from .cells import cell_len
from .measure import Measurement

T = TypeVar("T")


class Renderables:
    """A list subclass which renders its contents to the console."""

    def __init__(
        self, renderables: Optional[Iterable["RenderableType"]] = None
    ) -> None:
        self._renderables: List["RenderableType"] = (
            list(renderables) if renderables is not None else []
        )

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":
        """Console render method to insert line-breaks."""
        yield from self._renderables

    def __rich_measure__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "Measurement":
        dimensions = [
            Measurement.get(console, options, renderable)
            for renderable in self._renderables
        ]
        if not dimensions:
            return Measurement(1, 1)
        _min = max(dimension.minimum for dimension in dimensions)
        _max = max(dimension.maximum for dimension in dimensions)
        return Measurement(_min, _max)

    def append(self, renderable: "RenderableType") -> None:
        self._renderables.append(renderable)

    def __iter__(self) -> Iterable["RenderableType"]:
        return iter(self._renderables)


class Lines:
    """A list subclass which can render to the console."""

    def __init__(self, lines: Iterable["Text"] = ()) -> None:
        self._lines: List["Text"] = list(lines)

    def __repr__(self) -> str:
        return f"Lines({self._lines!r})"

    def __iter__(self) -> Iterator["Text"]:
        return iter(self._lines)

    @overload
    def __getitem__(self, index: int) -> "Text":
        ...

    @overload
    def __getitem__(self, index: slice) -> List["Text"]:
        ...

    def __getitem__(self, index: Union[slice, int]) -> Union["Text", List["Text"]]:
        return self._lines[index]

    def __setitem__(self, index: int, value: "Text") -> "Lines":
        self._lines[index] = value
        return self

    def __len__(self) -> int:
        return self._lines.__len__()

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":
        """Console render method to insert line-breaks."""
        yield from self._lines

    def append(self, line: "Text") -> None:
        self._lines.append(line)

    def extend(self, lines: Iterable["Text"]) -> None:
        self._lines.extend(lines)

    def pop(self, index: int = -1) -> "Text":
        return self._lines.pop(index)

    def justify(
        self,
        console: "Console",
        width: int,
        justify: "JustifyMethod" = "left",
        overflow: "OverflowMethod" = "fold",
    ) -> None:
        """Justify and overflow text to a given width.

        Args:
            console (Console): Console instance.
            width (int): Number of cells available per line.
            justify (str, optional): Default justify method for text: "left", "center", "full" or "right". Defaults to "left".
            overflow (str, optional): Default overflow for text: "crop", "fold", or "ellipsis". Defaults to "fold".

        """
        from .text import Text

        if justify == "left":
            for line in self._lines:
                line.truncate(width, overflow=overflow, pad=True)
        elif justify == "center":
            for line in self._lines:
                line.rstrip()
                line.truncate(width, overflow=overflow)
                line.pad_left((width - cell_len(line.plain)) // 2)
                line.pad_right(width - cell_len(line.plain))
        elif justify == "right":
            for line in self._lines:
                line.rstrip()
                line.truncate(width, overflow=overflow)
                line.pad_left(width - cell_len(line.plain))
        elif justify == "full":
            for line_index, line in enumerate(self._lines):
                # Don't full-justify the last line
                if line_index == len(self._lines) - 1:
                    break

                # Divide line into tokens of words and whitespace runs
                def _flatten_whitespace_spans() -> Iterable[int]:
                    for match in re.finditer(r"\s+", line.plain):
                        start, end = match.span()
                        yield start
                        yield end

                pieces: List[Text] = [p for p in line.divide(_flatten_whitespace_spans()) if p.plain != ""]

                # Identify indices of expandable single-space gaps (between words only)
                expandable_indices: List[int] = []
                for i, piece in enumerate(pieces):
                    if piece.plain == " ":
                        if 0 < i < len(pieces) - 1:
                            prev_is_word = not pieces[i - 1].plain.isspace()
                            next_is_word = not pieces[i + 1].plain.isspace()
                            if prev_is_word and next_is_word:
                                expandable_indices.append(i)

                # Compute extra spaces required to reach target width
                current_width = cell_len(line.plain)
                extra = max(0, width - current_width)

                # Distribute extra spaces from rightmost gap to left in round-robin
                increments: List[int] = [0] * len(pieces)
                if expandable_indices and extra:
                    rev_gaps = list(reversed(expandable_indices))
                    gi = 0
                    while extra > 0:
                        idx = rev_gaps[gi]
                        increments[idx] += 1
                        extra -= 1
                        gi = (gi + 1) % len(rev_gaps)

                # Rebuild tokens, preserving indentation blocks (whitespace runs > 1)
                tokens: List[Text] = []
                for i, piece in enumerate(pieces):
                    if piece.plain.isspace():
                        if piece.plain == " ":
                            # Single-space gap: expand according to increments
                            add = increments[i]
                            if add:
                                # Determine style for the expanded gap based on adjacent word styles
                                left_style = pieces[i - 1].get_style_at_offset(console, -1) if i > 0 else line.style
                                right_style = pieces[i + 1].get_style_at_offset(console, 0) if i + 1 < len(pieces) else line.style
                                space_style = left_style if left_style == right_style else line.style
                                tokens.append(Text(" " * (1 + add), style=space_style))
                            else:
                                tokens.append(piece)
                        else:
                            # Whitespace run (>1) treated as indentation/alignment block, preserve as-is
                            tokens.append(piece)
                    else:
                        tokens.append(piece)

                self[line_index] = Text("").join(tokens)
