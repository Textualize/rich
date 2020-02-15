"""

WORK IN PROGRESS

A syntax highlighter for Python code

In theory, this can give better results than Pygments

"""

from io import StringIO
import textwrap
import tokenize
from typing import Iterable, Optional, Set, Tuple

from ._tools import iter_first_last
from .console import Console, ConsoleOptions, RenderResult, Segment, ConsoleRenderable
from .style import Style
from .text import Text


class Python:
    def __init__(
        self,
        code: str,
        dedent: bool = False,
        line_numbers: bool = False,
        start_line_no: int = 1,
        line_range: Tuple[int, int] = None,
    ):
        self.code = code
        self.dedent = dedent
        self.line_numbers = line_numbers
        self.start_line_no = start_line_no
        self.line_range = line_range

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:

        OP = tokenize.OP
        tok_name = tokenize.tok_name
        code = self.code
        if self.dedent:
            code = textwrap.dedent(code)
        lines = Text(code).split(include_separator=True)
        line_count = len(lines)

        if self.line_range:
            styled_range = range(*self.line_range)
        else:
            styled_range = range(0, line_count)

        def add_style(
            line_no: int, start: int, end: int, styles: Iterable[str]
        ) -> None:
            """Add style to a portion of a line.
            
            Args:
                line_no (int): 1 indexed line number.
                start (int): Start column.
                end (int): End column, or None for end of line.
                styles (Iterable[str]): Styles to apply.
            """
            if line_no in styled_range:
                line = lines[line_no - 1]
                for style in styles:
                    line.stylize(start, end, style)

        for token in tokenize.generate_tokens(StringIO(code).readline):
            styles: Tuple[str, ...]
            if token.type == OP:
                styles = (
                    "python.operator",
                    f"python.{tok_name[token.exact_type].lower()}",
                )
            else:
                styles = (f"python.{tok_name[token.type].lower()}",)

            start_line, start_col = token.start
            end_line, end_col = token.end
            if start_line >= line_count:
                break
            if start_line == end_line:
                add_style(start_line, start_col, end_col, styles)
            else:
                line_range = range(start_line, end_line + 1)
                for first, last, line_no in iter_first_last(line_range):
                    if first:
                        add_style(line_no, start_col, line_count, styles)
                    elif last:
                        add_style(line_no, 0, end_col, styles)
                    else:
                        add_style(line_no, 0, line_count, styles)
        if self.line_range:
            yield from lines[slice(*styled_range)]
        else:
            yield from lines


if __name__ == "__main__":

    code = open("segment.py", encoding="utf-8").read()
    py = Python(code)

    from .console import Console

    console = Console()
    console.print(py)

    import tokenize

