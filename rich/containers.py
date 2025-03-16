from itertools import zip_longest
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

from itertools import zip_longest
from typing import TYPE_CHECKING, Iterable, Iterator, List, Optional, TypeVar, overload

if TYPE_CHECKING:
    from .console import Console, ConsoleOptions, JustifyMethod, OverflowMethod, RenderResult, RenderableType
    from .text import Text

from .cells import cell_len
from .measure import Measurement

T = TypeVar("T")


class Renderables:
    """A list subclass which renders its contents to the console."""

    def __init__(self, renderables: Optional[Iterable["RenderableType"]] = None) -> None:
        self._renderables = list(renderables) if renderables else []

    def __rich_console__(self, console: "Console", options: "ConsoleOptions") -> "RenderResult":
        yield from self._renderables

    def __rich_measure__(self, console: "Console", options: "ConsoleOptions") -> "Measurement":
        dimensions = [Measurement.get(console, options, r) for r in self._renderables]
        return Measurement(max((d.minimum for d in dimensions), default=1), max((d.maximum for d in dimensions), default=1))

    def append(self, renderable: "RenderableType") -> None:
        self._renderables.append(renderable)

    def __iter__(self) -> Iterator["RenderableType"]:
        return iter(self._renderables)


class Lines:
    """A list subclass which can render to the console."""

    def __init__(self, lines: Iterable["Text"] = ()) -> None:
        self._lines = list(lines)

    def __iter__(self) -> Iterator["Text"]:
        return iter(self._lines)

    @overload
    def __getitem__(self, index: int) -> "Text": ...
    
    @overload
    def __getitem__(self, index: slice) -> List["Text"]: ...

    def __getitem__(self, index: Union[int, slice]) -> Union["Text", List["Text"]]:
        return self._lines[index]

    def __setitem__(self, index: int, value: "Text") -> None:
        self._lines[index] = value

    def __len__(self) -> int:
        return len(self._lines)

    def __rich_console__(self, console: "Console", options: "ConsoleOptions") -> "RenderResult":
        yield from self._lines

    def append(self, line: "Text") -> None:
        self._lines.append(line)

    def extend(self, lines: Iterable["Text"]) -> None:
        self._lines.extend(lines)

    def pop(self, index: int = -1) -> "Text":
        return self._lines.pop(index)

    def justify(self, console: "Console", width: int, justify: "JustifyMethod" = "left", overflow: "OverflowMethod" = "fold") -> None:
        """Justify and overflow text to a given width."""
        from .text import Text

        for line in self._lines:
            line.rstrip()
            line.truncate(width, overflow=overflow)
            if justify == "center":
                padding = (width - cell_len(line.plain)) // 2
                line.pad_left(padding).pad_right(width - cell_len(line.plain))
            elif justify == "right":
                line.pad_left(width - cell_len(line.plain))
            elif justify == "full" and line is not self._lines[-1]:
                words = line.split(" ")
                words_size = sum(cell_len(w.plain) for w in words)
                spaces = [1] * (len(words) - 1)
                for i in range(width - words_size - len(spaces)):
                    spaces[-(i % len(spaces)) - 1] += 1

                tokens = []
                for i, (word, next_word) in enumerate(zip_longest(words, words[1:])):
                    tokens.append(word)
                    if i < len(spaces):
                        space_style = word.get_style_at_offset(console, -1) if word.get_style_at_offset(console, -1) == next_word.get_style_at_offset(console, 0) else line.style
                        tokens.append(Text(" " * spaces[i], style=space_style))
                self._lines[self._lines.index(line)] = Text("").join(tokens)
