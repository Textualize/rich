from __future__ import annotations

from typing import NamedTuple, Optional

from .style import Style

from typing import Iterable, List


class Segment(NamedTuple):
    """A piece of text with associated style."""

    text: str
    style: Optional[Style] = None

    def __repr__(self) -> str:
        """Simplified repr."""
        return f"Segment({self.text!r}, {self.style!r})"

    @classmethod
    def apply_style(
        cls, segments: Iterable[Segment], style: Style = None
    ) -> Iterable[Segment]:
        """Apply a style to an iterable of segments.
        
        Args:
            segments (Iterable[Segment]): Segments to process.
            style (Style, optional): A style to apply. Defaults to None.
        
        Returns:
            Iterable[Segments]: A new iterable of segments (possibly the same iterable).
        """
        if style is None:
            return segments
        apply = style.apply
        return (cls(text, apply(style)) for text, style in segments)

    @classmethod
    def split_lines(
        cls, segments: Iterable[Segment], length: int
    ) -> Iterable[List[Segment]]:
        """Split segments in to lines.
        
        Args:
            segments (Iterable[Segment]): An iterable of segments, probably 
                generated from console.render.
            length (Optional[int]): Length of line, or None for no change.
        
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
                        yield cls.adjust_line_length(lines[-1], length)
                        lines.append([])
                        append = lines[-1].append
            else:
                append(segment)
        if lines[-1]:
            yield cls.adjust_line_length(lines[-1], length)
        return lines

    @classmethod
    def adjust_line_length(
        cls, line: List[Segment], width: int, style: Style = None
    ) -> List[Segment]:
        """Adjust a line to a given width (cropping or padding as required.
        
        Args:
            segments (Iterable[Segment]): A list of segments in a single line.
            width (int): The desired width of the line.
            style (Style, optional): The style of padding if used (space on the end). Defaults to None.
        
        Returns:
            List[Segment]: A line of segments with the desired length.
        """
        if style is None:
            style = Style()
        length = sum(len(text) for text, style in line)
        if length < width:
            return line[:] + [Segment(" " * (width - length), style)]
        elif length > width:
            line_length = 0
            new_line: List[Segment] = []
            for segment in line:
                if line_length + len(segment.text) < width:
                    new_line.append(segment)
                    line_length += len(segment.text)
                else:
                    text, style = segment
                    new_line.append(Segment(text[width - line_length :], style))
                    break
            return new_line
        return line[:]
