from __future__ import annotations

from operator import itemgetter
from typing import Dict, Iterable, NamedTuple, Optional, List, Tuple, Union
from typing_extensions import Literal

from .console import Console, ConsoleOptions, RenderResult, RenderableType
from .style import Style
from .segment import Segment
from ._tools import iter_last, iter_first_last

JustifyValues = Optional[Literal["left", "center", "right", "full"]]


class Span(NamedTuple):
    """A marked up region in some text."""

    start: int
    end: int
    style: Union[str, Style]

    def __repr__(self) -> str:
        return f'<span {self.start}:{self.end} "{self.style}">'

    def __bool__(self) -> bool:
        return self.end > self.start

    def split(self, offset: int) -> Tuple[Span, Optional[Span]]:
        """Split a span in to 2 from a given offset."""

        if offset < self.start:
            return self, None
        if offset >= self.end:
            return self, None

        span1 = Span(self.start, min(self.end, offset), self.style)
        span2 = Span(span1.end, self.end, self.style)
        return span1, span2

    def overlaps(self, start: int, end: int) -> bool:
        """Check if a range overlaps this span.
        
        Args:
            start (int): Start offset.
            end (int): End offset.
        
        Returns:
            bool: True if stat and end overlaps this span, otherwise False.
        """
        return (
            (self.start <= end < self.end)
            or (self.start <= start < self.end)
            or (start <= self.start and end > self.end)
        )

    def move(self, offset: int) -> Span:
        """Move start and end by a given offset.
        
        Args:
            offset (int): Number of characters to add to start and end.
        
        Returns:
            TextSpan: A new TextSpan with adjusted position.
        """
        start, end, style = self
        return Span(start + offset, end + offset, style)

    def slice_text(self, text: str) -> str:
        """Slice the text according to the start and end offsets.
        
        Args:
            text (str): A string to slice.
        
        Returns:
            str: A slice of the original string.
        """
        return text[self.start : self.end]

    def right_crop(self, offset: int) -> Span:
        start, end, style = self
        if offset >= end:
            return self
        return Span(start, min(offset, end), style)


