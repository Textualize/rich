from __future__ import annotations

from typing import NamedTuple, Optional

from .style import Style

from typing import Iterable, List


class Styled(NamedTuple):
    """A piece of text with associated style."""

    text: str
    style: Optional[Style] = None

    def __repr__(self) -> str:
        """Simplified repr."""
        return f"Styled({self.text!r}, {self.style!r})"

    @classmethod
    def apply(
        cls, styled_text: Iterable[Styled], style: Style = None
    ) -> Iterable[Styled]:
        if style is None:
            return styled_text
        return (cls(text, style.apply(_style)) for text, _style in styled_text)

    @classmethod
    def split_lines(
        cls, styled_text: Iterable[Styled], length: int
    ) -> Iterable[List[Styled]]:
        """Split Styled text in to lines.
        
        Args:
            styled_text (Iterable[Styled]): An iterable of Styled text probably 
                generated from console.render.
            length (Optional[int]): Length of line, or None for no change.
        
        Returns:
            Iterable[List[Styled]]: An iterable of lines of Styled text.
        """
        lines: List[List[Styled]] = [[]]
        append = lines[-1].append
        for styled in styled_text:
            if "\n" in styled.text:
                text, style = styled
                while text:
                    _text, new_line, text = text.partition("\n")
                    if _text:
                        append(cls(_text, style))
                    if new_line:
                        yield cls.adjust_line_length(lines[-1], length)
                        lines.append([])
                        append = lines[-1].append
            else:
                append(styled)
        if lines[-1]:
            yield cls.adjust_line_length(lines[-1], length)
        return lines

    @classmethod
    def adjust_line_length(
        cls, line: List[Styled], width: int, style: Style = None
    ) -> List[Styled]:
        """Adjust a line to a given width (cropping or padding as required.
        
        Args:
            styled_text (Iterable[Styled]): A list of Styled text for a single line.
            width (int): The desired width of the line.
            style (Style, optional): The style of padding if used (space on the end). Defaults to None.
        
        Returns:
            List[Styled]: A line of Styled text with the desired length.
        """
        if style is None:
            style = Style()
        length = sum(len(text) for text, style in line)
        if length < width:
            return line[:] + [Styled(" " * (width - length), style)]
        elif length > width:
            line_length = 0
            new_line: List[Styled] = []
            for styled in line:
                if line_length + len(styled.text) < width:
                    new_line.append(styled)
                    line_length += len(styled.text)
                else:
                    text, style = styled
                    new_line.append(Styled(text[width - line_length :], style))
                    break
            return new_line
        return line[:]
