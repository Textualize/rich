# coding=utf-8

import sys
import os, tempfile

import pytest
from .render import render

from rich.panel import Panel
from rich.style import Style
from rich.syntax import Syntax, ANSISyntaxTheme, PygmentsSyntaxTheme, Color, Console


CODE = '''
def loop_first_last(values: Iterable[T]) -> Iterable[Tuple[bool, bool, T]]:
    """Iterate and generate a tuple with a flag for first and last value."""
    iter_values = iter(values)
    try:
        previous_value = next(iter_values)
    except StopIteration:
        return
    first = True
    for value in iter_values:
        yield first, False, previous_value
        first = False
        previous_value = value
    yield first, True, previous_value
'''


def test_python_render():
    syntax = Panel.fit(
        Syntax(
            CODE,
            lexer_name="python",
            line_numbers=True,
            line_range=(2, 10),
            theme="foo",
            code_width=60,
            word_wrap=True,
        ),
        padding=0,
    )
    rendered_syntax = render(syntax)
    print(repr(rendered_syntax))
    expected = '╭────────────────────────────────────────────────────────────────╮\n│\x1b[1;38;2;24;24;24;48;2;248;248;248m  \x1b[0m\x1b[38;2;173;173;173;48;2;248;248;248m 2 \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m    \x1b[0m\x1b[3;38;2;186;33;33;48;2;248;248;248m"""Iterate and generate a tuple with a flag for first \x1b[0m\x1b[48;2;248;248;248m \x1b[0m│\n│\x1b[48;2;248;248;248m     \x1b[0m\x1b[3;38;2;186;33;33;48;2;248;248;248mand last value."""\x1b[0m\x1b[48;2;248;248;248m                                         \x1b[0m│\n│\x1b[1;38;2;24;24;24;48;2;248;248;248m  \x1b[0m\x1b[38;2;173;173;173;48;2;248;248;248m 3 \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m    \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248miter_values\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;102;102;102;48;2;248;248;248m=\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;128;0;48;2;248;248;248miter\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m(\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mvalues\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m)\x1b[0m\x1b[48;2;248;248;248m                             \x1b[0m│\n│\x1b[1;38;2;24;24;24;48;2;248;248;248m  \x1b[0m\x1b[38;2;173;173;173;48;2;248;248;248m 4 \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m    \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248mtry\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m:\x1b[0m\x1b[48;2;248;248;248m                                                   \x1b[0m│\n│\x1b[1;38;2;24;24;24;48;2;248;248;248m  \x1b[0m\x1b[38;2;173;173;173;48;2;248;248;248m 5 \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m        \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mprevious_value\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;102;102;102;48;2;248;248;248m=\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;128;0;48;2;248;248;248mnext\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m(\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248miter_values\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m)\x1b[0m\x1b[48;2;248;248;248m                 \x1b[0m│\n│\x1b[1;38;2;24;24;24;48;2;248;248;248m  \x1b[0m\x1b[38;2;173;173;173;48;2;248;248;248m 6 \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m    \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248mexcept\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[1;38;2;210;65;58;48;2;248;248;248mStopIteration\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m:\x1b[0m\x1b[48;2;248;248;248m                                  \x1b[0m│\n│\x1b[1;38;2;24;24;24;48;2;248;248;248m  \x1b[0m\x1b[38;2;173;173;173;48;2;248;248;248m 7 \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m        \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248mreturn\x1b[0m\x1b[48;2;248;248;248m                                             \x1b[0m│\n│\x1b[1;38;2;24;24;24;48;2;248;248;248m  \x1b[0m\x1b[38;2;173;173;173;48;2;248;248;248m 8 \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m    \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mfirst\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;102;102;102;48;2;248;248;248m=\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248mTrue\x1b[0m\x1b[48;2;248;248;248m                                           \x1b[0m│\n│\x1b[1;38;2;24;24;24;48;2;248;248;248m  \x1b[0m\x1b[38;2;173;173;173;48;2;248;248;248m 9 \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m    \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248mfor\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mvalue\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[1;38;2;170;34;255;48;2;248;248;248min\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248miter_values\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m:\x1b[0m\x1b[48;2;248;248;248m                              \x1b[0m│\n│\x1b[1;38;2;24;24;24;48;2;248;248;248m  \x1b[0m\x1b[38;2;173;173;173;48;2;248;248;248m10 \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m        \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248myield\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mfirst\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m,\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248mFalse\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m,\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mprevious_value\x1b[0m\x1b[48;2;248;248;248m                 \x1b[0m│\n╰────────────────────────────────────────────────────────────────╯\n'
    assert rendered_syntax == expected


