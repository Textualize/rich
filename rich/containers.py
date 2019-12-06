from __future__ import annotations

from typing import List, Literal, TypeVar, TYPE_CHECKING


from .console import (
    Console,
    ConsoleOptions,
    RenderResult,
    RenderableType,
)

from .segment import Segment

if TYPE_CHECKING:
    from .text import Text


T = TypeVar("T")


class Renderables(List[T]):
    """A list subclass which renders its contents to the console."""

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        """Console render method to insert line-breaks."""
        for renderable in self:
            yield renderable


class Lines(List["Text"]):
    """A list subclass which can render to the console."""

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        """Console render method to insert line-breaks."""
        for line in self:
            yield line
            yield Segment("\n")

    def justify(
        self, width: int, align: Literal["left", "center", "right", "full"] = "left"
    ) -> None:
        """Pad each line with spaces to a given width.
        
        Args:
            width (int): Number of characters per line.
            
        """
        from .text import Text

        if align == "left":
            for line in self:
                line.pad_right(width - len(line.text))
        elif align == "center":
            for line in self:
                line.pad_left((width - len(line.text)) // 2)
                line.pad_right(width - len(line.text))
        elif align == "right":
            for line in self:
                line.pad_left(width - len(line.text))
        elif align == "full":
            for line_index, line in enumerate(self):
                if line_index == len(self) - 1:
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
