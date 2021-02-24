from typing import Dict, NamedTuple, Optional

from .cells import cell_len, set_cell_size
from .style import Style

from itertools import filterfalse, zip_longest
from operator import attrgetter
from typing import Iterable, List, Tuple


class Segment(NamedTuple):
    """A piece of text with associated style. Segments are produced by the Console render process and
    are ultimately converted in to strings to be written to the terminal.

    Args:
        text (str): A piece of text.
        style (:class:`~rich.style.Style`, optional): An optional style to apply to the text.
        is_control (bool, optional): Boolean that marks segment as containing non-printable control codes.
    """

    text: str = ""
    """Raw text."""
    style: Optional[Style] = None
    """An optional style."""
    is_control: bool = False
    """True if the segment contains control codes, otherwise False."""

    def __repr__(self) -> str:
        """Simplified repr."""
        if self.is_control:
            return f"Segment.control({self.text!r}, {self.style!r})"
        else:
            return f"Segment({self.text!r}, {self.style!r})"

    def __bool__(self) -> bool:
        """Check if the segment contains text."""
        return bool(self.text)

    @property
    def cell_length(self) -> int:
        """Get cell length of segment."""
        return 0 if self.is_control else cell_len(self.text)

    @classmethod
    def control(cls, text: str, style: Optional[Style] = None) -> "Segment":
        """Create a Segment with control codes.

        Args:
            text (str): Text containing non-printable control codes.
            style (Optional[style]): Optional style.

        Returns:
            Segment: A Segment instance with ``is_control=True``.
        """
        return cls(text, style, is_control=True)

    @classmethod
    def make_control(cls, segments: Iterable["Segment"]) -> Iterable["Segment"]:
        """Convert all segments in to control segments.

        Returns:
            Iterable[Segments]: Segments with is_control=True
        """
        return [cls(text, style, True) for text, style, _ in segments]

    @classmethod
    def line(cls, is_control: bool = False) -> "Segment":
        """Make a new line segment."""
        return cls("\n", is_control=is_control)

    @classmethod
    def apply_style(
        cls,
        segments: Iterable["Segment"],
        style: Style = None,
        post_style: Style = None,
    ) -> Iterable["Segment"]:
        """Apply style(s) to an iterable of segments.

        Returns an iterable of segments where the style is replaced by ``style + segment.style + post_style``.

        Args:
            segments (Iterable[Segment]): Segments to process.
            style (Style, optional): Base style. Defaults to None.
            post_style (Style, optional): Style to apply on top of segment style. Defaults to None.

        Returns:
            Iterable[Segments]: A new iterable of segments (possibly the same iterable).
        """
        if style:
            apply = style.__add__
            segments = (
                cls(text, None if is_control else apply(_style), is_control)
                for text, _style, is_control in segments
            )
        if post_style:
            segments = (
                cls(
                    text,
                    None
                    if is_control
                    else (_style + post_style if _style else post_style),
                    is_control,
                )
                for text, _style, is_control in segments
            )
        return segments

    @classmethod
    def filter_control(
        cls, segments: Iterable["Segment"], is_control=False
    ) -> Iterable["Segment"]:
        """Filter segments by ``is_control`` attribute.

        Args:
            segments (Iterable[Segment]): An iterable of Segment instances.
            is_control (bool, optional): is_control flag to match in search.

        Returns:
            Iterable[Segment]: And iterable of Segment instances.

        """
        if is_control:
            return filter(attrgetter("is_control"), segments)
        else:
            return filterfalse(attrgetter("is_control"), segments)

    @classmethod
    def split_lines(cls, segments: Iterable["Segment"]) -> Iterable[List["Segment"]]:
        """Split a sequence of segments in to a list of lines.

        Args:
            segments (Iterable[Segment]): Segments potentially containing line feeds.

        Yields:
            Iterable[List[Segment]]: Iterable of segment lists, one per line.
        """
        line: List[Segment] = []
        append = line.append

        for segment in segments:
            if "\n" in segment.text and not segment.is_control:
                text, style, _ = segment
                while text:
                    _text, new_line, text = text.partition("\n")
                    if _text:
                        append(cls(_text, style))
                    if new_line:
                        yield line
                        line = []
                        append = line.append
            else:
                append(segment)
        if line:
            yield line

    @classmethod
    def split_and_crop_lines(
        cls,
        segments: Iterable["Segment"],
        length: int,
        style: Style = None,
        pad: bool = True,
        include_new_lines: bool = True,
    ) -> Iterable[List["Segment"]]:
        """Split segments in to lines, and crop lines greater than a given length.

        Args:
            segments (Iterable[Segment]): An iterable of segments, probably
                generated from console.render.
            length (int): Desired line length.
            style (Style, optional): Style to use for any padding.
            pad (bool): Enable padding of lines that are less than `length`.

        Returns:
            Iterable[List[Segment]]: An iterable of lines of segments.
        """
        line: List[Segment] = []
        append = line.append

        adjust_line_length = cls.adjust_line_length
        new_line_segment = cls("\n")

        for segment in segments:
            if "\n" in segment.text and not segment.is_control:
                text, style, _ = segment
                while text:
                    _text, new_line, text = text.partition("\n")
                    if _text:
                        append(cls(_text, style))
                    if new_line:
                        cropped_line = adjust_line_length(
                            line, length, style=style, pad=pad
                        )
                        if include_new_lines:
                            cropped_line.append(new_line_segment)
                        yield cropped_line
                        del line[:]
            else:
                append(segment)
        if line:
            yield adjust_line_length(line, length, style=style, pad=pad)

    @classmethod
    def adjust_line_length(
        cls, line: List["Segment"], length: int, style: Style = None, pad: bool = True
    ) -> List["Segment"]:
        """Adjust a line to a given width (cropping or padding as required).

        Args:
            segments (Iterable[Segment]): A list of segments in a single line.
            length (int): The desired width of the line.
            style (Style, optional): The style of padding if used (space on the end). Defaults to None.
            pad (bool, optional): Pad lines with spaces if they are shorter than `length`. Defaults to True.

        Returns:
            List[Segment]: A line of segments with the desired length.
        """
        line_length = sum(segment.cell_length for segment in line)
        new_line: List[Segment]

        if line_length < length:
            if pad:
                new_line = line + [cls(" " * (length - line_length), style)]
            else:
                new_line = line[:]
        elif line_length > length:
            new_line = []
            append = new_line.append
            line_length = 0
            for segment in line:
                segment_length = segment.cell_length
                if line_length + segment_length < length or segment.is_control:
                    append(segment)
                    line_length += segment_length
                else:
                    text, segment_style, _ = segment
                    text = set_cell_size(text, length - line_length)
                    append(cls(text, segment_style))
                    break
        else:
            new_line = line[:]
        return new_line

    @classmethod
    def get_line_length(cls, line: List["Segment"]) -> int:
        """Get the length of list of segments.

        Args:
            line (List[Segment]): A line encoded as a list of Segments (assumes no '\\\\n' characters),

        Returns:
            int: The length of the line.
        """
        return sum(segment.cell_length for segment in line)

    @classmethod
    def get_shape(cls, lines: List[List["Segment"]]) -> Tuple[int, int]:
        """Get the shape (enclosing rectangle) of a list of lines.

        Args:
            lines (List[List[Segment]]): A list of lines (no '\\\\n' characters).

        Returns:
            Tuple[int, int]: Width and height in characters.
        """
        get_line_length = cls.get_line_length
        max_width = max(get_line_length(line) for line in lines) if lines else 0
        return (max_width, len(lines))

    @classmethod
    def set_shape(
        cls,
        lines: List[List["Segment"]],
        width: int,
        height: int = None,
        style: Style = None,
        new_lines: bool = False,
    ) -> List[List["Segment"]]:
        """Set the shape of a list of lines (enclosing rectangle).

        Args:
            lines (List[List[Segment]]): A list of lines.
            width (int): Desired width.
            height (int, optional): Desired height or None for no change.
            style (Style, optional): Style of any padding added. Defaults to None.
            new_lines (bool, optional): Padded lines should include "\n". Defaults to False.

        Returns:
            List[List[Segment]]: New list of lines that fits width x height.
        """
        if height is None:
            height = len(lines)
        shaped_lines: List[List[Segment]] = []
        pad_line = (
            [Segment(" " * width, style), Segment("\n")]
            if new_lines
            else [Segment(" " * width, style)]
        )

        append = shaped_lines.append
        adjust_line_length = cls.adjust_line_length
        line: Optional[List[Segment]]
        iter_lines = iter(lines)
        for _ in range(height):
            line = next(iter_lines, None)
            if line is None:
                append(pad_line)
            else:
                append(adjust_line_length(line, width, style=style))
        return shaped_lines

    @classmethod
    def simplify(cls, segments: Iterable["Segment"]) -> Iterable["Segment"]:
        """Simplify an iterable of segments by combining contiguous segments with the same style.

        Args:
            segments (Iterable[Segment]): An iterable of segments.

        Returns:
            Iterable[Segment]: A possibly smaller iterable of segments that will render the same way.
        """
        iter_segments = iter(segments)
        try:
            last_segment = next(iter_segments)
        except StopIteration:
            return

        _Segment = Segment
        for segment in iter_segments:
            if last_segment.style == segment.style and not segment.is_control:
                last_segment = _Segment(
                    last_segment.text + segment.text, last_segment.style
                )
            else:
                yield last_segment
                last_segment = segment
        yield last_segment

    @classmethod
    def strip_links(cls, segments: Iterable["Segment"]) -> Iterable["Segment"]:
        """Remove all links from an iterable of styles.

        Args:
            segments (Iterable[Segment]): An iterable segments.

        Yields:
            Segment: Segments with link removed.
        """
        for segment in segments:
            if segment.is_control or segment.style is None:
                yield segment
            else:
                text, style, _is_control = segment
                yield cls(text, style.update_link(None) if style else None)

    @classmethod
    def strip_styles(cls, segments: Iterable["Segment"]) -> Iterable["Segment"]:
        """Remove all styles from an iterable of segments.

        Args:
            segments (Iterable[Segment]): An iterable segments.

        Yields:
            Segment: Segments with styles replace with None
        """
        for text, _style, is_control in segments:
            yield cls(text, None, is_control)

    @classmethod
    def remove_color(cls, segments: Iterable["Segment"]) -> Iterable["Segment"]:
        """Remove all color from an iterable of segments.

        Args:
            segments (Iterable[Segment]): An iterable segments.

        Yields:
            Segment: Segments with colorless style.
        """

        cache: Dict[Style, Style] = {}
        for text, style, is_control in segments:
            if style:
                colorless_style = cache.get(style)
                if colorless_style is None:
                    colorless_style = style.without_color
                    cache[style] = colorless_style
                yield cls(text, colorless_style, is_control)
            else:
                yield cls(text, None, is_control)


if __name__ == "__main__":  # pragma: no cover
    from rich.syntax import Syntax
    from rich.text import Text
    from rich.console import Console

    code = """from rich.console import Console
console = Console()
text = Text.from_markup("Hello, [bold magenta]World[/]!")
console.print(text)"""

    text = Text.from_markup("Hello, [bold magenta]World[/]!")

    console = Console()

    console.rule("rich.Segment")
    console.print(
        "A Segment is the last step in the Rich render process before gemerating text with ANSI codes."
    )
    console.print("\nConsider the following code:\n")
    console.print(Syntax(code, "python", line_numbers=True))
    console.print()
    console.print(
        "When you call [b]print()[/b], Rich [i]renders[/i] the object in to the the following:\n"
    )
    fragments = list(console.render(text))
    console.print(fragments)
    console.print()
    console.print("The Segments are then processed to produce the following output:\n")
    console.print(text)
    console.print(
        "\nYou will only need to know this if you are implementing your own Rich renderables."
    )
