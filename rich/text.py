from __future__ import annotations

from operator import itemgetter
from typing import Iterable, NamedTuple, Optional, List, Tuple, Union
from typing_extensions import Literal

from .console import Console, ConsoleOptions, RenderResult, RenderableType
from .style import Style
from .segment import Segment

JustifyValues = Optional[Literal["left", "center", "right"]]


class TextSpan(NamedTuple):
    """A marked up region in some text."""

    start: int
    end: int
    style: Union[str, Style]

    def __repr__(self) -> str:
        return f'<textspan {self.start}:{self.end} "{self.style}">'

    def split(self, offset: int) -> Tuple[TextSpan, Optional[TextSpan]]:
        """Split a span in to 2 from a given offset."""

        if offset < self.start:
            return self, None
        if offset >= self.end:
            return self, None

        span1 = TextSpan(self.start, min(self.end, offset), self.style)
        span2 = TextSpan(span1.end, self.end, self.style)
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

    def adjust_offset(self, offset: int, max_length: int) -> TextSpan:
        """Get a new `TextSpan` with start and end adjusted.
        
        Args:
            offset (int): Number of characters to adjust offset by.
            max_length(int): Maximum length of new span.
        
        Returns:
            TextSpan: A new text span.
        """

        start, end, style = self
        start = max(0, start + offset)
        return TextSpan(start, min(start + max_length, max(0, end + offset)), style)

    def move(self, offset: int) -> TextSpan:
        """Move start and end by a given offset.
        
        Args:
            offset (int): Number of characters to add to start and end.
        
        Returns:
            TextSpan: A new TextSpan with adjusted position.
        """
        start, end, style = self
        return TextSpan(start + offset, end + offset, style)

    def slice_text(self, text: str) -> str:
        """Slice the text according to the start and end offsets.
        
        Args:
            text (str): A string to slice.
        
        Returns:
            str: A slice of the original string.
        """
        return text[self.start : self.end]

    def right_crop(self, offset: int) -> TextSpan:
        start, end, style = self
        if offset >= end:
            return self
        return TextSpan(start, min(offset, end), style)


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
        self._spans: List[TextSpan] = []
        self._length: int = len(text)

    def __len__(self) -> int:
        return self._length

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f"<text {self.text!r} {self._spans!r}>"

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
            append_span(TextSpan(offset, offset + span_length, style or "none"))
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
        self._spans.append(TextSpan(max(0, start), min(length, end), style))

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
        stack: List[Style] = []

        null_style = Style()

        def get_style(style: Union[str, Style]) -> Style:
            if isinstance(style, str):
                return console.parse_style(style) or Style()
            return style

        stack.append(get_style(line.style) if line.style is not None else Style())

        start_spans = (
            (span.start, True, get_style(span.style) or null_style)
            for span in line._spans
        )

        end_spans = (
            (span.end, False, get_style(span.style) or null_style)
            for span in line._spans
        )

        spans = [
            (0, True, null_style),
            *start_spans,
            *end_spans,
            (len(text), False, null_style),
        ]
        spans.sort(key=itemgetter(0, 1))

        current_style = stack[-1]

        for (offset, entering, _style), (next_offset, _, _) in zip(spans, spans[1:]):
            style = get_style(_style)

            if entering:
                stack.append(style)
                current_style = current_style.apply(style)
            else:
                stack.reverse()
                stack.remove(style)
                stack.reverse()
                current_style = Style.combine(stack)
            if next_offset > offset:
                span_text = text[offset:next_offset]
                yield Segment(span_text, current_style)

        # while stack:
        #     style = stack.pop()
        #     yield Segment("", style)
        if self.end:
            yield Segment(self.end)

    @classmethod
    def join(cls, lines: Iterable[Text]) -> Text:
        """Join lines in to a new text instance."""
        new_text = Text()
        new_text.text = "\n".join(line.text for line in lines)
        offset = 0
        for line in lines:
            new_text._spans.extend(span.move(offset) for span in line._spans)
            offset += len(line.text)
        return new_text

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
        self._length = len(new_text)
        return self

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

    def append(self, text: str, style: Union[str, Style] = None) -> None:
        """Add text with an optional style.
        
        Args:
            text (str): Text to append.
            style (str, optional): A style name. Defaults to None.
        """
        self._text.append(text)
        offset = len(self)
        text_length = len(text)
        if style is not None:
            self._spans.append(TextSpan(offset, offset + text_length, style))
        self._length += text_length
        self._text_str = None

    def split(self, separator="\n") -> List[Text]:
        """Split rich text in to lines, preserving styles.
        
        Args:
            separator (str, optional): String to split on. Defaults to "\n".
        
        Returns:
            List[RichText]: A list of rich text, one per line of the original.
        """
        assert separator, "separator must not be empty"

        text = self.text.rstrip("\n")
        if separator not in text:
            return [self.copy()]
        offsets: List[int] = []
        append = offsets.append
        offset = 0
        while True:
            try:
                offset = text.index(separator, offset) + len(separator)
            except ValueError:
                break
            append(offset)
        return self.divide(offsets)

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
            Text(text[start:end].rstrip(), style=self.style, justify=self.justify)
            for start, end in line_ranges
        )

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
        self, width: int, align: Literal["left", "center", "right"] = "left"
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


if __name__ == "__main__":
    text = """\
The main area where I think Django's models are missing out is the lack of type hinting (hardly surprising since Django pre-dates type hints). Adding type hints allows Mypy to detect bugs before you even run your code. It may only save you minutes each time, but multiply that by the number of code + run iterations you do each day, and it can save hours of development time. Multiply that by the lifetime of your project, and it could save weeks or months. A clear win.
""".rstrip()
    console = Console(width=50, markup=None)
    rtext = Text(text, style=Style.parse("on black"), justify=None)
    rtext.stylize(20, 60, "bold yellow")
    rtext.stylize(28, 36, "underline")
    rtext.stylize(259, 357, "yellow on blue")

    console.print(rtext)

    # lines = rtext.wrap(console.width, justify="left")
    # for line in lines:
    #     print(repr(line))
    # print("-" * 50)

    # with console.style(Style()):
    #     console.print(lines)

    from .panel import Panel

    print("--")
    panel = Panel(rtext)
    console.print(panel)

    p = Text("hello")
    console.print(Panel(p, style="yellow on blue"))

    # console.wrap(50)

# if __name__ == "__main__":

#     rich_text = RichText("0123456789012345")
#     rich_text.stylize(0, 100, "magenta")
#     rich_text.stylize(1, 5, "cyan")
#     rich_text.stylize(2, 8, "bold")


#     console = Console()

#     console.print(rich_text)

#     for line in rich_text.divide([4, 8]):
#         console.print(line)

#     for line in rich_text.split("3"):
#         console.print(line)
