from enum import IntEnum

from typing import Dict, NamedTuple, Optional

from .cells import cell_len, set_cell_size
from .style import Style

from itertools import filterfalse
from operator import attrgetter
from typing import cast, Iterable, List, Sequence, Union, Tuple, TYPE_CHECKING


if TYPE_CHECKING:
    from .console import Console, ConsoleOptions, RenderResult


class ControlType(IntEnum):
    """Non-printable control codes which typically translate to ANSI codes."""

    BELL = 1
    CARRIAGE_RETURN = 2
    HOME = 3
    CLEAR = 4
    SHOW_CURSOR = 5
    HIDE_CURSOR = 6
    ENABLE_ALT_SCREEN = 7
    DISABLE_ALT_SCREEN = 8
    CURSOR_UP = 9
    CURSOR_DOWN = 10
    CURSOR_FORWARD = 11
    CURSOR_BACKWARD = 12
    CURSOR_MOVE_TO_COLUMN = 13
    CURSOR_MOVE_TO = 14
    ERASE_IN_LINE = 15


ControlCode = Union[
    Tuple[ControlType], Tuple[ControlType, int], Tuple[ControlType, int, int]
]


class Segment(NamedTuple):
    """A piece of text with associated style. Segments are produced by the Console render process and
    are ultimately converted in to strings to be written to the terminal.

    Args:
        text (str): A piece of text.
        style (:class:`~rich.style.Style`, optional): An optional style to apply to the text.
        control (Tuple[ControlCode..], optional): Optional sequence of control codes.
    """

    text: str = ""
    """Raw text."""
    style: Optional[Style] = None
    """An optional style."""
    control: Optional[Sequence[ControlCode]] = None
    """Optional sequence of control codes."""

    def __repr__(self) -> str:
        """Simplified repr."""
        if self.control:
            return f"Segment({self.text!r}, {self.style!r}, {self.control!r})"
        else:
            return f"Segment({self.text!r}, {self.style!r})"

    def __bool__(self) -> bool:
        """Check if the segment contains text."""
        return bool(self.text)

    @property
    def cell_length(self) -> int:
        """Get cell length of segment."""
        return 0 if self.control else cell_len(self.text)

    @property
    def is_control(self) -> bool:
        """Check if the segment contains control codes."""
        return self.control is not None

    @classmethod
    def line(cls) -> "Segment":
        """Make a new line segment."""
        return cls("\n")

    @classmethod
    def apply_style(
        cls,
        segments: Iterable["Segment"],
        style: Optional[Style] = None,
        post_style: Optional[Style] = None,
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
                cls(text, None if control else apply(_style), control)
                for text, _style, control in segments
            )
        if post_style:
            segments = (
                cls(
                    text,
                    None
                    if control
                    else (_style + post_style if _style else post_style),
                    control,
                )
                for text, _style, control in segments
            )
        return segments

    @classmethod
    def filter_control(
        cls, segments: Iterable["Segment"], is_control: bool = False
    ) -> Iterable["Segment"]:
        """Filter segments by ``is_control`` attribute.

        Args:
            segments (Iterable[Segment]): An iterable of Segment instances.
            is_control (bool, optional): is_control flag to match in search.

        Returns:
            Iterable[Segment]: And iterable of Segment instances.

        """
        if is_control:
            return filter(attrgetter("control"), segments)
        else:
            return filterfalse(attrgetter("control"), segments)

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
            if "\n" in segment.text and not segment.control:
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
        style: Optional[Style] = None,
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
            if "\n" in segment.text and not segment.control:
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
        cls,
        line: List["Segment"],
        length: int,
        style: Optional[Style] = None,
        pad: bool = True,
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
                if line_length + segment_length < length or segment.control:
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
        height: Optional[int] = None,
        style: Optional[Style] = None,
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
            if last_segment.style == segment.style and not segment.control:
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
            if segment.control or segment.style is None:
                yield segment
            else:
                text, style, _control = segment
                yield cls(text, style.update_link(None) if style else None)

    @classmethod
    def strip_styles(cls, segments: Iterable["Segment"]) -> Iterable["Segment"]:
        """Remove all styles from an iterable of segments.

        Args:
            segments (Iterable[Segment]): An iterable segments.

        Yields:
            Segment: Segments with styles replace with None
        """
        for text, _style, control in segments:
            yield cls(text, None, control)

    @classmethod
    def remove_color(cls, segments: Iterable["Segment"]) -> Iterable["Segment"]:
        """Remove all color from an iterable of segments.

        Args:
            segments (Iterable[Segment]): An iterable segments.

        Yields:
            Segment: Segments with colorless style.
        """

        cache: Dict[Style, Style] = {}
        for text, style, control in segments:
            if style:
                colorless_style = cache.get(style)
                if colorless_style is None:
                    colorless_style = style.without_color
                    cache[style] = colorless_style
                yield cls(text, colorless_style, control)
            else:
                yield cls(text, None, control)


class Segments:
    """A simple renderable to render an iterable of segments. This class may be useful if
    you want to print segments outside of a __rich_console__ method.

    Args:
        segments (Iterable[Segment]): An iterable of segments.
        new_lines (bool, optional): Add new lines between segments. Defaults to False.
    """

    def __init__(self, segments: Sequence[Segment], new_lines: bool = False) -> None:
        self.segments = list(segments)
        self.new_lines = new_lines

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":
        if self.new_lines:
            line = Segment.line()
            for segment in self.segments:
                yield segment
                yield line
        else:
            yield from self.segments


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
        "A Segment is the last step in the Rich render process before generating text with ANSI codes."
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
