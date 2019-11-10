from __future__ import annotations

from operator import itemgetter
from typing import Iterable, NamedTuple, Optional, List
from typing_extensions import Literal

from .console import Console, ConsoleOptions, StyledText
from .style import Style


class TextSpan(NamedTuple):
    """A marked up region in some text."""

    start: int
    end: int
    style: str

    def adjust_offset(self, offset: int, max_length) -> TextSpan:
        """Get a new `TextSpan` with start and end adjusted.
        
        Args:
            offset (int): Number of characters to adjust offset by.
        
        Returns:
            TextSpan: A new text span.
        """
        return TextSpan(
            min(max_length, max(0, self.start + offset)),
            min(max_length, max(0, self.end + offset)),
            self.style,
        )

    def slice_text(self, text: str) -> str:
        """Slice the text according to the start and end offsets.
        
        Args:
            text (str): A string to slice.
        
        Returns:
            str: A slice of the original string.
        """
        return text[self.start : self.end]


class RichText:
    """Text with colored spans."""

    def __init__(
        self,
        text: str = "",
        wrap=True,
        align: Literal["left", "center", "right"] = "left",
    ) -> None:
        self._text: List[str] = [text]
        self._wrap = wrap
        self._align = align
        self._text_str: Optional[str] = text
        self._spans: List[TextSpan] = []
        self._length: int = len(text)

    def __len__(self) -> int:
        return self._length

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f"RichText({self.text!r})"

    def stylize(self, start: int, end: int, style: str) -> None:
        """Apply a style to a portion of the text.
        
        Args:
            start (int): Start offset.
            end (int): End offset.
            style (str): Style name to apply.
        
        Returns:
            None: 
        """
        length = len(self)
        if end < 0 or start > length:
            # span in range
            return
        self._spans.append(TextSpan(max(0, start), min(length, end), style))

    def __console_render__(
        self, console: Console, options: ConsoleOptions
    ) -> Iterable[StyledText]:
        """Render the rich text to the console.
        
        Args:
            console (Console): Console instance.
            options (ConsoleOptions): Console options.
        
        Returns:
            Iterable[StyledText]: An iterable of styled text.
        """

        text = self.text
        stack: List[Style] = []

        get_style = console.get_style
        null_style = Style()
        start_spans = (
            (span.start, True, get_style(span.style) or null_style)
            for span in self._spans
        )
        end_spans = (
            (span.end, False, get_style(span.style) or null_style)
            for span in self._spans
        )

        spans = [
            (0, True, null_style),
            *start_spans,
            *end_spans,
            (len(text), False, null_style),
        ]
        spans.sort(key=itemgetter(0))

        current_style = Style()
        for (offset, entering, style), (next_offset, _, _) in zip(spans, spans[1:]):
            if entering:
                stack.append(style)
                current_style = current_style.apply(style)
            else:
                stack.reverse()
                stack.remove(style)
                stack.reverse()
                current_style = Style.combine(stack)
            span_text = text[offset:next_offset]
            yield StyledText(span_text, current_style)

    @property
    def text(self) -> str:
        """Get the text as a single string."""
        if self._text_str is None:
            self._text_str = "".join(self._text)
        return self._text_str

    def append(self, text: str, style: str = None) -> None:
        """Add text with an optional style.
        
        Args:
            text (str): Text to append.
            style (str, optional): A style name. Defaults to None.
        """
        self._text.append(text)
        offset = len(self)
        text_length = len(text)
        self._spans.append(TextSpan(offset, offset + text_length, style or "none"))
        self._length += text_length
        self._text_str = None

    def split(self, separator="\n") -> List[RichText]:
        """Split rich text in to lines, preserving styles.
        
        Args:
            separator (str, optional): String to split on. Defaults to "\n".
        
        Returns:
            List[RichText]: A list of rich text, one per line of the original.
        """
        lines = self.text.split(separator)
        offset = 0
        offsets: List[int] = []
        offset_append = offsets.append
        for _line in lines:
            offset_append(offset)
            offset += len(_line) + len(separator)

        new_lines: List[RichText] = [RichText(line + separator) for line in lines]
        for span in self._spans:
            for offset, line in zip(offsets, new_lines):
                if span.end <= offset or span.start >= offset + len(line):
                    continue
                line._spans.append(span.adjust_offset(-offset, len(line)))

        return new_lines


if __name__ == "__main__":

    rich_text = RichText("0123456789012345")
    rich_text.stylize(0, 100, "dim")
    rich_text.stylize(0, 5, "bright")
    rich_text.stylize(2, 8, "bold")

    # rich_text.append("Hello\n", style="bold")
    # rich_text.append("World!\n", style="italic")
    # rich_text.append("1 2 3 ", style="red")
    # rich_text.append("4 5 6", style="green")

    console = Console()
    # for line in rich_text.split("\n"):
    #     console.print(line)

    console.print(rich_text)