def test_python_render_simple():
    syntax = Syntax(
        CODE,
        lexer_name="python",
        line_numbers=False,
        theme="foo",
        code_width=60,
        word_wrap=False,
    )
    rendered_syntax = render(syntax)
    print(repr(rendered_syntax))
    expected = '\x1b[1;38;2;0;128;0;48;2;248;248;248mdef\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;0;255;48;2;248;248;248mloop_first_last\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m(\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mvalues\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m:\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mIterable\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m[\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mT\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m]\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m)\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;102;102;102;48;2;248;248;248m-\x1b[0m\x1b[38;2;102;102;102;48;2;248;248;248m>\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mIterable\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m[\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mTuple\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m[\x1b[0m\x1b[38;2;0;128;0;48;2;248;248;248mb\x1b[0m\n\x1b[38;2;0;0;0;48;2;248;248;248m    \x1b[0m\x1b[3;38;2;186;33;33;48;2;248;248;248m"""Iterate and generate a tuple with a flag for first an\x1b[0m\n\x1b[38;2;0;0;0;48;2;248;248;248m    \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248miter_values\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;102;102;102;48;2;248;248;248m=\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;128;0;48;2;248;248;248miter\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m(\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mvalues\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m)\x1b[0m\x1b[48;2;248;248;248m                              \x1b[0m\n\x1b[38;2;0;0;0;48;2;248;248;248m    \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248mtry\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m:\x1b[0m\x1b[48;2;248;248;248m                                                    \x1b[0m\n\x1b[38;2;0;0;0;48;2;248;248;248m        \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mprevious_value\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;102;102;102;48;2;248;248;248m=\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;128;0;48;2;248;248;248mnext\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m(\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248miter_values\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m)\x1b[0m\x1b[48;2;248;248;248m                  \x1b[0m\n\x1b[38;2;0;0;0;48;2;248;248;248m    \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248mexcept\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[1;38;2;210;65;58;48;2;248;248;248mStopIteration\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m:\x1b[0m\x1b[48;2;248;248;248m                                   \x1b[0m\n\x1b[38;2;0;0;0;48;2;248;248;248m        \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248mreturn\x1b[0m\x1b[48;2;248;248;248m                                              \x1b[0m\n\x1b[38;2;0;0;0;48;2;248;248;248m    \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mfirst\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;102;102;102;48;2;248;248;248m=\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248mTrue\x1b[0m\x1b[48;2;248;248;248m                                            \x1b[0m\n\x1b[38;2;0;0;0;48;2;248;248;248m    \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248mfor\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mvalue\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[1;38;2;170;34;255;48;2;248;248;248min\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248miter_values\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m:\x1b[0m\x1b[48;2;248;248;248m                               \x1b[0m\n\x1b[38;2;0;0;0;48;2;248;248;248m        \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248myield\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mfirst\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m,\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248mFalse\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m,\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mprevious_value\x1b[0m\x1b[48;2;248;248;248m                  \x1b[0m\n\x1b[38;2;0;0;0;48;2;248;248;248m        \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mfirst\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;102;102;102;48;2;248;248;248m=\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248mFalse\x1b[0m\x1b[48;2;248;248;248m                                       \x1b[0m\n\x1b[38;2;0;0;0;48;2;248;248;248m        \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mprevious_value\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;102;102;102;48;2;248;248;248m=\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mvalue\x1b[0m\x1b[48;2;248;248;248m                              \x1b[0m\n\x1b[38;2;0;0;0;48;2;248;248;248m    \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248myield\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mfirst\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m,\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248mTrue\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m,\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mprevious_value\x1b[0m\x1b[48;2;248;248;248m                       \x1b[0m\n'
    assert rendered_syntax == expected


