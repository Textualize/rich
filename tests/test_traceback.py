import io
import sys

import pytest

from rich.console import Console
from rich.traceback import install, Traceback

from .render import render

try:
    from _exception_render import expected
except ImportError:
    expected = None


CAPTURED_EXCEPTION = 'Traceback (most recent call last):\n╭──────────────────────────────────────────────────────────────────────────────────────────────────╮\n│ File "/Users/willmcgugan/projects/rich/tests/test_traceback.py", line 26, in test_handler        │\n│    23     try:                                                                                   │\n│    24         old_handler = install(console=console, line_numbers=False)                         │\n│    25         try:                                                                               │\n│  ❱ 26             1 / 0                                                                          │\n│    27         except Exception:                                                                  │\n│    28             exc_type, exc_value, traceback = sys.exc_info()                                │\n│    29             sys.excepthook(exc_type, exc_value, traceback)                                 │\n╰──────────────────────────────────────────────────────────────────────────────────────────────────╯\nZeroDivisionError: division by zero\n'


def test_handler():
    console = Console(file=io.StringIO(), width=100, color_system=None)
    expected_old_handler = sys.excepthook
    try:
        old_handler = install(console=console, line_numbers=False)
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


if __name__ == "__main__":  # pragma: no cover

    expected = render(get_exception())

    with open("_exception_render.py", "wt") as fh:
        exc_render = render(get_exception())
        print(exc_render)
        fh.write(f"expected={exc_render!r}")