class Text:
    """Text with colored spans."""

    def __init__(
        self,
        text: str = "",
        style: Union[str, Style] = None,
        justify: JustifyValues = "left",
        end: str = "\n",
    ) -> None:
        self._text: List[str] = [text] if text else []
        self.style = style
        self.justify = justify
        self.end = end
        self._text_str: Optional[str] = text
        self._spans: List[Span] = []
        self._length: int = len(text)

    def __len__(self) -> int:
        return self._length

    def __bool__(self) -> bool:
        return bool(self._length)

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f"<text {self.text!r} {self._spans!r}>"

    @property
    def text(self) -> str:
        """Get the text as a single string."""
        if self._text_str is None:
            self._text_str = "".join(self._text)
        return self._text_str

    @text.setter
    def text(self, new_text: str) -> Text:
        """Set the text to a new value."""
        self._text[:] = [new_text]
        self._text_str = new_text
        new_length = len(new_text)
        if new_length < self._length:
            self._trim_spans()
        self._length = new_length
        return self

    @classmethod
    def from_segments(cls, segments: Iterable[Segment]) -> Text:
        """Convert segments in to a Text object for further processing.
        
        Args:
            segments (Iterable[Segment]): Segments from a rendered console object.
        
        Returns:
            Text: A new text instance.
        """

        text = Text(justify=None)
        append_span = text._spans.append
        append_text = text._text.append
        offset = 0
        for text_str, style in segments:
            span_length = len(text_str)
            append_span(Span(offset, offset + span_length, style or "none"))
            append_text(text_str)
            offset += span_length
            text._length += span_length
        text._text_str = None
        return text

    def copy(self) -> Text:
        """Return a copy of this instance."""
        copy_self = Text(self.text, style=self.style)
        copy_self._spans = self._spans[:]
        return copy_self

    def stylize(self, start: int, end: int, style: Union[str, Style]) -> None:
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
        self._spans.append(Span(max(0, start), min(length, end), style))

    def set_length(self, new_length: int) -> None:
        """Set new length of the text, clipping or padding is required."""
        length = len(self)
        if length == new_length:
            return
        if length < new_length:
            self.pad_right(new_length - length)
        else:
            text = self.text[:new_length]
            self.text = text
            new_spans = []
            for span in self._spans:
                if span.start >= new_length:
                    break
                new_spans.append(span.right_crop(new_length))
            self._spans[:] = new_spans

    def __console__(
        self, console: Console, options: ConsoleOptions
    ) -> Iterable[Segment]:
        lines = self.wrap(options.max_width, justify=self.justify)
        for line in lines:
            yield from self._render_line(line, console, options)

    def _render_line(
        self, line: Text, console: Console, options: ConsoleOptions
    ) -> Iterable[Segment]:
        """Render the rich text to the console.
        
        Args:
            console (Console): Console instance.
            options (ConsoleOptions): Console options.
        
        Returns:
            Iterable[Segment]: Result of render that may be written to the console.
        """

        text = line.text
        style_map: Dict[int, Style] = {}
        null_style = Style()

        def get_style(style: Union[str, Style]) -> Style:
            if isinstance(style, str):
                style = console.parse_style(style) or null_style
            return style

        style_map = {
            0: get_style(self.style or "none"),
            **{
                index + 1: get_style(span.style)
                for index, span in enumerate(line._spans)
            },
        }

        spans = [
            (0, False, 0),
            *((span.start, False, index + 1) for index, span in enumerate(line._spans)),
            *((span.end, True, index + 1) for index, span in enumerate(line._spans)),
            (len(text), True, 0),
        ]
        spans.sort(key=itemgetter(0, 1))

        stack: List[int] = [0]
        current_style = style_map[0]

        for (offset, leaving, style_id), (next_offset, _, _) in zip(spans, spans[1:]):
            style = style_map[style_id]
            if leaving:
                stack.remove(style_id)
                current_style = Style.combine(
                    style_map[_style_id] for _style_id in stack
                )
            else:
                stack.append(style_id)
                current_style = current_style.apply(style)

            if next_offset > offset:
                span_text = text[offset:next_offset]
                yield Segment(span_text, current_style)
        if self.end:
            yield Segment(self.end)

    @classmethod
    def join(cls, lines: Iterable[Text], join_str: str = "\n") -> Text:
        """Join lines in to a new text instance."""
        new_text = Text()
        new_text.text = join_str.join(text.text for text in lines)
        offset = 0
        join_length = len(join_str)
        extend = new_text._spans.extend
        for text in lines:
            extend(span.move(offset) for span in text._spans)
            offset += len(text) + join_length
        return new_text

    def join(self, lines: Iterable[Text]) -> Text:
        """Join text together."""
        new_text = Text()
        append = new_text.append
        for last, line in iter_last(lines):
            append(line)
            if not last:
                append(self)
        return new_text

    def _trim_spans(self) -> None:
        """Remove or modify any spans that are over the end of the text."""
        new_length = self._length
        spans: List[Span] = []
        append = spans.append
        for span in self._spans:
            if span.end < new_length:
                append(span)
                continue
            if span.start > new_length:
                continue
            append(span.right_crop(new_length))
        self._spans[:] = spans

    def pad_left(self, count: int, character: str = " ") -> None:
        """Pad the left with a given character.
        
        Args:
            count (int): Number of characters to pad.
            character (str, optional): Character to pad with. Defaults to " ".
        """
        assert len(character) == 1, "Character must be a string of length 1"
        if count:
            self.text = f"{character * count}{self.text}"
            self._spans[:] = [span.move(count) for span in self._spans]

    def pad_right(self, count: int, character: str = " ") -> None:
        """Pad the right with a given character.
        
        Args:
            count (int): Number of characters to pad.
            character (str, optional): Character to pad with. Defaults to " ".
        """
        assert len(character) == 1, "Character must be a string of length 1"
        if count:
            self.text = f"{self.text}{character * count}"

    def append(self, text: Union[Text, str], style: Union[str, Style] = None) -> None:
        """Add text with an optional style.
        
        Args:
            text (Union[Text, str]): A str or Text to append.
            style (str, optional): A style name. Defaults to None.
        """
        if isinstance(text, str):
            self._text.append(text)
            offset = len(self)
            text_length = len(text)
            if style is not None:
                self._spans.append(Span(offset, offset + text_length, style))
            self._length += text_length
            self._text_str = None
        else:
            if style is not None:
                raise ValueError("style must not be set if appending Text instance")
            text_length = self._length
            self._text.append(text.text)
            self._spans.extend(
                Span(start + text_length, end + text_length, style)
                for start, end, style in text._spans
            )
            self._length += len(text)
            self._text_str = None

    def split(self, separator="\n", include_separator: bool = False) -> List[Text]:
        """Split rich text in to lines, preserving styles.
        
        Args:
            separator (str, optional): String to split on. Defaults to "\n".
        
        Returns:
            List[RichText]: A list of rich text, one per line of the original.
        """
        assert separator, "separator must not be empty"

        text = self.text
        if separator not in text:
            return [self.copy()]
        if text.endswith(separator):
            text = text[: -len(separator)]
        offsets: List[int] = []
        append = offsets.append
        offset = 0
        while True:
            try:
                offset = text.index(separator, offset) + len(separator)
            except ValueError:
                break
            append(offset)
        lines = self.divide(offsets)
        if not include_separator:
            separator_length = len(separator)
            for line in lines:
                if line.text.endswith(separator):
                    line.right_crop(separator_length)
        return lines

    def divide(self, offsets: Iterable[int]) -> Lines:
        """Divide text in to a number of lines at given offsets.

        Args:
            offsets (Iterable[int]): Offsets used to divide text.
        
        Returns:
            Lines: New RichText instances between offsets.
        """

        if not offsets:
            line = self.copy()
            return Lines([line])

        text = self.text
        text_length = len(text)
        divide_offsets = [0, *offsets, text_length]
        line_ranges = list(zip(divide_offsets, divide_offsets[1:]))
        average_line_length = -(-text_length // len(line_ranges))

        new_lines = Lines(
            Text(text[start:end], style=self.style, justify=self.justify)
            for start, end in line_ranges
        )
        line_ranges = [
            (offset, offset + len(line))
            for offset, line in zip(divide_offsets, new_lines)
        ]

        for span in self._spans:
            if span.start >= text_length:
                continue
            line_index = span.start // average_line_length

            line_start, line_end = line_ranges[line_index]
            if span.start < line_start:
                while True:
                    line_index -= 1
                    line_start, line_end = line_ranges[line_index]
                    if span.end >= line_start:
                        break
            elif span.start > line_end:
                while True:
                    line_index += 1
                    line_start, line_end = line_ranges[line_index]
                    if span.start <= line_end:
                        break

            while True:
                span, new_span = span.split(line_end)
                new_lines[line_index]._spans.append(span.move(-line_start))
                if new_span is None:
                    break
                span = new_span
                line_index += 1
                if line_index >= len(line_ranges):
                    break
                line_start, line_end = line_ranges[line_index]

        return new_lines

    def right_crop(self, amount: int = 1) -> None:
        """Remove a number of characters from the end of the text."""
        self.text = self.text[:-amount]

    def wrap(self, width: int, justify: JustifyValues = "left") -> Lines:
        """Word wrap the text.
        
        Args:
            width (int): Number of characters per line.
            justify (bool, optional): True to pad lines with spaces. Defaults to False.
        
        Returns:
            Lines: Number of lines.
        """
        lines: Lines = Lines()
        for line in self.split():
            text = line.text
            text_length = len(text)
            line_start = 0
            line_end = width
            offsets: List[int] = []
            while line_end < text_length:
                break_offset = text.rfind(" ", line_start, line_end)
                if break_offset != -1:
                    line_end = break_offset + 1
                line_start = line_end
                line_end = line_start + width
                offsets.append(line_start)
            new_lines = line.divide(offsets)
            if justify:
                new_lines.justify(width, align=justify)
            lines.extend(new_lines)
        return lines


class Lines(List[Text]):
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
                tokens = []
                index = 0
                for index, word in enumerate(words):
                    tokens.append(word)
                    if index < len(spaces):
                        tokens.append(Text(" " * spaces[index]))
                    index += 1
                self[line_index] = Text("").join(tokens)


if __name__ == "__main__":
    console = Console(markup=None)
    text = Text("Hello, World! 1 2 3", justify=None)
    text.stylize(1, 10, "bold")
    text.stylize(7, 17, "underline")
    print(repr(text))
    console.print(text)

    words = text.split(" ")
    # for word in words:
    #     console.print(word)
    # print(repr(words))

    console.print(text)

    j = Text(" ").join(words)
    console.print(j)