def test_python_render_simple_indent_guides():
    syntax = Syntax(
        CODE,
        lexer_name="python",
        line_numbers=False,
        theme="ansi_light",
        code_width=60,
        word_wrap=False,
        indent_guides=True,
    )
    rendered_syntax = render(syntax)
    print(repr(rendered_syntax))
    expected = '\x1b[34mdef\x1b[0m \x1b[32mloop_first_last\x1b[0m(values: Iterable[T]) -> Iterable[Tuple[\x1b[36mb\x1b[0m\n\x1b[2m│   \x1b[0m\x1b[33m"""Iterate and generate a tuple with a flag for first an\x1b[0m\n\x1b[2m│   \x1b[0miter_values = \x1b[36miter\x1b[0m(values)\n\x1b[2m│   \x1b[0m\x1b[34mtry\x1b[0m:\n\x1b[2m│   │   \x1b[0mprevious_value = \x1b[36mnext\x1b[0m(iter_values)\n\x1b[2m│   \x1b[0m\x1b[34mexcept\x1b[0m \x1b[36mStopIteration\x1b[0m:\n\x1b[2m│   │   \x1b[0m\x1b[34mreturn\x1b[0m\n\x1b[2m│   \x1b[0mfirst = \x1b[34mTrue\x1b[0m\n\x1b[2m│   \x1b[0m\x1b[34mfor\x1b[0m value \x1b[35min\x1b[0m iter_values:\n\x1b[2m│   │   \x1b[0m\x1b[34myield\x1b[0m first, \x1b[34mFalse\x1b[0m, previous_value\n\x1b[2m│   │   \x1b[0mfirst = \x1b[34mFalse\x1b[0m\n\x1b[2m│   │   \x1b[0mprevious_value = value\n\x1b[2m│   \x1b[0m\x1b[34myield\x1b[0m first, \x1b[34mTrue\x1b[0m, previous_value\n'
    assert rendered_syntax == expected


def test_python_render_line_range_indent_guides():
    syntax = Syntax(
        CODE,
        lexer_name="python",
        line_numbers=False,
        theme="ansi_light",
        code_width=60,
        word_wrap=False,
        line_range=(2, 3),
        indent_guides=True,
    )
    rendered_syntax = render(syntax)
    print(repr(rendered_syntax))
    expected = '\x1b[2m│   \x1b[0m\x1b[33m"""Iterate and generate a tuple with a flag for first an\x1b[0m\n\x1b[2m│   \x1b[0miter_values = \x1b[36miter\x1b[0m(values)\n'
    assert rendered_syntax == expected


