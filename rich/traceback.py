from __future__ import absolute_import

from dataclasses import dataclass, field
from traceback import extract_tb
from typing import Optional, Type, List

from .console import (
    Console,
    ConsoleOptions,
    ConsoleRenderable,
    render_group,
    RenderResult,
)
from .constrain import Constrain
from .highlighter import RegexHighlighter, ReprHighlighter
from .padding import Padding
from .panel import Panel
from .rule import Rule
from .text import Text
from ._tools import iter_last
from .syntax import Syntax


@dataclass
class Frame:
    filename: str
    lineno: int
    name: str
    line: str


@dataclass
class Stack:
    exc_type: str
    exc_value: str
    frames: List[Frame] = field(default_factory=list)


@dataclass
class Trace:
    stacks: List[Stack]


class PathHighlighter(RegexHighlighter):
    highlights = [r'"(?P<dim>.*/)(?P<_>.+)"']


class Traceback:
    def __init__(
        self, trace: Trace = None, code_width: Optional[int] = 88, extra_lines: int = 3,
    ):
        if trace is None:
            trace = self.extract(*sys.exc_info())
        self.trace = trace
        self.code_width = code_width
        self.extra_lines = extra_lines

    @classmethod
    def extract(
        cls, exc_type: Type[BaseException], exc_value: BaseException, traceback
    ) -> Trace:
        stacks: List[Stack] = []
        while True:
            stack = Stack(exc_type=str(exc_type.__name__), exc_value=str(exc_value))
            stacks.append(stack)
            append = stack.frames.append

            for frame_summary in extract_tb(traceback):
                frame = Frame(
                    filename=frame_summary.filename,
                    lineno=frame_summary.lineno,
                    name=frame_summary.name,
                    line=frame_summary.line,
                )
                append(frame)

            cause = exc_value.__context__
            if cause:
                exc_type = cause.__class__
                exc_value = cause
                traceback = cause.__traceback__
                continue
            break
        trace = Trace(stacks=stacks)
        return trace

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        yield ""
        highlighter = ReprHighlighter()
        for last, stack in iter_last(reversed(self.trace.stacks)):
            yield Text.from_markup("[b]Traceback[/b] [dim](most recent call last):")
            stack_renderable: ConsoleRenderable = Panel(
                self._render_stack(stack), style="blue"
            )
            if self.code_width is not None:
                stack_renderable = Constrain(stack_renderable, width=self.code_width)
            yield stack_renderable
            yield Text.assemble((f"{stack.exc_type}: ", "traceback.exc_type"), end="")
            yield highlighter(stack.exc_value)
            if not last:
                yield Text.from_markup(
                    "\n[i]During handling of the above exception, another exception occurred:\n\n",
                )

    @render_group
    def _render_stack(self, stack: Stack) -> RenderResult:
        path_highlighter = PathHighlighter()
        for frame in stack.frames:
            text = Text.assemble(
                (" File ", "traceback.text"),
                (f'"{frame.filename}"', "traceback.filename"),
                (", in ", "traceback.text"),
                (frame.name, "traceback.name"),
            )
            yield path_highlighter(text)
            try:
                syntax = Syntax.from_path(
                    frame.filename,
                    line_numbers=True,
                    line_range=(
                        frame.lineno - self.extra_lines,
                        frame.lineno + self.extra_lines,
                    ),
                    highlight_lines={frame.lineno},
                )
            except Exception:
                syntax = Syntax(
                    frame.line,
                    "python",
                    line_numbers=True,
                    start_line=frame.lineno,
                    highlight_lines={frame.lineno},
                )
            yield Padding.indent(syntax, 2)


if __name__ == "__main__":

    from .console import Console

    console = Console()
    import sys

    def bar(a):
        print(1 / a)

    def foo(a):
        bar(a)

    try:
        try:
            foo(0)
        except:
            slfkjsldkfj
    except:
        tb = Traceback()
        # print(fooads)
        console.print(tb)

