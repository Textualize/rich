from __future__ import absolute_import

import platform
import sys
from dataclasses import dataclass, field
from traceback import extract_tb
from types import TracebackType
from typing import Callable, List, Optional, Type

from ._loop import loop_last
from .console import (
    Console,
    ConsoleOptions,
    ConsoleRenderable,
    RenderResult,
    render_group,
)
from .constrain import Constrain
from .highlighter import RegexHighlighter, ReprHighlighter
from .padding import Padding
from .panel import Panel
from .syntax import Syntax
from .text import Text

WINDOWS = platform.system() == "Windows"


def install(
    *,
    console: Console = None,
    width: Optional[int] = 100,
    line_numbers: bool = True,
    extra_lines: int = 3,
    theme: Optional[str] = None,
    word_wrap: bool = False,
) -> Callable:
    """Install a rich traceback handler.

    Once installed, any tracebacks will be printed with syntax highlighting and rich formatting.


    Args:
        console (Optional[Console], optional): Console to write exception to. Default uses internal Console instance.
        width (Optional[int], optional): Width (in characters) of traceback. Defaults to 100.
        line_numbers (bool, optional): Enable line numbers.
        extra_lines (int, optional): Extra lines of code. Defaults to 3.
        theme (Optional[str], optional): Pygments theme to use in traceback. Defaults to ``None`` which will pick
            a theme appropriate for the platform.
        word_wrap(bool, optional): Enable word wrapping of long lines. Defaults to False.

    Returns:
        Callable: The previous exception handler that was replaced

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
    frames: List[Frame] = field(default_factory=list)


@dataclass
class Trace:
    stacks: List[Stack]


class PathHighlighter(RegexHighlighter):
    highlights = [r'"(?P<dim>.*/)(?P<_>.+)"']


class Traceback:
    """A Console renderable that renders a traceback.

    Args:
        trace (Trace, optional): A `Trace` object produced from `extract`. Defaults to None, which uses
            the last exception.
        width (Optional[int], optional): Number of characters used to traceback. Defaults to 100.
        extra_lines (int, optional): Additional lines of code to render. Defaults to 3.
        theme (str, optional): Override pygments theme used in traceback.
        word_wrap (bool, optional): Enable word wrapping of long lines. Defaults to False.
    """

    def __init__(
        self,
        trace: Trace = None,
        width: Optional[int] = 88,
        extra_lines: int = 3,
        theme: Optional[str] = None,
        word_wrap: bool = False,
    ):
        if trace is None:
            exc_type, exc_value, traceback = sys.exc_info()
            if exc_type is None or exc_value is None or traceback is None:
                raise ValueError(
                    "Value for 'trace' required if not called in except: block"
                )
            trace = self.extract(exc_type, exc_value, traceback)
        self.trace = trace
        self.width = width
        self.extra_lines = extra_lines
        self.theme = theme
        self.word_wrap = word_wrap

    @classmethod
    def from_exception(
        cls,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
        width: Optional[int] = 100,
        extra_lines: int = 3,
        theme: Optional[str] = None,
        word_wrap: bool = False,
    ) -> "Traceback":
        rich_traceback = cls.extract(exc_type, exc_value, traceback)
        return Traceback(
            rich_traceback,
            width=width,
            extra_lines=extra_lines,
            theme=theme,
            word_wrap=word_wrap,
        )

    @classmethod
    def extract(
        cls,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ) -> Trace:
        """Extrace traceback information.

        Args:
            exc_type (Type[BaseException]): Exception type.
            exc_value (BaseException): Exception value.
            traceback (TracebackType): Python Traceback object.

        Returns:
            Trace: A Trace instance which you can use to construct a `Traceback`.
        """
        stacks: List[Stack] = []
        while True:
            stack = Stack(exc_type=str(exc_type.__name__), exc_value=str(exc_value))

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

            for frame_summary in extract_tb(traceback):
                frame = Frame(
                    filename=frame_summary.filename,
                    lineno=frame_summary.lineno,
                    name=frame_summary.name,
                )
                append(frame)

            cause = exc_value.__context__
            if cause and cause.__traceback__:
                exc_type = cause.__class__
                exc_value = cause
                traceback = cause.__traceback__
                continue
            # No cover, code is reached but coverage doesn't recognize it.
            break  # pragma: no cover

        trace = Trace(stacks=stacks)
        return trace

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        highlighter = ReprHighlighter()
        for last, stack in loop_last(reversed(self.trace.stacks)):
            if stack.frames:
                yield Text.from_markup("[b]Traceback[/b] [dim](most recent call last):")
                stack_renderable: ConsoleRenderable = Panel(
                    self._render_stack(stack), style="blue", expand=False
                )
                stack_renderable = Constrain(stack_renderable, self.width)
                yield stack_renderable
            if stack.syntax_error is not None:
                yield Constrain(
                    Panel(
                        self._render_syntax_error(stack.syntax_error),
                        style="red",
                        expand=False,
                    ),
                    self.width,
                )
                yield Text.assemble(
                    (f"{stack.exc_type}: ", "traceback.exc_type"), end=""
                )
                yield highlighter(stack.syntax_error.msg)
            else:
                yield Text.assemble(
                    (f"{stack.exc_type}: ", "traceback.exc_type"), end=""
                )
                yield highlighter(stack.exc_value)
            if not last:
                yield Text.from_markup(
                    "\n[i]During handling of the above exception, another exception occurred:\n\n",
                )

    @render_group()
    def _render_syntax_error(self, syntax_error: _SyntaxError) -> RenderResult:
        highlighter = ReprHighlighter()
        path_highlighter = PathHighlighter()
        text = Text.assemble(
            (" File ", "traceback.text"),
            (f'"{syntax_error.filename}"', "traceback.filename"),
            (", line ", "traceback.text"),
            (str(syntax_error.lineno), "traceback.lineno"),
        )
        yield path_highlighter(text)
        yield highlighter("   " + syntax_error.line)
        yield Text.from_markup(
            "   " + " " * (syntax_error.offset - 1) + "[traceback.offset]▲[/]\n"
        )

    @render_group()
    def _render_stack(self, stack: Stack) -> RenderResult:
        path_highlighter = PathHighlighter()
        theme = self.theme or ("fruity" if WINDOWS else "monokai")
        for frame in stack.frames:
            text = Text.assemble(
                (" File ", "traceback.text"),
                (f'"{frame.filename}"', "traceback.filename"),
                (", line ", "traceback.text"),
                (str(frame.lineno), "traceback.lineno"),
                (", in ", "traceback.text"),
                (frame.name, "traceback.name"),
            )
            yield path_highlighter(text)
            if frame.filename.startswith("<"):
                continue
            try:
                syntax = Syntax.from_path(
                    frame.filename,
                    theme=theme,
                    line_numbers=True,
                    line_range=(
                        frame.lineno - self.extra_lines,
                        frame.lineno + self.extra_lines,
                    ),
                    highlight_lines={frame.lineno},
                    word_wrap=self.word_wrap,
                )
            except Exception:
                pass
            else:
                yield Padding.indent(syntax, 2)


if __name__ == "__main__":  # pragma: no cover

    from .console import Console

    console = Console()
    import sys

    def bar(a):  # 这是对亚洲语言支持的测试。面对模棱两可的想法，拒绝猜测的诱惑
        print(1 / a)

    def foo(a):
        bar(a)

    try:
        try:
            foo(0)
        except:
            slfkjsldkfj  # type: ignore
    except:
        tb = Traceback()
        # print(fooads)
        console.print(tb)