def test_python_render_indent_guides():
    syntax = Panel.fit(
        Syntax(
            CODE,
            lexer_name="python",
            line_numbers=True,
            line_range=(2, 10),
            theme="foo",
            code_width=60,
            word_wrap=True,
            indent_guides=True,
        ),
        padding=0,
    )
    rendered_syntax = render(syntax)
    print(repr(rendered_syntax))
    expected = '╭────────────────────────────────────────────────────────────────╮\n│\x1b[1;38;2;24;24;24;48;2;248;248;248m  \x1b[0m\x1b[38;2;173;173;173;48;2;248;248;248m 2 \x1b[0m\x1b[2;3;38;2;64;128;128;48;2;248;248;248m│   \x1b[0m\x1b[3;38;2;186;33;33;48;2;248;248;248m"""Iterate and generate a tuple with a flag for first \x1b[0m\x1b[48;2;248;248;248m \x1b[0m│\n│\x1b[48;2;248;248;248m     \x1b[0m\x1b[3;38;2;186;33;33;48;2;248;248;248mand last value."""\x1b[0m\x1b[48;2;248;248;248m                                         \x1b[0m│\n│\x1b[1;38;2;24;24;24;48;2;248;248;248m  \x1b[0m\x1b[38;2;173;173;173;48;2;248;248;248m 3 \x1b[0m\x1b[2;3;38;2;64;128;128;48;2;248;248;248m│   \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248miter_values\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;102;102;102;48;2;248;248;248m=\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;128;0;48;2;248;248;248miter\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m(\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mvalues\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m)\x1b[0m\x1b[48;2;248;248;248m                             \x1b[0m│\n│\x1b[1;38;2;24;24;24;48;2;248;248;248m  \x1b[0m\x1b[38;2;173;173;173;48;2;248;248;248m 4 \x1b[0m\x1b[2;3;38;2;64;128;128;48;2;248;248;248m│   \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248mtry\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m:\x1b[0m\x1b[48;2;248;248;248m                                                   \x1b[0m│\n│\x1b[1;38;2;24;24;24;48;2;248;248;248m  \x1b[0m\x1b[38;2;173;173;173;48;2;248;248;248m 5 \x1b[0m\x1b[2;3;38;2;64;128;128;48;2;248;248;248m│   │   \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mprevious_value\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;102;102;102;48;2;248;248;248m=\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;128;0;48;2;248;248;248mnext\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m(\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248miter_values\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m)\x1b[0m\x1b[48;2;248;248;248m                 \x1b[0m│\n│\x1b[1;38;2;24;24;24;48;2;248;248;248m  \x1b[0m\x1b[38;2;173;173;173;48;2;248;248;248m 6 \x1b[0m\x1b[2;3;38;2;64;128;128;48;2;248;248;248m│   \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248mexcept\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[1;38;2;210;65;58;48;2;248;248;248mStopIteration\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m:\x1b[0m\x1b[48;2;248;248;248m                                  \x1b[0m│\n│\x1b[1;38;2;24;24;24;48;2;248;248;248m  \x1b[0m\x1b[38;2;173;173;173;48;2;248;248;248m 7 \x1b[0m\x1b[2;3;38;2;64;128;128;48;2;248;248;248m│   │   \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248mreturn\x1b[0m\x1b[48;2;248;248;248m                                             \x1b[0m│\n│\x1b[1;38;2;24;24;24;48;2;248;248;248m  \x1b[0m\x1b[38;2;173;173;173;48;2;248;248;248m 8 \x1b[0m\x1b[2;3;38;2;64;128;128;48;2;248;248;248m│   \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mfirst\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;102;102;102;48;2;248;248;248m=\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248mTrue\x1b[0m\x1b[48;2;248;248;248m                                           \x1b[0m│\n│\x1b[1;38;2;24;24;24;48;2;248;248;248m  \x1b[0m\x1b[38;2;173;173;173;48;2;248;248;248m 9 \x1b[0m\x1b[2;3;38;2;64;128;128;48;2;248;248;248m│   \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248mfor\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mvalue\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[1;38;2;170;34;255;48;2;248;248;248min\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248miter_values\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m:\x1b[0m\x1b[48;2;248;248;248m                              \x1b[0m│\n│\x1b[1;38;2;24;24;24;48;2;248;248;248m  \x1b[0m\x1b[38;2;173;173;173;48;2;248;248;248m10 \x1b[0m\x1b[2;3;38;2;64;128;128;48;2;248;248;248m│   │   \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248myield\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mfirst\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m,\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248mFalse\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m,\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mprevious_value\x1b[0m\x1b[48;2;248;248;248m                 \x1b[0m│\n╰────────────────────────────────────────────────────────────────╯\n'
    assert rendered_syntax == expected


def test_pygments_syntax_theme_non_str():
    from pygments.style import Style as PygmentsStyle

    style = PygmentsSyntaxTheme(PygmentsStyle())
    assert style.get_background_style().bgcolor == Color.parse("#ffffff")


