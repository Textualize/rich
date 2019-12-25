from typing import NamedTuple, Optional

from .style import Style

from itertools import zip_longest
from typing import Iterable, List, Tuple


class Segment(NamedTuple):
    """A piece of text with associated style."""

    text: str
    style: Optional[Style] = None

    def __repr__(self) -> str:
        """Simplified repr."""
        return f"Segment({self.text!r}, {self.style!r})"

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
        return (cls(text, apply(style)) for text, style in segments)

    @classmethod
    def split_and_crop_lines(
        cls, segments: Iterable["Segment"], length: int, style: Style = None
    ) -> Iterable[List["Segment"]]:
        """Split segments in to lines, and crop lines greater than a given length.
        
        Args:
            segments (Iterable[Segment]): An iterable of segments, probably 
                generated from console.render.
            length (Optional[int]): Desired line length.           
        
        Returns:
            Iterable[List[Segment]]: An iterable of lines of segments.
        """
        lines: List[List[Segment]] = [[]]
        append = lines[-1].append

        for segment in segments:
            if "\n" in segment.text:
                text, style = segment
                while text:
                    _text, new_line, text = text.partition("\n")
                    if _text:
                        append(cls(_text, style))
                    if new_line:
                        yield cls.adjust_line_length(lines[-1], length, style=style)
                        lines.append([])
                        append = lines[-1].append
            else:
                append(segment)
        if lines[-1]:
            yield cls.adjust_line_length(lines[-1], length, style=style)

    @classmethod
    def adjust_line_length(
        cls, line: List["Segment"], length: int, style: Style = None
    ) -> List["Segment"]:
        """Adjust a line to a given width (cropping or padding as required.
        
        Args:
            segments (Iterable[Segment]): A list of segments in a single line.
            length (int): The desired width of the line.
            style (Style, optional): The style of padding if used (space on the end). Defaults to None.
        
        Returns:
            List[Segment]: A line of segments with the desired length.
        """
        line_length = sum(len(text) for text, _style in line)
        if line_length < length:
            return line[:] + [Segment(" " * (length - line_length), style)]
        elif line_length > length:
            line_length = 0
            new_line: List[Segment] = []
            append = new_line.append
            for segment in line:
                segment_length = len(segment.text)
                if line_length + segment_length < length:
                    append(segment)
                    line_length += segment_length
                else:
                    text, style = segment
                    append(Segment(text[: length - line_length], style))
                    break
            return new_line
        return line

    @classmethod
    def get_line_length(cls, line: List["Segment"]) -> int:
        r"""Get the length of list of segments.
        
        Args:
            line (List[Segment]): A line encoded as a list of Segments (assumes no '\n' characters),
        
        Returns:
            int: The length of the line.
        """
        return sum(len(text) for text, _ in line)

    @classmethod
    def get_shape(cls, lines: List[List["Segment"]]) -> Tuple[int, int]:
        """Get the shape (enclosing rectangle) of a list of lines
        
        Args:
            lines (List[List[Segment]]): A list of lines (no '\n' characters)
        
        Returns:
            Tuple[int, int]: Width and height in characters
        """
        get_line_length = cls.get_line_length
        max_width = max(get_line_length(line) for line in lines)
        return (max_width, len(lines))

    @classmethod
    def set_shape(
        cls,
        lines: List[List["Segment"]],
        width: int,
        height: int = None,
        style: Style = None,
    ) -> List[List["Segment"]]:
        """Set the shape of a list of lines (enclosing rectangle)
        
        Args:
            lines (List[List[Segment]]): A list of lines.
            width (int): Desired width.
            height (int, optional): Desired height or None for no change..
            style (Style, optional): Style of any padding added. Defaults to None.
        
        Returns:
            [type]: New list of lines that fits width x height.
        """
        if height is None:
            height = len(lines)
        new_lines: List[List[Segment]] = []
        pad_line = [Segment(" " * width, style)]
        append = new_lines.append
        adjust_line_length = cls.adjust_line_length
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
            if last_segment.style == segment.style:
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
