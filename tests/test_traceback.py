import io
import sys

import pytest

from rich.console import Console
from rich.theme import Theme
from rich.traceback import Traceback, install

# from .render import render

try:
    from ._exception_render import expected
except ImportError:
    expected = None


CAPTURED_EXCEPTION = 'Traceback (most recent call last):\n╭──────────────────────────────────────────────────────────────────────────────────────────────────╮\n│ File "/Users/willmcgugan/projects/rich/tests/test_traceback.py", line 26, in test_handler        │\n│    23     try:                                                                                   │\n│    24         old_handler = install(console=console, line_numbers=False)                         │\n│    25         try:                                                                               │\n│  ❱ 26             1 / 0                                                                          │\n│    27         except Exception:                                                                  │\n│    28             exc_type, exc_value, traceback = sys.exc_info()                                │\n│    29             sys.excepthook(exc_type, exc_value, traceback)                                 │\n╰──────────────────────────────────────────────────────────────────────────────────────────────────╯\nZeroDivisionError: division by zero\n'


def test_handler():
    console = Console(file=io.StringIO(), width=100, color_system=None)
    expected_old_handler = sys.excepthook
    try:
        old_handler = install(console=console)
        try:
            1 / 0
        except Exception:
            exc_type, exc_value, traceback = sys.exc_info()
            sys.excepthook(exc_type, exc_value, traceback)
            rendered_exception = console.file.getvalue()
            print(repr(rendered_exception))
            assert "Traceback" in rendered_exception
            assert "ZeroDivisionError" in rendered_exception
    finally:
        sys.excepthook = old_handler
        assert old_handler == expected_old_handler


def text_exception_render():
    exc_render = render(get_exception())
    assert exc_render == expected


def test_capture():
    try:
        1 / 0
    except Exception:
        tb = Traceback()
        assert tb.trace.stacks[0].exc_type == "ZeroDivisionError"


def test_no_exception():
    with pytest.raises(ValueError):
        tb = Traceback()


def get_exception() -> Traceback:
    def bar(a):
        print(1 / a)

    def foo(a):
        bar(a)

    try:
        try:
            foo(0)
        except:
            foobarbaz
    except:
        tb = Traceback()
        return tb


def test_print_exception():
    console = Console(width=100, file=io.StringIO())
    try:
        1 / 0
    except Exception:
        console.print_exception()
    exception_text = console.file.getvalue()
    assert "ZeroDivisionError" in exception_text


def test_print_exception_no_msg():
    console = Console(width=100, file=io.StringIO())
    try:
        raise RuntimeError
    except Exception:
        console.print_exception()
    exception_text = console.file.getvalue()
    assert "RuntimeError" in exception_text
    assert "RuntimeError:" not in exception_text


def test_print_exception_locals():
    console = Console(width=100, file=io.StringIO())
    try:
        1 / 0
    except Exception:
        console.print_exception(show_locals=True)
    exception_text = console.file.getvalue()
    print(exception_text)
    assert "ZeroDivisionError" in exception_text
    assert "locals" in exception_text
    assert "console = <console width=100 None>" in exception_text


def test_syntax_error():
    console = Console(width=100, file=io.StringIO())
    try:
        # raises SyntaxError: unexpected EOF while parsing
        eval("(2+2")
    except SyntaxError:
        console.print_exception()
    exception_text = console.file.getvalue()
    assert "SyntaxError" in exception_text


def test_nested_exception():
    console = Console(width=100, file=io.StringIO())
    value_error_message = "ValueError because of ZeroDivisionError"

    try:
        try:
            1 / 0
        except ZeroDivisionError:
            raise ValueError(value_error_message)
    except Exception:
        console.print_exception()
    exception_text = console.file.getvalue()

    text_should_contain = [
        value_error_message,
        "ZeroDivisionError",
        "ValueError",
        "During handling of the above exception",
    ]

    for msg in text_should_contain:
        assert msg in exception_text

    # ZeroDivisionError should come before ValueError
    assert exception_text.find("ZeroDivisionError") < exception_text.find("ValueError")