def test_pygments_syntax_theme():
    style = PygmentsSyntaxTheme("default")
    assert style.get_style_for_token("abc") == Style.parse("none")


def test_get_line_color_none():
    style = PygmentsSyntaxTheme("default")
    style._background_style = Style(bgcolor=None)
    syntax = Syntax(
        CODE,
        lexer_name="python",
        line_numbers=True,
        line_range=(2, 10),
        theme=style,
        code_width=60,
        word_wrap=True,
        background_color="red",
    )
    assert syntax._get_line_numbers_color() == Color.default()


def test_highlight_background_color():
    syntax = Syntax(
        CODE,
        lexer_name="python",
        line_numbers=True,
        line_range=(2, 10),
        theme="foo",
        code_width=60,
        word_wrap=True,
        background_color="red",
    )
    assert syntax.highlight(CODE).style == Style.parse("on red")


def test_get_number_styles():
    syntax = Syntax(CODE, "python", theme="monokai", line_numbers=True)
    console = Console(color_system="windows")
    assert syntax._get_number_styles(console=console) == (
        Style.parse("on #272822"),
        Style.parse("dim on #272822"),
        Style.parse("not dim on #272822"),
    )


def test_get_style_for_token():
    # from pygments.style import Style as PygmentsStyle
    # pygments_style = PygmentsStyle()
    from pygments.style import Token

    style = PygmentsSyntaxTheme("default")
    style_dict = {Token.Text: Style(color=None)}
    style._style_cache = style_dict
    syntax = Syntax(
        CODE,
        lexer_name="python",
        line_numbers=True,
        line_range=(2, 10),
        theme=style,
        code_width=60,
        word_wrap=True,
        background_color="red",
    )
    assert syntax._get_line_numbers_color() == Color.default()


