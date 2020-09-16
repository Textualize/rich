import os.path
import platform
import textwrap
from typing import Any, Dict, Optional, Set, Tuple, Type, Union

from pygments.lexers import get_lexer_by_name, guess_lexer_for_filename
from pygments.style import Style as PygmentsStyle
from pygments.styles import get_style_by_name
from pygments.token import Token
from pygments.util import ClassNotFound

from ._loop import loop_first
from .color import Color, blend_rgb, parse_rgb_hex
from .console import Console, ConsoleOptions, JustifyMethod, RenderResult, Segment
from .jupyter import JupyterMixin
from .measure import Measurement
from .style import Style
from .text import Text

WINDOWS = platform.system() == "Windows"
DEFAULT_THEME = "monokai"


class Syntax(JupyterMixin):
    """Construct a Syntax object to render syntax highlighted code.

    Args:
        code (str): Code to highlight.
        lexer_name (str): Lexer to use (see https://pygments.org/docs/lexers/)
        theme (str, optional): Color theme, aka Pygments style (see https://pygments.org/docs/styles/#getting-a-list-of-available-styles). Defaults to "monokai".
        dedent (bool, optional): Enable stripping of initial whitespace. Defaults to True.
        line_numbers (bool, optional): Enable rendering of line numbers. Defaults to False.
        start_line (int, optional): Starting number for line numbers. Defaults to 1.
        line_range (Tuple[int, int], optional): If given should be a tuple of the start and end line to render.
        highlight_lines (Set[int]): A set of line numbers to highlight.
        code_width: Width of code to render (not including line numbers), or ``None`` to use all available width.
        tab_size (int, optional): Size of tabs. Defaults to 4.
        word_wrap (bool, optional): Enable word wrapping.
    """

    _pygments_style_class: Type[PygmentsStyle]

    def __init__(
        self,
        code: str,
        lexer_name: str,
        *,
        theme: Union[str, Type[PygmentsStyle]] = DEFAULT_THEME,
        dedent: bool = False,
        line_numbers: bool = False,
        start_line: int = 1,
        line_range: Tuple[int, int] = None,
        highlight_lines: Set[int] = None,
        code_width: Optional[int] = None,
        tab_size: int = 4,
        word_wrap: bool = False
    ) -> None:
        self.code = code
        self.lexer_name = lexer_name
        self.dedent = dedent
        self.line_numbers = line_numbers
        self.start_line = start_line
        self.line_range = line_range
        self.highlight_lines = highlight_lines or set()
        self.code_width = code_width
        self.tab_size = tab_size
        self.word_wrap = word_wrap

        self._style_cache: Dict[Any, Style] = {}

        if not isinstance(theme, str) and issubclass(theme, PygmentsStyle):
            self._pygments_style_class = theme
        else:
            try:
                self._pygments_style_class = get_style_by_name(theme)
            except ClassNotFound:
                self._pygments_style_class = get_style_by_name("default")
        self._background_color = self._pygments_style_class.background_color

    @classmethod
    def from_path(
        cls,
        path: str,
        encoding: str = "utf-8",
        theme: Union[str, Type[PygmentsStyle]] = DEFAULT_THEME,
        dedent: bool = True,
        line_numbers: bool = False,
        line_range: Tuple[int, int] = None,
        start_line: int = 1,
        highlight_lines: Set[int] = None,
        code_width: Optional[int] = None,
        tab_size: int = 4,
        word_wrap: bool = False,
    ) -> "Syntax":
        """Construct a Syntax object from a file.

        Args:
            path (str): Path to file to highlight.
            encoding (str): Encoding of file.
            lexer_name (str): Lexer to use (see https://pygments.org/docs/lexers/)
            theme (str, optional): Color theme, aka Pygments style (see https://pygments.org/docs/styles/#getting-a-list-of-available-styles). Defaults to "emacs".
            dedent (bool, optional): Enable stripping of initial whitespace. Defaults to True.
            line_numbers (bool, optional): Enable rendering of line numbers. Defaults to False.
            start_line (int, optional): Starting number for line numbers. Defaults to 1.
            line_range (Tuple[int, int], optional): If given should be a tuple of the start and end line to render.
            highlight_lines (Set[int]): A set of line numbers to highlight.
            code_width: Width of code to render (not including line numbers), or ``None`` to use all available width.
            tab_size (int, optional): Size of tabs. Defaults to 4.
            word_wrap (bool, optional): Enable word wrapping of code.

        Returns:
            [Syntax]: A Syntax object that may be printed to the console
        """
        with open(path, "rt", encoding=encoding) as code_file:
            code = code_file.read()

        lexer = None
        lexer_name = "default"
        try:
            _, ext = os.path.splitext(path)
            if ext:
                extension = ext.lstrip(".").lower()
                lexer = get_lexer_by_name(extension)
                lexer_name = lexer.name
        except ClassNotFound:
            pass

        if lexer is None:
            try:
                lexer = guess_lexer_for_filename(path, code)
                lexer_name = lexer.name
            except ClassNotFound:
                pass

        return cls(
            code,
            lexer_name,
            theme=theme,
            dedent=dedent,
            line_numbers=line_numbers,
            line_range=line_range,
            start_line=start_line,
            highlight_lines=highlight_lines,
            code_width=code_width,
            tab_size=tab_size,
            word_wrap=word_wrap,
        )

    def _get_theme_style(self, token_type) -> Style:
        if token_type in self._style_cache:
            style = self._style_cache[token_type]
        else:
            try:
                pygments_style = self._pygments_style_class.style_for_token(token_type)
            except KeyError:
                style = Style()
            else:
                color = pygments_style["color"]
                bgcolor = pygments_style["bgcolor"]
                style = Style(
                    color="#" + color if color else "#000000",
                    bgcolor="#" + bgcolor if bgcolor else self._background_color,
                    bold=pygments_style["bold"],
                    italic=pygments_style["italic"],
                    underline=pygments_style["underline"],
                )
            self._style_cache[token_type] = style

        return style

    def _get_default_style(self) -> Style:
        style = self._get_theme_style(Token.Text)
        style = style + Style(bgcolor=self._pygments_style_class.background_color)
        return style

    def highlight(self, code: str) -> Text:
        """Highlight code and return a Text instance.

        Args:
            code (str). Code to highlight.

        Returns:
            Text: A text instance containing syntax highlight.
        """

        default_style = self._get_default_style()
        try:
            lexer = get_lexer_by_name(self.lexer_name)
        except ClassNotFound:
            return Text(
                code, justify="left", style=default_style, tab_size=self.tab_size
            )
        text = Text(justify="left", style=default_style, tab_size=self.tab_size)
        append = text.append
        _get_theme_style = self._get_theme_style
        for token_type, token in lexer.get_tokens(code):
            append(token, _get_theme_style(token_type))
        return text

    def _get_line_numbers_color(self, blend: float = 0.3) -> Color:
        background_color = parse_rgb_hex(
            self._pygments_style_class.background_color[1:]
        )
        foreground_color = self._get_theme_style(Token.Text)._color
        if foreground_color is None:
            return Color.default()
        # TODO: Handle no full colors here
        assert foreground_color.triplet is not None
        new_color = blend_rgb(
            background_color, foreground_color.triplet, cross_fade=blend
        )
        return Color.from_triplet(new_color)

    @property
    def _numbers_column_width(self) -> int:
        """Get the number of characters used to render the numbers column."""
        if self.line_numbers:
            return len(str(self.start_line + self.code.count("\n"))) + 2
        return 0

    def _get_number_styles(self, console: Console) -> Tuple[Style, Style, Style]:
        """Get background, number, and highlight styles for line numbers."""
        background_style = Style(bgcolor=self._pygments_style_class.background_color)
        if console.color_system in ("256", "truecolor"):
            number_style = Style.chain(
                background_style,
                self._get_theme_style(Token.Text),
                Style(color=self._get_line_numbers_color()),
            )
            highlight_number_style = Style.chain(
                background_style,
                self._get_theme_style(Token.Text),
                Style(bold=True, color=self._get_line_numbers_color(0.9)),
            )
        else:
            number_style = highlight_number_style = Style()
        return background_style, number_style, highlight_number_style

    def __rich_measure__(self, console: "Console", max_width: int) -> "Measurement":
        if self.code_width is not None:
            width = self.code_width + self._numbers_column_width
            return Measurement(self._numbers_column_width, width)
        return Measurement(self._numbers_column_width, max_width)

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        code_width = (
            (options.max_width - self._numbers_column_width - 1)
            if self.code_width is None
            else self.code_width
        )
        code = self.code
        if self.dedent:
            code = textwrap.dedent(code)
        text = self.highlight(self.code)
        if text.plain.endswith("\n"):
            text.plain = text.plain[:-1]
        if not self.line_numbers:
            if self.code_width is None:
                yield text
            else:
                yield from console.render(
                    text, options=options.update(width=code_width)
                )
            return

        lines = text.split("\n")

        line_offset = 0
        if self.line_range:
            start_line, end_line = self.line_range
            line_offset = max(0, start_line - 1)
            lines = lines[line_offset:end_line]

        numbers_column_width = self._numbers_column_width
        render_options = options.update(width=code_width)

        (
            background_style,
            number_style,
            highlight_number_style,
        ) = self._get_number_styles(console)

        highlight_line = self.highlight_lines.__contains__
        _Segment = Segment
        padding = _Segment(" " * numbers_column_width + " ", background_style)
        new_line = _Segment("\n")

        line_pointer = "❱ "

        for line_no, line in enumerate(lines, self.start_line + line_offset):
            if self.word_wrap:
                wrapped_lines = console.render_lines(
                    line, render_options, style=background_style
                )
            else:
                segments = list(line.render(console, end=""))
                wrapped_lines = [
                    Segment.adjust_line_length(
                        segments, render_options.max_width, style=background_style
                    )
                ]
            for first, wrapped_line in loop_first(wrapped_lines):
                if first:
                    line_column = str(line_no).rjust(numbers_column_width - 2) + " "
                    if highlight_line(line_no):
                        yield _Segment(line_pointer, number_style)
                        yield _Segment(
                            line_column,
                            highlight_number_style,
                        )
                    else:
                        yield _Segment("  ", highlight_number_style)
                        yield _Segment(
                            line_column,
                            number_style,
                        )
                else:
                    yield padding
                yield from wrapped_line
                yield new_line


if __name__ == "__main__":  # pragma: no cover

    import argparse

    parser = argparse.ArgumentParser(
        description="Render syntax to the console with Rich"
    )
    parser.add_argument("path", metavar="PATH", help="path to file")
    parser.add_argument(
        "-c",
        "--force-color",
        dest="force_color",
        action="store_true",
        default=None,
        help="force color for non-terminals",
    )
    parser.add_argument(
        "-l",
        "--line-numbers",
        dest="line_numbers",
        action="store_true",
        help="render line numbers",
    )
    parser.add_argument(
        "-w",
        "--width",
        type=int,
        dest="width",
        default=None,
        help="width of output (default will auto-detect)",
    )
    parser.add_argument(
        "-r",
        "--wrap",
        dest="word_wrap",
        action="store_true",
        default=False,
        help="word wrap long lines",
    )
    parser.add_argument(
        "-t", "--theme", dest="theme", default="monokai", help="pygments theme"
    )
    args = parser.parse_args()

    from rich.console import Console

    console = Console(force_terminal=args.force_color, width=args.width)

    syntax = Syntax.from_path(
        args.path,
        line_numbers=args.line_numbers,
        word_wrap=args.word_wrap,
        theme=args.theme,
    )
    console.print(syntax)
