# coding=utf-8

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

import os, tempfile

from .render import render

from rich.panel import Panel
from rich.style import Style
from rich.syntax import Syntax, ANSISyntaxTheme


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
        )
    )
    rendered_syntax = render(syntax)
    print(repr(rendered_syntax))
    expected = '╭────────────────────────────────────────────────────────────────╮\n│\x1b[1;38;2;24;24;24;48;2;248;248;248m  \x1b[0m\x1b[38;2;173;173;173;48;2;248;248;248m 2 \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m    \x1b[0m\x1b[3;38;2;186;33;33;48;2;248;248;248m"""Iterate and generate a tuple with a flag for first \x1b[0m\x1b[48;2;248;248;248m \x1b[0m│\n│\x1b[48;2;248;248;248m     \x1b[0m\x1b[3;38;2;186;33;33;48;2;248;248;248mand last value."""\x1b[0m\x1b[48;2;248;248;248m                                         \x1b[0m│\n│\x1b[1;38;2;24;24;24;48;2;248;248;248m  \x1b[0m\x1b[38;2;173;173;173;48;2;248;248;248m 3 \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m    \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248miter_values\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;102;102;102;48;2;248;248;248m=\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;128;0;48;2;248;248;248miter\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m(\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mvalues\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m)\x1b[0m\x1b[48;2;248;248;248m                             \x1b[0m│\n│\x1b[1;38;2;24;24;24;48;2;248;248;248m  \x1b[0m\x1b[38;2;173;173;173;48;2;248;248;248m 4 \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m    \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248mtry\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m:\x1b[0m\x1b[48;2;248;248;248m                                                   \x1b[0m│\n│\x1b[1;38;2;24;24;24;48;2;248;248;248m  \x1b[0m\x1b[38;2;173;173;173;48;2;248;248;248m 5 \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m        \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mprevious_value\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;102;102;102;48;2;248;248;248m=\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;128;0;48;2;248;248;248mnext\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m(\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248miter_values\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m)\x1b[0m\x1b[48;2;248;248;248m                 \x1b[0m│\n│\x1b[1;38;2;24;24;24;48;2;248;248;248m  \x1b[0m\x1b[38;2;173;173;173;48;2;248;248;248m 6 \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m    \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248mexcept\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[1;38;2;210;65;58;48;2;248;248;248mStopIteration\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m:\x1b[0m\x1b[48;2;248;248;248m                                  \x1b[0m│\n│\x1b[1;38;2;24;24;24;48;2;248;248;248m  \x1b[0m\x1b[38;2;173;173;173;48;2;248;248;248m 7 \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m        \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248mreturn\x1b[0m\x1b[48;2;248;248;248m                                             \x1b[0m│\n│\x1b[1;38;2;24;24;24;48;2;248;248;248m  \x1b[0m\x1b[38;2;173;173;173;48;2;248;248;248m 8 \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m    \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mfirst\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;102;102;102;48;2;248;248;248m=\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248mTrue\x1b[0m\x1b[48;2;248;248;248m                                           \x1b[0m│\n│\x1b[1;38;2;24;24;24;48;2;248;248;248m  \x1b[0m\x1b[38;2;173;173;173;48;2;248;248;248m 9 \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m    \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248mfor\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mvalue\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[1;38;2;170;34;255;48;2;248;248;248min\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248miter_values\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m:\x1b[0m\x1b[48;2;248;248;248m                              \x1b[0m│\n│\x1b[1;38;2;24;24;24;48;2;248;248;248m  \x1b[0m\x1b[38;2;173;173;173;48;2;248;248;248m10 \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m        \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248myield\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mfirst\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m,\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[1;38;2;0;128;0;48;2;248;248;248mFalse\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m,\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248mprevious_value\x1b[0m\x1b[48;2;248;248;248m                 \x1b[0m│\n╰────────────────────────────────────────────────────────────────╯\n'
    assert rendered_syntax == expected


def test_ansi_theme():
    style = Style(color="red")
    theme = ANSISyntaxTheme({("foo", "bar"): style})
    assert theme.get_style_for_token(("foo", "bar", "baz")) == style
    assert theme.get_background_style() == Style()


def test_from_file():
    fh, path = tempfile.mkstemp("example.py")
    try:
        os.write(fh, b"import this\n")
        syntax = Syntax.from_path(path)
        assert syntax.lexer_name == "Python"
        assert syntax.code == "import this\n"
    finally:
        os.remove(path)


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
        )
    )
    rendered = render(markdown)
    print(rendered)
    print(repr(rendered))
