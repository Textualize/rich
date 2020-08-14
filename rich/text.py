import re
from operator import itemgetter
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Tuple,
    Union,
    cast,
)

from ._loop import loop_last
from ._pick import pick_bool
from ._wrap import divide_line
from .align import AlignValues
from .cells import cell_len, set_cell_size
from .containers import Lines
from .control import strip_control_codes
from .jupyter import JupyterMixin
from .measure import Measurement
from .segment import Segment
from .style import Style, StyleType

if TYPE_CHECKING:  # pragma: no cover
    from .console import (
        Console,
        ConsoleOptions,
        JustifyMethod,
        OverflowMethod,
    )

DEFAULT_JUSTIFY: "JustifyMethod" = "default"
DEFAULT_OVERFLOW: "OverflowMethod" = "fold"


_re_whitespace = re.compile(r"\s+$")

TextType = Union[str, "Text"]

GetStyleCallable = Callable[[str], Optional[StyleType]]


class Span(NamedTuple):
    """A marked up region in some text."""

    start: int
    """Span start index."""
    end: int
    """Span end index."""
    style: Union[str, Style]
    """Style associated with the span."""

    def __repr__(self) -> str:
        return f"Span({self.start}, {self.end}, {str(self.style)!r})"

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


class Text(JupyterMixin):
    """Text with color / style.
        
        Args:
            text (str, optional): Default unstyled text. Defaults to "".
            style (Union[str, Style], optional): Base style for text. Defaults to "".
            justify (str, optional): Justify method: "left", "center", "full", "right". Defaults to None.
            overflow (str, optional): Overflow method: "crop", "fold", "ellipsis". Defaults to None. 
            no_wrap (bool, optional): Disable text wrapping, or None for default. Defaults to None.
            end (str, optional): Character to end text with. Defaults to "\\n".
            tab_size (int): Number of spaces per tab, or ``None`` to use ``console.tab_size``. Defaults to 8.
            spans (List[Span], optional). A list of predefined style spans. Defaults to None.
    """

    __slots__ = [
        "_text",
        "style",
        "justify",
        "overflow",
        "no_wrap",
        "end",
        "tab_size",
        "_spans",
        "_length",
    ]

    def __init__(
        self,
        text: str = "",
        style: Union[str, Style] = "",
        *,
        justify: "JustifyMethod" = None,
        overflow: "OverflowMethod" = None,
        no_wrap: bool = None,
        end: str = "\n",
        tab_size: Optional[int] = 8,
        spans: List[Span] = None,
    ) -> None:
        self._text = [strip_control_codes(text)]
        self.style = style
        self.justify = justify
        self.overflow = overflow
        self.no_wrap = no_wrap
        self.end = end
        self.tab_size = tab_size
        self._spans: List[Span] = spans or []
        self._length: int = len(text)

    def __len__(self) -> int:
        return self._length

    def __bool__(self) -> bool:
        return bool(self._length)

    def __str__(self) -> str:
        return self.plain

    def __repr__(self) -> str:
        return f"<text {self.plain!r} {self._spans!r}>"

    def __add__(self, other: Any) -> "Text":
        if isinstance(other, (str, Text)):
            result = self.copy()
            result.append(other)
            return result
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Text):
            return NotImplemented
        return self.plain == other.plain and self._spans == other._spans

    def __contains__(self, other: object) -> bool:
        if isinstance(other, str):
            return other in self.plain
        elif isinstance(other, Text):
            return other.plain in self.plain
        return False

    @property
    def cell_len(self) -> int:
        """Get the number of cells required to render this text."""
        return cell_len(self.plain)

    @classmethod
    def from_markup(
        cls,
        text: str,
        *,
        style: Union[str, Style] = "",
        emoji: bool = True,
        justify: "JustifyMethod" = None,
        overflow: "OverflowMethod" = None,
    ) -> "Text":
        """Create Text instance from markup.
        
        Args:
            text (str): A string containing console markup.
            emoji (bool, optional): Also render emoji code. Defaults to True.
            justify (str, optional): Justify method: "left", "center", "full", "right". Defaults to None.
            overflow (str, optional): Overflow method: "crop", "fold", "ellipsis". Defaults to None. 
        
        Returns:
            Text: A Text instance with markup rendered.
        """
        from .markup import render

        rendered_text = render(text, style, emoji=emoji)
        rendered_text.justify = justify
        rendered_text.overflow = overflow
        return rendered_text

    @classmethod
    def styled(
        cls,
        text: str,
        style: StyleType = "",
        *,
        justify: "JustifyMethod" = None,
        overflow: "OverflowMethod" = None,
    ) -> "Text":
        """Construct a Text instance with a pre-applied styled. A style applied in this way won't be used
        to pad the text when it is justified.

        Args:
            text (str): A string containing console markup.
            style (Union[str, Style]): Style to apply to the text. Defaults to "".
            justify (str, optional): Justify method: "left", "center", "full", "right". Defaults to None.
            overflow (str, optional): Overflow method: "crop", "fold", "ellipsis". Defaults to None. 
        
        Returns:
            Text: A text instance with a style applied to the entire string.
        """
        styled_text = cls(text, justify=justify, overflow=overflow)
        styled_text.stylize(style)
        return styled_text

    @classmethod
    def assemble(
        cls,
        *parts: Union[str, "Text", Tuple[str, StyleType]],
        style: Union[str, Style] = "",
        justify: "JustifyMethod" = None,
        overflow: "OverflowMethod" = None,
        end: str = "\n",
        tab_size: int = 8,
    ) -> "Text":
        """Construct a text instance by combining a sequence of strings with optional styles.
        The positional arguments should be either strings, or a tuple of string + style.        

        Args:            
            style (Union[str, Style], optional): Base style for text. Defaults to "".
            justify (str, optional): Justify method: "left", "center", "full", "right". Defaults to None.
            overflow (str, optional): Overflow method: "crop", "fold", "ellipsis". Defaults to None. 
            end (str, optional): Character to end text with. Defaults to "\\n".
            tab_size (int): Number of spaces per tab, or ``None`` to use ``console.tab_size``. Defaults to 8.

        Returns:
            Text: A new text instance.
        """
        text = cls(
            style=style, justify=justify, overflow=overflow, end=end, tab_size=tab_size
        )
        append = text.append
        _Text = Text
        for part in parts:
            if isinstance(part, (_Text, str)):
                append(part)
            else:
                append(*part)
        return text

    @property
    def plain(self) -> str:
        """Get the text as a single string."""
        if len(self._text) != 1:
            self._text[:] = ["".join(self._text)]
        return self._text[0]

    @plain.setter
    def plain(self, new_text: str) -> None:
        """Set the text to a new value."""
        if new_text != self.plain:
            self._text[:] = [new_text]
            old_length = self._length
            self._length = len(new_text)
            if old_length > self._length:
                self._trim_spans()

    @property
    def spans(self) -> List[Span]:
        """Get a reference to the internal list of spans."""
        return self._spans

    @spans.setter
    def spans(self, spans: List[Span]) -> None:
        """Set spans."""
        self._spans = spans[:]

    def blank_copy(self) -> "Text":
        """Return a new Text instance with copied meta data (but not the string or spans)."""
        copy_self = Text(
            style=self.style,
            justify=self.justify,
            overflow=self.overflow,
            no_wrap=self.no_wrap,
            end=self.end,
            tab_size=self.tab_size,
        )
        return copy_self

    def copy(self) -> "Text":
        """Return a copy of this instance."""
        copy_self = Text(
            self.plain,
            style=self.style,
            justify=self.justify,
            overflow=self.overflow,
            no_wrap=self.no_wrap,
            end=self.end,
            tab_size=self.tab_size,
        )
        copy_self._spans[:] = self._spans
        return copy_self

    def stylize(
        self, style: Union[str, Style], start: int = 0, end: Optional[int] = None
    ) -> None:
        """Apply a style to the text, or a portion of the text.        

        Args:            
            style (Union[str, Style]): Style instance or style definition to apply.
            start (int): Start offset (negative indexing is supported). Defaults to 0.
            end (Optional[int], optional): End offset (negative indexing is supported), or None for end of text. Defaults to None.

        """
        length = len(self)
        if start < 0:
            start = length + start
        if end is None:
            end = length
        if end < 0:
            end = length + end
        if start >= length or end <= start:
            # Span not in text or not valid
            return
        self._spans.append(Span(start, min(length, end), style))

    def get_style_at_offset(self, console: "Console", offset: int) -> Style:
        """Get the style of a character at give offset.

        Args:
            console (~Console): Console where text will be rendered.
            offset (int): Offset in to text (negative indexing supported)

        Returns:
            Style: A Style instance.
        """
        if offset < 0:
            offset = len(self) + offset

        get_style = console.get_style
        style = console.get_style(self.style).copy()
        for start, end, span_style in self._spans:
            if offset >= start and offset < end:
                style += get_style(span_style)
        return style

    def highlight_regex(
        self,
        re_highlight: str,
        style: Union[GetStyleCallable, StyleType] = None,
        *,
        style_prefix: str = "",
    ) -> int:
        """Highlight text with a regular expression, where group names are
        translated to styles.

        Args:
            re_highlight (str): A regular expression.
            style (Union[GetStyleCallable, StyleType]): Optional style to apply to whole match, or a callable
                which accepts the matched text and returns a style. Defaults to None.
            style_prefix (str, optional): Optional prefix to add to style group names.            

        Returns:
            int: Number of regex matches
        """
        count = 0
        append_span = self._spans.append
        _Span = Span
        plain = self.plain
        for match in re.finditer(re_highlight, plain):
            get_span = match.span
            if style:
                start, end = get_span()
                match_style = style(plain[start:end]) if callable(style) else style
                if match_style is not None:
                    append_span(_Span(start, end, match_style))

            count += 1
            for name in match.groupdict().keys():
                start, end = get_span(name)
                if start != -1:
                    append_span(_Span(start, end, f"{style_prefix}{name}"))
        return count

    def highlight_words(
        self,
        words: Iterable[str],
        style: Union[str, Style],
        *,
        case_sensitive: bool = True,
    ) -> int:
        """Highlight words with a style.
        
        Args:
            words (Iterable[str]): Worlds to highlight.
            style (Union[str, Style]): Style to apply.
            case_sensitive (bool, optional): Enable case sensitive matchings. Defaults to True.
        
        Returns:
            int: Number of words highlighted.
        """
        re_words = "|".join(re.escape(word) for word in words)
        add_span = self._spans.append
        count = 0
        _Span = Span
        for match in re.finditer(
            re_words, self.plain, flags=0 if case_sensitive else re.IGNORECASE
        ):
            start, end = match.span(0)
            add_span(_Span(start, end, style))
            count += 1
        return count

    def rstrip(self) -> None:
        """Strip whitespace from end of text."""
        self.plain = self.plain.rstrip()

    def rstrip_end(self, size: int) -> None:
        """Remove whitespace beyond a certain width at the end of the text.

        Args:
            size (int): The desired size of the text.
        """
        text_length = len(self)
        if text_length > size:
            excess = text_length - size
            whitespace_match = _re_whitespace.search(self.plain)
            if whitespace_match is not None:
                whitespace_count = len(whitespace_match.group(0))
                self.plain = self.plain[: -min(whitespace_count, excess)]

    def set_length(self, new_length: int) -> None:
        """Set new length of the text, clipping or padding is required."""
        length = len(self)
        if length == new_length:
            return
        if length < new_length:
            self.pad_right(new_length - length)
        else:
            self.plain = self.plain[:new_length]

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> Iterable[Segment]:
        tab_size: int = console.tab_size or self.tab_size or 8  # type: ignore
        justify = cast(
            "JustifyMethod", self.justify or options.justify or DEFAULT_OVERFLOW
        )
        overflow = cast(
            "OverflowMethod", self.overflow or options.overflow or DEFAULT_OVERFLOW
        )

        lines = self.wrap(
            console,
            options.max_width,
            justify=justify,
            overflow=overflow,
            tab_size=tab_size or 8,
            no_wrap=pick_bool(self.no_wrap, options.no_wrap, False),
        )
        all_lines = Text("\n").join(lines)
        yield from all_lines.render(console, end=self.end)

    def __rich_measure__(self, console: "Console", max_width: int) -> Measurement:
        text = self.plain
        if not text.strip():
            return Measurement(cell_len(text), cell_len(text))
        max_text_width = max(cell_len(line) for line in text.splitlines())
        min_text_width = max(cell_len(word) for word in text.split())
        return Measurement(min_text_width, max_text_width)

    def render(self, console: "Console", end: str = "") -> Iterable["Segment"]:
        """Render the text as Segments.
        
        Args:
            console (Console): Console instance.  
            end (Optional[str], optional): Optional end character.          
        
        Returns:
            Iterable[Segment]: Result of render that may be written to the console.
        """

        text = self.plain
        style_map: Dict[int, Style] = {}
        null_style = Style()

        def get_style(style: Union[str, Style]) -> Style:
            return console.get_style(style, default=null_style)

        enumerated_spans = list(enumerate(self._spans, 1))

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
        if end:
            yield _Segment(end)

    def join(self, lines: Iterable["Text"]) -> "Text":
        """Join text together with this instance as the separator.
        
        Args:
            lines (Iterable[Text]): An iterable of Text instances to join.
        
        Returns:
            Text: A new text instance containing join text.
        """

        new_text = self.blank_copy()

        def iter_text() -> Iterable["Text"]:
            if self.plain:
                for last, line in loop_last(lines):
                    yield line
                    if not last:
                        yield self
            else:
                yield from lines

        extend_text = new_text._text.extend
        append_span = new_text._spans.append
        extend_spans = new_text._spans.extend
        offset = 0
        _Span = Span

        for text in iter_text():
            extend_text(text._text)
            if text.style is not None:
                append_span(_Span(offset, offset + len(text), text.style))
            extend_spans(
                _Span(offset + start, offset + end, style)
                for start, end, style in text._spans
            )
            offset += len(text)
        new_text._length = offset
        return new_text

    def tabs_to_spaces(self, tab_size: int = None) -> "Text":
        """Get a new string with tabs converted to spaces.
        
        Args:
            tab_size (int, optional): Size of tabs. Defaults to 8.

        Returns:
            Text: A new instance with tabs replaces by spaces.
        """
        if "\t" not in self.plain:
            return self.copy()
        parts = self.split("\t", include_separator=True)
        pos = 0
        if tab_size is None:
            tab_size = self.tab_size
        assert tab_size is not None
        result = self.blank_copy()
        append = result.append

        for part in parts:
            if part.plain.endswith("\t"):
                part._text = [part.plain[:-1] + " "]
                append(part)
                pos += len(part)
                spaces = tab_size - ((pos - 1) % tab_size) - 1
                if spaces:
                    append(" " * spaces, self.style)
                    pos += spaces
            else:
                append(part)
        return result

    def truncate(
        self,
        max_width: int,
        *,
        overflow: Optional["OverflowMethod"] = None,
        pad: bool = False,
    ) -> None:
        """Truncate text if it is longer that a given width.

        Args:
            max_width (int): Maximum number of characters in text.
            overflow (str, optional): Overflow method: "crop", "fold", or "ellipsis". Defaults to None, to use self.overflow.
            pad (bool, optional): Pad with spaces if the length is less than max_width. Defaults to False.
        """
        _overflow = overflow or self.overflow or DEFAULT_OVERFLOW
        if _overflow != "ignore":
            length = cell_len(self.plain)
            if length > max_width:
                if _overflow == "ellipsis":
                    self.plain = set_cell_size(self.plain, max_width - 1).rstrip() + "…"
                else:
                    self.plain = set_cell_size(self.plain, max_width)
            if pad and length < max_width:
                spaces = max_width - length
                self.plain = f"{self.plain}{' ' * spaces}"

    def _trim_spans(self) -> None:
        """Remove or modify any spans that are over the end of the text."""
        new_length = self._length
        spans: List[Span] = []
        append = spans.append
        _Span = Span
        for span in self._spans:
            if span.end < new_length:
                append(span)
                continue
            if span.start >= new_length:
                continue
            if span.end > new_length:
                start, end, style = span
                append(_Span(start, min(new_length, end), style))
            else:
                append(span)
        self._spans[:] = spans

    def pad(self, count: int, character: str = " ") -> None:
        """Pad left and right with a given number of characters.

        Args:
            count (int): Width of padding.
        """
        assert len(character) == 1, "Character must be a string of length 1"
        if count:
            pad_characters = character * count
            self.plain = f"{pad_characters}{self.plain}{pad_characters}"
            _Span = Span
            self._spans[:] = [
                _Span(start + count, end + count, style)
                for start, end, style in self._spans
            ]

    def pad_left(self, count: int, character: str = " ") -> None:
        """Pad the left with a given character.
        
        Args:
            count (int): Number of characters to pad.
            character (str, optional): Character to pad with. Defaults to " ".
        """
        assert len(character) == 1, "Character must be a string of length 1"
        if count:
            self.plain = f"{character * count}{self.plain}"
            _Span = Span
            self._spans[:] = [
                _Span(start + count, end + count, style)
                for start, end, style in self._spans
            ]

    def pad_right(self, count: int, character: str = " ") -> None:
        """Pad the right with a given character.
        
        Args:
            count (int): Number of characters to pad.
            character (str, optional): Character to pad with. Defaults to " ".
        """
        assert len(character) == 1, "Character must be a string of length 1"
        if count:
            self.plain = f"{self.plain}{character * count}"

    def align(self, align: AlignValues, width: int, character: str = " ") -> None:
        """Align text to a given width.

        Args:
            align (AlignValues): One of "left", "center", or "right".
            width (int): Desired width.
            character (str, optional): Character to pad with. Defaults to " ".
        """
        self.truncate(width)
        excess_space = width - cell_len(self.plain)
        if excess_space:
            if align == "left":
                self.pad_right(excess_space, character)
            elif align == "center":
                left = excess_space // 2
                self.pad_left(left, character)
                self.pad_right(excess_space - left, character)
            else:
                self.pad_left(excess_space, character)

    def append(
        self, text: Union["Text", str], style: Union[str, "Style"] = None
    ) -> "Text":
        """Add text with an optional style.
        
        Args:
            text (Union[Text, str]): A str or Text to append.
            style (str, optional): A style name. Defaults to None.
        
        Returns:
            Text: Returns self for chaining.
        """

        if not isinstance(text, (str, Text)):
            raise TypeError("Only str or Text can be appended to Text")

        if len(text):
            if isinstance(text, str):
                text = strip_control_codes(text)
                self._text.append(text)
                offset = len(self)
                text_length = len(text)
                if style is not None:
                    self._spans.append(Span(offset, offset + text_length, style))
                self._length += text_length
            elif isinstance(text, Text):
                _Span = Span
                if style is not None:
                    raise ValueError(
                        "style must not be set when appending Text instance"
                    )

                text_length = self._length
                if text.style is not None:
                    self._spans.append(
                        _Span(text_length, text_length + len(text), text.style)
                    )
                self._text.append(text.plain)
                self._spans.extend(
                    _Span(start + text_length, end + text_length, style)
                    for start, end, style in text._spans
                )
                self._length += len(text)
        return self

    def append_text(self, text: "Text") -> "Text":
        """Append another Text instance. This method is more performant that Text.append, but
        only works for Text.

        Returns:
            Text: Returns self for chaining.
        """
        _Span = Span
        text_length = self._length
        if text.style is not None:
            self._spans.append(_Span(text_length, text_length + len(text), text.style))
        self._text.append(text.plain)
        self._spans.extend(
            _Span(start + text_length, end + text_length, style)
            for start, end, style in text._spans
        )
        self._length += len(text)
        return self

    def copy_styles(self, text: "Text") -> None:
        """Copy styles from another Text instance.

        Args:
            text (Text): A Text instance to copy styles from, must be the same length.
        """
        self._spans.extend(text._spans)

    def split(
        self,
        separator="\n",
        *,
        include_separator: bool = False,
        allow_blank: bool = False,
    ) -> Lines:
        """Split rich text in to lines, preserving styles.
        
        Args:
            separator (str, optional): String to split on. Defaults to "\\n".
            include_separator (bool, optional): Include the separator in the lines. Defaults to False.
            allow_blank (bool, optional): Return a blank line if the text ends with a separator. Defaults to False.
        
        Returns:
            List[RichText]: A list of rich text, one per line of the original.
        """
        assert separator, "separator must not be empty"

        text = self.plain
        if separator not in text:
            return Lines([self.copy()])
        if not allow_blank and text.endswith(separator):
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
                if line.plain.endswith(separator):
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

        text = self.plain
        text_length = len(text)
        divide_offsets = [0, *offsets, text_length]
        line_ranges = list(zip(divide_offsets, divide_offsets[1:]))
        average_line_length = -(-text_length // len(line_ranges))

        new_lines = Lines(
            Text(
                text[start:end],
                style=self.style,
                justify=self.justify,
                overflow=self.overflow,
            )
            for start, end in line_ranges
        )
        line_ranges = [
            (offset, offset + len(line))
            for offset, line in zip(divide_offsets, new_lines)
        ]

        for span in self._spans:
            line_index = (span.start // average_line_length) % len(line_ranges)

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
                line_index = (line_index + 1) % len(line_ranges)
                line_start, line_end = line_ranges[line_index]

        return new_lines

    def right_crop(self, amount: int = 1) -> None:
        """Remove a number of characters from the end of the text."""
        self.plain = self.plain[:-amount]

    def wrap(
        self,
        console: "Console",
        width: int,
        *,
        justify: "JustifyMethod" = None,
        overflow: "OverflowMethod" = None,
        tab_size: int = 8,
        no_wrap: bool = None,
    ) -> Lines:
        """Word wrap the text.
        
        Args:
            console (Console): Console instance.
            width (int): Number of characters per line.
            emoji (bool, optional): Also render emoji code. Defaults to True.
            justify (str, optional): Justify method: "default", "left", "center", "full", "right". Defaults to "default".
            overflow (str, optional): Overflow method: "crop", "fold", or "ellipsis". Defaults to None.
            tab_size (int, optional): Default tab size. Defaults to 8.
            no_wrap (bool, optional): Disable wrapping, Defaults to False.
        
        Returns:
            Lines: Number of lines.
        """
        wrap_justify = cast("JustifyMethod", justify or self.justify or DEFAULT_JUSTIFY)
        wrap_overflow = cast(
            "OverflowMethod", overflow or self.overflow or DEFAULT_OVERFLOW
        )
        no_wrap = pick_bool(no_wrap, self.no_wrap, False) or overflow == "ignore"

        lines = Lines()
        for line in self.split(allow_blank=True):
            if "\t" in line:
                line = line.tabs_to_spaces(tab_size)
            if no_wrap:
                new_lines = Lines([line])
            else:
                offsets = divide_line(str(line), width, fold=wrap_overflow == "fold")
                new_lines = line.divide(offsets)
            for line in new_lines:
                line.rstrip_end(width)
            if wrap_justify:
                new_lines.justify(
                    console, width, justify=wrap_justify, overflow=wrap_overflow
                )
            for line in new_lines:
                line.truncate(width, overflow=wrap_overflow)
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
    from rich.console import Console

    console = Console()
    t = Text("foo bar", justify="left")
    print(repr(t.wrap(console, 4)))

    test = Text("Vulnerability CVE-2018-6543 detected")

    def get_style(text: str) -> str:
        return f"bold link https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={text}"

    test.highlight_regex(r"CVE-\d{4}-\d+", get_style)
    console.print(test)
