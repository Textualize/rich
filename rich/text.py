from operator import itemgetter
from typing import (
    Any,
    Dict,
    Iterable,
    NamedTuple,
    Optional,
    List,
    Tuple,
    TYPE_CHECKING,
    Union,
)
from typing_extensions import Literal

if TYPE_CHECKING:  # pragma: no cover
    from .console import (
        Console,
        ConsoleOptions,
        JustifyValues,
        RenderResult,
        RenderableType,
    )

from .containers import Lines
from .style import Style
from .segment import Segment
from ._render_width import RenderWidth
from ._tools import iter_last, iter_first_last


class Span(NamedTuple):
    """A marked up region in some text."""

    start: int
    end: int
    style: Union[str, Style]

    def __repr__(self) -> str:
        return f'<span {self.start}:{self.end} "{self.style}">'

    def __bool__(self) -> bool:
        return self.end > self.start

    def split(self, offset: int) -> Tuple["Span", Optional["Span"]]:
        """Split a span in to 2 from a given offset."""

        if offset < self.start:
            return self, None
        if offset >= self.end:
            return self, None

        start, end, style = self
        span1 = Span(start, min(end, offset), style)
        span2 = Span(span1.end, end, style)
        return span1, span2

    def move(self, offset: int) -> "Span":
        """Move start and end by a given offset.
        
        Args:
            offset (int): Number of characters to add to start and end.
        
        Returns:
            TextSpan: A new TextSpan with adjusted position.
        """
        start, end, style = self
        return Span(start + offset, end + offset, style)

    def right_crop(self, offset: int) -> "Span":
        """Crop the span at the given offset.
        
        Args:
            offset (int): A value between start and end.
        
        Returns:
            Span: A new (possibly smaller) span.
        """
        start, end, style = self
        if offset >= end:
            return self
        return Span(start, min(offset, end), style)


