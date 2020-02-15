from __future__ import absolute_import

from dataclasses import dataclass, field
from traceback import extract_tb
from typing import Type, List

from .console import Console, ConsoleOptions, RenderResult
from .highlighter import RegexHighlighter
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


@dataclass
class Stack:
    exc_type: str
    exc_value: str
    frames: List[Frame] = field(default_factory=list)

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        path_highlighter = PathHighlighter()
        for frame in self.frames:
            text = Text.assemble(
                (" File ", "traceback.text"),
                (f'"{frame.filename}"', "traceback.filename"),
                (", line ", "traceback.text"),
                (str(frame.lineno), "traceback.lineno"),
                (", in ", "traceback.text"),
                (frame.name, "traceback.name"),
            )
            yield path_highlighter(text)
            syntax = Syntax.from_path(
                frame.filename,
                line_numbers=True,
                line_range=(frame.lineno - 3, frame.lineno + 3),
                highlight_lines={frame.lineno},
            )
            yield Padding.indent(syntax, 2)


@dataclass
class Trace:
    stacks: List[Stack]


class PathHighlighter(RegexHighlighter):
    highlights = [r'"(?P<dim>.*/)(?P<b>.+)"']


class Traceback:
    def __init__(self, trace: Trace = None):
        if trace is None:
            trace = self.extract(*sys.exc_info())
        self.trace = trace

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
                append(
                    Frame(
                        frame_summary.filename, frame_summary.lineno, frame_summary.name
                    )
                )
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
        for last, stack in iter_last(reversed(self.trace.stacks)):
            yield Text.from_markup("[b]Traceback[/b] [dim](most recent call last):")
            yield Panel(stack, style="blue")
            yield Text.assemble(
                (f"{stack.exc_type}: ", "traceback.exc_type"),
                (stack.exc_value, "traceback.exc_value"),
            )
            if not last:
                yield Text.from_markup(
                    "\n[I]During handling of the above exception, another exception occurred:\n\n",
                )


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

