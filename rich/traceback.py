from __future__ import absolute_import

import os.path
import platform
import sys
from dataclasses import dataclass, field
from textwrap import indent
from traceback import walk_tb
from types import TracebackType
from typing import Callable, Dict, Iterable, List, Optional, Type

from pygments.lexers import guess_lexer_for_filename
from pygments.token import (
    Comment,
    Keyword,
    Name,
    Number,
    Operator,
    String,
    Token,
    Text as TextToken,
)

from . import pretty
from ._loop import loop_first, loop_last
from .columns import Columns
from .console import (
    Console,
    ConsoleOptions,
    ConsoleRenderable,
    RenderResult,
    render_group,
)
from .constrain import Constrain
from .highlighter import RegexHighlighter, ReprHighlighter
from .panel import Panel
from .scope import render_scope
from .style import Style
from .syntax import Syntax
from .text import Text
from .theme import Theme

WINDOWS = platform.system() == "Windows"

LOCALS_MAX_LENGTH = 10
LOCALS_MAX_STRING = 80


def install(
    *,
    console: Console = None,
    width: Optional[int] = 100,
    extra_lines: int = 3,
    theme: Optional[str] = None,
    word_wrap: bool = False,
    show_locals: bool = False,
    indent_guides: bool = True,
) -> Callable:
    """Install a rich traceback handler.

    Once installed, any tracebacks will be printed with syntax highlighting and rich formatting.


    Args:
        console (Optional[Console], optional): Console to write exception to. Default uses internal Console instance.
        width (Optional[int], optional): Width (in characters) of traceback. Defaults to 100.
        extra_lines (int, optional): Extra lines of code. Defaults to 3.
        theme (Optional[str], optional): Pygments theme to use in traceback. Defaults to ``None`` which will pick
            a theme appropriate for the platform.
        word_wrap (bool, optional): Enable word wrapping of long lines. Defaults to False.
        show_locals (bool, optional): Enable display of local variables. Defaults to False.
        indent_guides (bool, optional): Enable indent guides in code and locals. Defaults to True.

    Returns:
        Callable: The previous exception handler that was replaced.

    """
    traceback_console = Console(file=sys.stderr) if console is None else console

    def excepthook(
        type_: Type[BaseException],
        value: BaseException,
        traceback: TracebackType,
    ) -> None:
        traceback_console.print(
            Traceback.from_exception(
                type_,
                value,
                traceback,
                width=width,
                extra_lines=extra_lines,
                theme=theme,
                word_wrap=word_wrap,
                show_locals=show_locals,
                indent_guides=indent_guides,
            )
        )

    old_excepthook = sys.excepthook
    sys.excepthook = excepthook
    return old_excepthook


@dataclass
class Frame:
    filename: str
    lineno: int
    name: str
    line: str = ""
    locals: Optional[Dict[str, pretty.Node]] = None


@dataclass
class _SyntaxError:
    offset: int
    filename: str
    line: str
    lineno: int
    msg: str


@dataclass
class Stack:
    exc_type: str
    exc_value: str
    syntax_error: Optional[_SyntaxError] = None
    is_cause: bool = False
    frames: List[Frame] = field(default_factory=list)


@dataclass
class Trace:
    stacks: List[Stack]


class PathHighlighter(RegexHighlighter):
    highlights = [r"(?P<dim>.*/)(?P<bold>.+)"]