def test_option_no_wrap():
    syntax = Syntax(
        CODE,
        lexer_name="python",
        line_numbers=True,
        line_range=(2, 10),
        code_width=60,
        word_wrap=False,
        background_color="red",
    )

    rendered_syntax = render(syntax, True)
    print(repr(rendered_syntax))
    expected = '\x1b[1;39;41m  \x1b[0m\x1b[39;41m 2 \x1b[0m\x1b[38;2;248;248;242;41m    \x1b[0m\x1b[38;2;230;219;116;41m"""Iterate and generate a tuple with a flag for first and last value."""\x1b[0m\n\x1b[1;39;41m  \x1b[0m\x1b[39;41m 3 \x1b[0m\x1b[38;2;248;248;242;41m    \x1b[0m\x1b[38;2;248;248;242;41miter_values\x1b[0m\x1b[38;2;248;248;242;41m \x1b[0m\x1b[38;2;249;38;114;41m=\x1b[0m\x1b[38;2;248;248;242;41m \x1b[0m\x1b[38;2;248;248;242;41miter\x1b[0m\x1b[38;2;248;248;242;41m(\x1b[0m\x1b[38;2;248;248;242;41mvalues\x1b[0m\x1b[38;2;248;248;242;41m)\x1b[0m\n\x1b[1;39;41m  \x1b[0m\x1b[39;41m 4 \x1b[0m\x1b[38;2;248;248;242;41m    \x1b[0m\x1b[38;2;102;217;239;41mtry\x1b[0m\x1b[38;2;248;248;242;41m:\x1b[0m\n\x1b[1;39;41m  \x1b[0m\x1b[39;41m 5 \x1b[0m\x1b[38;2;248;248;242;41m        \x1b[0m\x1b[38;2;248;248;242;41mprevious_value\x1b[0m\x1b[38;2;248;248;242;41m \x1b[0m\x1b[38;2;249;38;114;41m=\x1b[0m\x1b[38;2;248;248;242;41m \x1b[0m\x1b[38;2;248;248;242;41mnext\x1b[0m\x1b[38;2;248;248;242;41m(\x1b[0m\x1b[38;2;248;248;242;41miter_values\x1b[0m\x1b[38;2;248;248;242;41m)\x1b[0m\n\x1b[1;39;41m  \x1b[0m\x1b[39;41m 6 \x1b[0m\x1b[38;2;248;248;242;41m    \x1b[0m\x1b[38;2;102;217;239;41mexcept\x1b[0m\x1b[38;2;248;248;242;41m \x1b[0m\x1b[38;2;166;226;46;41mStopIteration\x1b[0m\x1b[38;2;248;248;242;41m:\x1b[0m\n\x1b[1;39;41m  \x1b[0m\x1b[39;41m 7 \x1b[0m\x1b[38;2;248;248;242;41m        \x1b[0m\x1b[38;2;102;217;239;41mreturn\x1b[0m\n\x1b[1;39;41m  \x1b[0m\x1b[39;41m 8 \x1b[0m\x1b[38;2;248;248;242;41m    \x1b[0m\x1b[38;2;248;248;242;41mfirst\x1b[0m\x1b[38;2;248;248;242;41m \x1b[0m\x1b[38;2;249;38;114;41m=\x1b[0m\x1b[38;2;248;248;242;41m \x1b[0m\x1b[38;2;102;217;239;41mTrue\x1b[0m\n\x1b[1;39;41m  \x1b[0m\x1b[39;41m 9 \x1b[0m\x1b[38;2;248;248;242;41m    \x1b[0m\x1b[38;2;102;217;239;41mfor\x1b[0m\x1b[38;2;248;248;242;41m \x1b[0m\x1b[38;2;248;248;242;41mvalue\x1b[0m\x1b[38;2;248;248;242;41m \x1b[0m\x1b[38;2;249;38;114;41min\x1b[0m\x1b[38;2;248;248;242;41m \x1b[0m\x1b[38;2;248;248;242;41miter_values\x1b[0m\x1b[38;2;248;248;242;41m:\x1b[0m\n\x1b[1;39;41m  \x1b[0m\x1b[39;41m10 \x1b[0m\x1b[38;2;248;248;242;41m        \x1b[0m\x1b[38;2;102;217;239;41myield\x1b[0m\x1b[38;2;248;248;242;41m \x1b[0m\x1b[38;2;248;248;242;41mfirst\x1b[0m\x1b[38;2;248;248;242;41m,\x1b[0m\x1b[38;2;248;248;242;41m \x1b[0m\x1b[38;2;102;217;239;41mFalse\x1b[0m\x1b[38;2;248;248;242;41m,\x1b[0m\x1b[38;2;248;248;242;41m \x1b[0m\x1b[38;2;248;248;242;41mprevious_value\x1b[0m\n'
    assert rendered_syntax == expected


def test_ansi_theme():
    style = Style(color="red")
    theme = ANSISyntaxTheme({("foo", "bar"): style})
    assert theme.get_style_for_token(("foo", "bar", "baz")) == style
    assert theme.get_background_style() == Style()


@pytest.mark.skipif(sys.platform == "win32", reason="permissions error on Windows")
def test_from_file():
    fh, path = tempfile.mkstemp("example.py")
    try:
        os.write(fh, b"import this\n")
        syntax = Syntax.from_path(path)
        assert syntax.lexer_name == "Python"
        assert syntax.code == "import this\n"
    finally:
        os.remove(path)


@pytest.mark.skipif(sys.platform == "win32", reason="permissions error on Windows")
def test_from_file_unknown_lexer():
    fh, path = tempfile.mkstemp("example.nosuchtype")
    try:
        os.write(fh, b"import this\n")
        syntax = Syntax.from_path(path)
        assert syntax.lexer_name == "default"
        assert syntax.code == "import this\n"
    finally:
        os.remove(path)


if __name__ == "__main__":
    syntax = Panel.fit(
        Syntax(
            CODE,
            lexer_name="python",
            line_numbers=True,
            line_range=(2, 10),
            theme="foo",
            code_width=60,
            word_wrap=True,
        ),
        padding=0,
    )
    rendered = render(markdown)
    print(rendered)
    print(repr(rendered))
