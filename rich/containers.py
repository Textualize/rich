from typing import Iterator, Iterable, List, TypeVar, TYPE_CHECKING, Union
from typing_extensions import Literal

from .segment import Segment


if TYPE_CHECKING:
    from .console import (
        Console,
        ConsoleOptions,
        ConsoleRenderable,
        RenderResult,
        RenderableType,
    )
    from .text import Text

from ._render_width import RenderWidth

T = TypeVar("T")


class Renderables:
    """A list subclass which renders its contents to the console."""

    def __init__(self, renderables: Iterable["ConsoleRenderable"] = None) -> None:
        self._renderables: List["ConsoleRenderable"] = (
            list(renderables) if renderables is not None else []
        )

    def __console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":
        """Console render method to insert line-breaks."""
        yield from self._renderables

    def __console_width__(self, max_width: int) -> "RenderWidth":
        dimensions = [
            RenderWidth.get(renderable, max_width) for renderable in self._renderables
        ]
        _min = max(dimension.minimum for dimension in dimensions)
        _max = max(dimension.maximum for dimension in dimensions)
        return RenderWidth(_min, _max)

    def append(self, renderable: "ConsoleRenderable") -> None:
        self._renderables.append(renderable)

    def __iter__(self) -> Iterable["ConsoleRenderable"]:
        return iter(self._renderables)


class Lines:
    """A list subclass which can render to the console."""

    def __init__(self, lines: Iterable["Text"] = ()) -> None:
        self._lines: List["Text"] = list(lines)

    def __iter__(self) -> Iterator["Text"]:
        return iter(self._lines)

    def __getitem__(self, index: int) -> "Text":
        return self._lines[index]

    def __setitem__(self, index: int, value: "Text") -> "Lines":
        self._lines[index] = value
        return self

    def __len__(self) -> int:
        return self._lines.__len__()

    def __console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":
        """Console render method to insert line-breaks."""
        for line in self._lines:
            yield line

    def append(self, line: "Text") -> None:
        self._lines.append(line)

    def extend(self, lines: Iterable["Text"]) -> None:
        self._lines.extend(lines)

    def justify(
        self,
        width: int,
        align: Literal["none", "left", "center", "right", "full"] = "left",
    ) -> None:
        """Pad each line with spaces to a given width.
        
        Args:
            width (int): Number of characters per line.
            
        """
        from .text import Text

        if align == "left":
            for line in self._lines:
                line.pad_right(width - len(line.text))
        elif align == "center":
            for line in self._lines:
                line.pad_left((width - len(line.text)) // 2)
                line.pad_right(width - len(line.text))
        elif align == "right":
            for line in self._lines:
                line.pad_left(width - len(line.text))
        elif align == "full":
            for line_index, line in enumerate(self._lines):
                if line_index == len(self._lines) - 1:
                    break
                words = line.split(" ")
                words_size = sum(len(word) for word in words)
                num_spaces = len(words) - 1
                spaces = [1 for _ in range(num_spaces)]
                index = 0
                while words_size + num_spaces < width:
                    spaces[len(spaces) - index - 1] += 1
                    num_spaces += 1
                    index = (index + 1) % len(spaces)
                tokens: List[Text] = []
                index = 0
                for index, word in enumerate(words):
                    tokens.append(word)
                    if index < len(spaces):
                        tokens.append(Text(" " * spaces[index]))
                    index += 1
                self[line_index] = Text("").join(tokens)
