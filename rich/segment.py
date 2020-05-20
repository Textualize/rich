from typing import NamedTuple, Optional

from .cells import cell_len, set_cell_size
from .style import Style, StyleType

from itertools import filterfalse, zip_longest
from operator import attrgetter
from typing import Iterable, List, Tuple


class Segment(NamedTuple):
    """A piece of text with associated style.
    
    Args:
        text (str): A piece of text.
        style (:class:`~rich.style.Style`, optional): An optional style to apply to the text.
        is_control (bool, optional): Boolean that marks segment as containing non-printable control codes.
    """

    text: str = ""
    style: Optional[Style] = None
    is_control: bool = False

    def __repr__(self) -> str:
        """Simplified repr."""
        return f"Segment({self.text!r}, {self.style!r}, {self.is_control!r})"

    @property
    def cell_length(self) -> int:
        """Get cell length of segment."""
        return 0 if self.is_control else cell_len(self.text)

    @classmethod
    def control(self, text: str) -> "Segment":
        """Create a Segment with control codes.

        Args:
            text (str): Text containing non-printable control codes.

        Returns:
            Segment: A Segment instance with ``is_control=True``.
        """
        return Segment(text, is_control=True)

    @classmethod
    def line(self) -> "Segment":
        """Make a new line segment."""
        return Segment("\n")

    @classmethod
    def apply_style(
        cls, segments: Iterable["Segment"], style: Style = None
    ) -> Iterable["Segment"]:
        """Apply a style to an iterable of segments.

        Args:
            segments (Iterable[Segment]): Segments to process.
            style (Style, optional): A style to apply. Defaults to None.

        Returns:
            Iterable[Segments]: A new iterable of segments (possibly the same iterable).
        """
        if style is None:
            return segments
        apply = style.__add__
        return (
            cls(text, None if is_control else apply(style), is_control)
            for text, style, is_control in segments
        )

    @classmethod
    def filter_control(
        self, segments: Iterable["Segment"], is_control=False
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
                    text, style, _ = segment
                    text = set_cell_size(text, length - line_length)
                    append(cls(text, style))
                    break
        else:
            new_line = line[:]
        return new_line

    @classmethod
    def get_line_length(cls, line: List["Segment"]) -> int:
        r"""Get the length of list of segments.

        Args:
            line (List[Segment]): A line encoded as a list of Segments (assumes no '\n' characters),

        Returns:
            int: The length of the line.
        """
        return sum(segment.cell_length for segment in line)

    @classmethod
    def get_shape(cls, lines: List[List["Segment"]]) -> Tuple[int, int]:
        r"""Get the shape (enclosing rectangle) of a list of lines.

        Args:
            lines (List[List[Segment]]): A list of lines (no '\n' characters).

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
    ) -> List[List["Segment"]]:
        """Set the shape of a list of lines (enclosing rectangle).

        Args:
            lines (List[List[Segment]]): A list of lines.
            width (int): Desired width.
            height (int, optional): Desired height or None for no change.
            style (Style, optional): Style of any padding added. Defaults to None.

        Returns:
            List[List[Segment]]: New list of lines that fits width x height.
        """
        if height is None:
            height = len(lines)
        new_lines: List[List[Segment]] = []
        pad_line = [Segment(" " * width, style)]
        append = new_lines.append
        adjust_line_length = cls.adjust_line_length
        line: Optional[List[Segment]]
        for line, _ in zip_longest(lines, range(height)):
            if line is None:
                append(pad_line)
            else:
                append(adjust_line_length(line, width, style=style))
        return new_lines

    @classmethod
    def simplify(cls, segments: Iterable["Segment"]) -> Iterable["Segment"]:
        """Simplify an iterable of segments by combining contiguous segments with the same style.

        Args:
            segments (Iterable[Segment]): An iterable segments.

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


if __name__ == "__main__":  # pragma: no cover
    lines = [[Segment("Hello")]]
    lines = Segment.set_shape(lines, 50, 4, style=Style.parse("on blue"))
    for line in lines:
        print(line)

    print(Style.parse("on blue") + Style.parse("on red"))