class Traceback:
    """A Console renderable that renders a traceback.

    Args:
        trace (Trace, optional): A `Trace` object produced from `extract`. Defaults to None, which uses
            the last exception.
        width (Optional[int], optional): Number of characters used to traceback. Defaults to 100.
        extra_lines (int, optional): Additional lines of code to render. Defaults to 3.
        theme (str, optional): Override pygments theme used in traceback.
        word_wrap (bool, optional): Enable word wrapping of long lines. Defaults to False.
        show_locals (bool, optional): Enable display of local variables. Defaults to False.
        indent_guides (bool, optional): Enable indent guides in code and locals. Defaults to True.
        locals_max_length (int, optional): Maximum length of containers before abbreviating, or None for no abbreviation.
            Defaults to 10.
        locals_max_string (int, optional): Maximum length of string before truncating, or None to disable. Defaults to 80.
    """

    def __init__(
        self,
        trace: Trace = None,
        width: Optional[int] = 100,
        extra_lines: int = 3,
        theme: Optional[str] = None,
        word_wrap: bool = False,
        show_locals: bool = False,
        indent_guides: bool = True,
        locals_max_length: int = LOCALS_MAX_LENGTH,
        locals_max_string: int = LOCALS_MAX_STRING,
    ):
        if trace is None:
            exc_type, exc_value, traceback = sys.exc_info()
            if exc_type is None or exc_value is None or traceback is None:
                raise ValueError(
                    "Value for 'trace' required if not called in except: block"
                )
            trace = self.extract(
                exc_type, exc_value, traceback, show_locals=show_locals
            )
        self.trace = trace
        self.width = width
        self.extra_lines = extra_lines
        self.theme = Syntax.get_theme(theme or "ansi_dark")
        self.word_wrap = word_wrap
        self.show_locals = show_locals
        self.indent_guides = indent_guides
        self.locals_max_length = locals_max_length
        self.locals_max_string = locals_max_string

    @classmethod
    def from_exception(
        cls,
        exc_type: Type,
        exc_value: BaseException,
        traceback: Optional[TracebackType],
        width: Optional[int] = 100,
        extra_lines: int = 3,
        theme: Optional[str] = None,
        word_wrap: bool = False,
        show_locals: bool = False,
        indent_guides: bool = True,
        locals_max_length: int = LOCALS_MAX_LENGTH,
        locals_max_string: int = LOCALS_MAX_STRING,
    ) -> "Traceback":
        """Create a traceback from exception info

        Args:
            exc_type (Type[BaseException]): Exception type.
            exc_value (BaseException): Exception value.
            traceback (TracebackType): Python Traceback object.
            width (Optional[int], optional): Number of characters used to traceback. Defaults to 100.
            extra_lines (int, optional): Additional lines of code to render. Defaults to 3.
            theme (str, optional): Override pygments theme used in traceback.
            word_wrap (bool, optional): Enable word wrapping of long lines. Defaults to False.
            show_locals (bool, optional): Enable display of local variables. Defaults to False.
            indent_guides (bool, optional): Enable indent guides in code and locals. Defaults to True.
            locals_max_length (int, optional): Maximum length of containers before abbreviating, or None for no abbreviation.
                Defaults to 10.
            locals_max_string (int, optional): Maximum length of string before truncating, or None to disable. Defaults to 80.

        Returns:
            Traceback: A Traceback instance that may be printed.
        """
        rich_traceback = cls.extract(
            exc_type, exc_value, traceback, show_locals=show_locals
        )
        return Traceback(
            rich_traceback,
            width=width,
            extra_lines=extra_lines,
            theme=theme,
            word_wrap=word_wrap,
            show_locals=show_locals,
            indent_guides=indent_guides,
            locals_max_length=locals_max_length,
            locals_max_string=locals_max_string,
        )

    @classmethod
    def extract(
        cls,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: Optional[TracebackType],
        show_locals: bool = False,
        locals_max_length: int = LOCALS_MAX_LENGTH,
        locals_max_string: int = LOCALS_MAX_STRING,
    ) -> Trace:
        """Extract traceback information.

        Args:
            exc_type (Type[BaseException]): Exception type.
            exc_value (BaseException): Exception value.
            traceback (TracebackType): Python Traceback object.
            show_locals (bool, optional): Enable display of local variables. Defaults to False.
            locals_max_length (int, optional): Maximum length of containers before abbreviating, or None for no abbreviation.
                Defaults to 10.
            locals_max_string (int, optional): Maximum length of string before truncating, or None to disable. Defaults to 80.

        Returns:
            Trace: A Trace instance which you can use to construct a `Traceback`.
        """

        stacks: List[Stack] = []
        is_cause = False

        while True:
            stack = Stack(
                exc_type=str(exc_type.__name__),
                exc_value=str(exc_value),
                is_cause=is_cause,
            )

            if isinstance(exc_value, SyntaxError):
                stack.syntax_error = _SyntaxError(
                    offset=exc_value.offset or 0,
                    filename=exc_value.filename or "?",
                    lineno=exc_value.lineno or 0,
                    line=exc_value.text or "",
                    msg=exc_value.msg,
                )

            stacks.append(stack)
            append = stack.frames.append

            for frame_summary, line_no in walk_tb(traceback):
                filename = frame_summary.f_code.co_filename
                if filename and not filename.startswith("<"):
                    filename = os.path.abspath(filename) if filename else "?"
                frame = Frame(
                    filename=filename,
                    lineno=line_no,
                    name=frame_summary.f_code.co_name,
                    locals={
                        key: pretty.traverse(
                            value,
                            max_length=locals_max_length,
                            max_string=locals_max_string,
                        )
                        for key, value in frame_summary.f_locals.items()
                    }
                    if show_locals
                    else None,
                )
                append(frame)

            cause = getattr(exc_value, "__cause__", None)
            if cause and cause.__traceback__:
                exc_type = cause.__class__
                exc_value = cause
                traceback = cause.__traceback__
                if traceback:
                    is_cause = True
                    continue

            cause = exc_value.__context__
            if (
                cause
                and cause.__traceback__
                and not getattr(exc_value, "__suppress_context__", False)
            ):
                exc_type = cause.__class__
                exc_value = cause
                traceback = cause.__traceback__
                if traceback:
                    is_cause = False
                    continue
            # No cover, code is reached but coverage doesn't recognize it.
            break  # pragma: no cover

        trace = Trace(stacks=stacks)
        return trace

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        theme = self.theme
        background_style = theme.get_background_style()
        token_style = theme.get_style_for_token

        traceback_theme = Theme(
            {
                "pretty": token_style(TextToken),
                "pygments.text": token_style(Token),
                "pygments.string": token_style(String),
                "pygments.function": token_style(Name.Function),
                "pygments.number": token_style(Number),
                "repr.indent": token_style(Comment) + Style(dim=True),
                "repr.str": token_style(String),
                "repr.brace": token_style(TextToken) + Style(bold=True),
                "repr.number": token_style(Number),
                "repr.bool_true": token_style(Keyword.Constant),
                "repr.bool_false": token_style(Keyword.Constant),
                "repr.none": token_style(Keyword.Constant),
                "scope.border": token_style(String.Delimiter),
                "scope.equals": token_style(Operator),
                "scope.key": token_style(Name),
                "scope.key.special": token_style(Name.Constant) + Style(dim=True),
            }
        )

        highlighter = ReprHighlighter()
        for last, stack in loop_last(reversed(self.trace.stacks)):
            if stack.frames:
                stack_renderable: ConsoleRenderable = Panel(
                    self._render_stack(stack),
                    title="[traceback.title]Traceback [dim](most recent call last)",
                    style=background_style,
                    border_style="traceback.border.syntax_error",
                    expand=True,
                    padding=(0, 1),
                )
                stack_renderable = Constrain(stack_renderable, self.width)
                with console.use_theme(traceback_theme):
                    yield stack_renderable
            if stack.syntax_error is not None:
                with console.use_theme(traceback_theme):
                    yield Constrain(
                        Panel(
                            self._render_syntax_error(stack.syntax_error),
                            style=background_style,
                            border_style="traceback.border",
                            expand=True,
                            padding=(0, 1),
                            width=self.width,
                        ),
                        self.width,
                    )
                yield Text.assemble(
                    (f"{stack.exc_type}: ", "traceback.exc_type"),
                    highlighter(stack.syntax_error.msg),
                )
            else:
                yield Text.assemble(
                    (f"{stack.exc_type}: ", "traceback.exc_type"),
                    highlighter(stack.exc_value),
                )

            if not last:
                if stack.is_cause:
                    yield Text.from_markup(
                        "\n[i]The above exception was the direct cause of the following exception:\n",
                    )
                else:
                    yield Text.from_markup(
                        "\n[i]During handling of the above exception, another exception occurred:\n",
                    )

    @render_group()
    def _render_syntax_error(self, syntax_error: _SyntaxError) -> RenderResult:
        highlighter = ReprHighlighter()
        path_highlighter = PathHighlighter()
        if syntax_error.filename != "<stdin>":
            text = Text.assemble(
                (f" {syntax_error.filename}", "pygments.string"),
                (":", "pygments.text"),
                (str(syntax_error.lineno), "pygments.number"),
                style="pygments.text",
            )
            yield path_highlighter(text)
        syntax_error_text = highlighter(syntax_error.line.rstrip())
        syntax_error_text.no_wrap = True
        offset = min(syntax_error.offset - 1, len(syntax_error_text))
        syntax_error_text.stylize("bold underline", offset, offset + 1)
        syntax_error_text += Text.from_markup(
            "\n" + " " * offset + "[traceback.offset]▲[/]",
            style="pygments.text",
        )
        yield syntax_error_text

    @render_group()
    def _render_stack(self, stack: Stack) -> RenderResult:
        path_highlighter = PathHighlighter()
        theme = self.theme
        code_cache: Dict[str, str] = {}

        def read_code(filename: str) -> str:
            """Read files, and cache results on filename.

            Args:
                filename (str): Filename to read

            Returns:
                str: Contents of file
            """
            code = code_cache.get(filename)
            if code is None:
                with open(
                    filename, "rt", encoding="utf-8", errors="replace"
                ) as code_file:
                    code = code_file.read()
                code_cache[filename] = code
            return code

        def render_locals(frame: Frame) -> Iterable[ConsoleRenderable]:
            if frame.locals:
                yield render_scope(
                    frame.locals,
                    title="locals",
                    indent_guides=self.indent_guides,
                    max_length=self.locals_max_length,
                    max_string=self.locals_max_string,
                )

        for first, frame in loop_first(stack.frames):
            text = Text.assemble(
                path_highlighter(Text(frame.filename, style="pygments.string")),
                (":", "pygments.text"),
                (str(frame.lineno), "pygments.number"),
                " in ",
                (frame.name, "pygments.function"),
                style="pygments.text",
            )
            if not frame.filename.startswith("<") and not first:
                yield ""
            yield text
            if frame.filename.startswith("<"):
                yield from render_locals(frame)
                continue
            try:
                code = read_code(frame.filename)
                lexer = guess_lexer_for_filename(frame.filename, code)
                lexer_name = lexer.name
                syntax = Syntax(
                    code,
                    lexer_name,
                    theme=theme,
                    line_numbers=True,
                    line_range=(
                        frame.lineno - self.extra_lines,
                        frame.lineno + self.extra_lines,
                    ),
                    highlight_lines={frame.lineno},
                    word_wrap=self.word_wrap,
                    code_width=88,
                    indent_guides=self.indent_guides,
                )
                yield ""
            except Exception as error:
                yield Text.assemble(
                    (f"{error.__class__.__name__}: {error}", "traceback.error"),
                )
            else:
                yield (
                    Columns(
                        [
                            syntax,
                            *render_locals(frame),
                        ],
                        padding=1,
                    )
                    if frame.locals
                    else syntax
                )


if __name__ == "__main__":  # pragma: no cover

    from .console import Console

    console = Console()
    import sys

    def bar(a):  # 这是对亚洲语言支持的测试。面对模棱两可的想法，拒绝猜测的诱惑
        one = 1
        print(one / a)

    def foo(a):

        zed = {
            "characters": {
                "Paul Atriedies",
                "Vladimir Harkonnen",
                "Thufir Haway",
                "Duncan Idaho",
            },
            "atomic_types": (None, False, True),
        }
        bar(a)

    def error():

        try:
            try:
                foo(0)
            except:
                slfkjsldkfj  # type: ignore
        except:
            console.print_exception(show_locals=True)

    error()