class Text:
    """Text with colored spans."""

    def __init__(
        self,
        text: str = "",
        style: Union[str, Style] = "none",
        word_wrap: bool = True,
        justify: "JustifyValues" = None,
        end: str = "\n",
    ) -> None:
        self._text: List[str] = [text] if text else []
        self.style = style
        self.word_wrap = word_wrap
        self.justify = justify
        self.end = end
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

    def __add__(self, other: Any) -> "Text":
        if isinstance(other, (str, Text)):
            result = self.copy()
            result.append(other)
            return result
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Text):
            return NotImplemented
        return self.text == other.text and self._spans == other._spans

    @classmethod
    def from_markup(cls, text: str, style: Union[str, Style] = "") -> "Text":
        """Create Text instance from markup.
        
        Args:
            text (str): A string containing console markup.
        
        Returns:
            Text: A Text instance with markup rendered.
        """
        from .markup import render

        return render(text, style)

    @property
    def text(self) -> str:
        """Get the text as a single string."""
        if len(self._text) not in (0, 1):
            text = "".join(self._text)
            self._text[:] = [text]
        return self._text[0] if self._text else ""

    @text.setter
    def text(self, new_text: str) -> "Text":
        """Set the text to a new value."""
        self._text[:] = [new_text]
        old_length = self._length
        self._length = len(new_text)
        if old_length > self._length:
            self._trim_spans()
        return self

    def copy(self) -> "Text":
        """Return a copy of this instance."""
        self.text
        copy_self = Text(
            self.text,
            style=self.style,
            word_wrap=self.word_wrap,
            justify=self.justify,
            end=self.end,
        )
        copy_self._spans[:] = self._spans[:]
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
            # span not in range
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
                if span.start < new_length:
                    new_spans.append(span.right_crop(new_length))
            self._spans[:] = new_spans

    def __console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> Iterable[Segment]:
        if self.word_wrap:
            lines = self.wrap(
                options.max_width, justify=self.justify or options.justify
            )
        else:
            lines = self.fit(options.max_width)

        all_lines = Text("\n").join(lines)
        yield from self._render_line(all_lines, console, options)

    def __console_width__(self, max_width: int) -> RenderWidth:
        text = self.text
        if not text.strip():
            return RenderWidth(len(text), len(text))
        max_text_width = max(len(line) for line in text.splitlines())
        min_text_width = max(len(word) for word in text.split())
        return RenderWidth(min_text_width, max_text_width)

    def _render_line(
        self, line: "Text", console: "Console", options: "ConsoleOptions"
    ) -> Iterable["Segment"]:
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
            return console.get_style(style, default=null_style)

        enumerated_spans = list(enumerate(line._spans, 1))
        style_map = {index: get_style(span.style) for index, span in enumerated_spans}
        style_map[0] = get_style(self.style)

        spans = [
            (0, False, 0),
            *((span.start, False, index) for index, span in enumerated_spans),
            *((span.end, True, index) for index, span in enumerated_spans),
            (len(text), True, 0),
        ]
        spans.sort(key=itemgetter(0, 1))

        stack: List[int] = []
        stack_append = stack.append
        stack_pop = stack.remove

        _Segment = Segment

        style_cache: Dict[Tuple[int, ...], Style] = {}
        combine = Style.combine

        def get_current_style() -> Style:
            """Construct current style from stack."""
            style_ids = tuple(sorted(stack))
            cached_style = style_cache.get(style_ids)
            if cached_style is not None:
                return cached_style
            current_style = combine(style_map[_style_id] for _style_id in style_ids)
            style_cache[style_ids] = current_style
            return current_style

        for (offset, leaving, style_id), (next_offset, _, _) in zip(spans, spans[1:]):
            if leaving:
                stack_pop(style_id)
            else:
                stack_append(style_id)
            if next_offset > offset:
                yield _Segment(text[offset:next_offset], get_current_style())
        if self.end:
            yield _Segment(self.end)

    def join(self, lines: Iterable["Text"]) -> "Text":
        """Join text together with this instance as the separator.
        
        Args:
            lines (Iterable[Text]): An iterable of Text instances to join.
        
        Returns:
            Text: A new text instance containing join text.
        """

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
            if span.start >= new_length:
                break
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

    def append(
        self, text: Union["Text", str], style: Union[str, "Style"] = None
    ) -> None:
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
        elif isinstance(text, Text):
            if style is not None:
                raise ValueError("style must not be set when appending Text instance")
            text_length = self._length
            if text.style is not None:
                self._spans.append(
                    Span(text_length, text_length + len(text), text.style),
                )
            self._text.append(text.text)
            self._spans.extend(
                Span(start + text_length, end + text_length, style)
                for start, end, style in text._spans
            )
            self._length += len(text)
        else:
            raise TypeError("Only str or Text can be appended to Text")

    def split(self, separator="\n", include_separator: bool = False) -> List["Text"]:
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

    def wrap(self, width: int, justify: "JustifyValues" = "left") -> Lines:
        """Word wrap the text.
        
        Args:
            width (int): Number of characters per line.
            justify (bool, optional): True to pad lines with spaces. Defaults to False.
        
        Returns:
            Lines: Number of lines.
        """
        assert width > 0, "width must be an integer >0"
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

    def fit(self, width: int) -> Lines:
        """Fit the text in to given width by chopping in to lines.
        
        Args:
            width (int): Maximum characters in a line.
        
        Returns:
            Lines: List of lines.
        """
        lines: Lines = Lines()
        append = lines.append
        for line in self.split():
            line.set_length(width)
            append(line)
        return lines


if __name__ == "__main__":  # pragma: no cover
    text = Text("Hello, World!")
    from .console import Console

    c = Console()
    c.print(text)

    text.stylize(0, 12, "bold red")
    text.stylize(0, 6, "not bold default")

    print(text._spans)

    c.print(text)

    c.print("[bold red]Danger Will Robinson[/bold red]")

    t = Text.from_markup("[magenta]wat")
    print(len(t))
    print(RenderWidth.get(t, 100))