def test_caused_exception():
    console = Console(width=100, file=io.StringIO())
    value_error_message = "ValueError caused by ZeroDivisionError"

    try:
        try:
            1 / 0
        except ZeroDivisionError as e:
            raise ValueError(value_error_message) from e
    except Exception:
        console.print_exception()
    exception_text = console.file.getvalue()

    text_should_contain = [
        value_error_message,
        "ZeroDivisionError",
        "ValueError",
        "The above exception was the direct cause",
    ]

    for msg in text_should_contain:
        assert msg in exception_text

    # ZeroDivisionError should come before ValueError
    assert exception_text.find("ZeroDivisionError") < exception_text.find("ValueError")


def test_filename_with_bracket():
    console = Console(width=100, file=io.StringIO())
    try:
        exec(compile("1/0", filename="<string>", mode="exec"))
    except Exception:
        console.print_exception()
    exception_text = console.file.getvalue()
    assert "<string>" in exception_text


def test_filename_not_a_file():
    console = Console(width=100, file=io.StringIO())
    try:
        exec(compile("1/0", filename="string", mode="exec"))
    except Exception:
        console.print_exception()
    exception_text = console.file.getvalue()
    assert "string" in exception_text


@pytest.mark.skipif(sys.platform == "win32", reason="renders different on windows")
def test_traceback_console_theme_applies():
    """
    Ensure that themes supplied via Console init work on Tracebacks.
    Regression test for https://github.com/Textualize/rich/issues/1786
    """
    r, g, b = 123, 234, 123
    console = Console(
        force_terminal=True,
        _environ={"COLORTERM": "truecolor"},
        theme=Theme({"traceback.title": f"rgb({r},{g},{b})"}),
    )

    console.begin_capture()
    try:
        1 / 0
    except Exception:
        console.print_exception()

    result = console.end_capture()

    assert f"\\x1b[38;2;{r};{g};{b}mTraceback \\x1b[0m" in repr(result)


def test_broken_str():
    class BrokenStr(Exception):
        def __str__(self):
            1 / 0

    console = Console(width=100, file=io.StringIO())
    try:
        raise BrokenStr()
    except Exception:
        console.print_exception()
    result = console.file.getvalue()
    print(result)
    assert "<exception str() failed>" in result


def test_guess_lexer():
    assert Traceback._guess_lexer("foo.py", "code") == "python"
    code_python = "#! usr/bin/env python\nimport this"
    assert Traceback._guess_lexer("foo", code_python) == "python"
    assert Traceback._guess_lexer("foo", "foo\nbnar") == "text"


def test_guess_lexer_yaml_j2():
    # https://github.com/Textualize/rich/issues/2018
    code = """\
foobar:
    something: {{ raiser() }}
    else: {{ 5 + 5 }}
    """
    assert Traceback._guess_lexer("test.yaml.j2", code) == "text"


def test_recursive():
    def foo(n):
        return bar(n)

    def bar(n):
        return foo(n)

    console = Console(width=100, file=io.StringIO())
    try:
        foo(1)
    except Exception:
        console.print_exception(max_frames=6)
    result = console.file.getvalue()
    print(result)
    assert "frames hidden" in result
    assert result.count("in foo") < 4


def test_suppress():
    try:
        1 / 0
    except Exception:
        traceback = Traceback(suppress=[pytest, "foo"])
        assert len(traceback.suppress) == 2
        assert "pytest" in traceback.suppress[0]
        assert "foo" in traceback.suppress[1]


if __name__ == "__main__":  # pragma: no cover

    expected = render(get_exception())

    with open("_exception_render.py", "wt") as fh:
        exc_render = render(get_exception())
        print(exc_render)
        fh.write(f"expected={exc_render!r}")
