import io
import re
import sys
from typing import List

import pytest

from rich.console import Console
from rich.theme import Theme
from rich.traceback import Traceback, install


def test_handler():
    console = Console(file=io.StringIO(), width=100, color_system=None)
    expected_old_handler = sys.excepthook

    def level1():
        level2()

    def level2():
        return 1 / 0

    try:
        old_handler = install(console=console)
        try:
            level1()
        except Exception:
            exc_type, exc_value, traceback = sys.exc_info()
            sys.excepthook(exc_type, exc_value, traceback)
            rendered_exception = console.file.getvalue()
            print(repr(rendered_exception))
            assert "Traceback" in rendered_exception
            assert "ZeroDivisionError" in rendered_exception

            frame_blank_line_possible_preambles = (
                # Start of the stack rendering:
                "╭─────────────────────────────── Traceback (most recent call last) ────────────────────────────────╮",
                # Each subsequent frame (starting with the file name) should then be preceded with a blank line:
                "│" + (" " * 98) + "│",
            )
            for frame_start in re.finditer(
                "^│ .+rich/tests/test_traceback.py:",
                rendered_exception,
                flags=re.MULTILINE,
            ):
                frame_start_index = frame_start.start()
                for preamble in frame_blank_line_possible_preambles:
                    preamble_start, preamble_end = (
                        frame_start_index - len(preamble) - 1,
                        frame_start_index - 1,
                    )
                    if rendered_exception[preamble_start:preamble_end] == preamble:
                        break
                else:
                    pytest.fail(
                        f"Frame {frame_start[0]} doesn't have the expected preamble"
                    )
    finally:
        sys.excepthook = old_handler
        assert old_handler == expected_old_handler


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
    assert Traceback._guess_lexer("test.yaml.j2", code) in ("text", "YAML+Jinja")


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


@pytest.mark.parametrize(
    "rich_traceback_omit_for_level2,expected_frames_length,expected_frame_names",
    (
        # fmt: off
        [True, 3, ["test_rich_traceback_omit_optional_local_flag", "level1", "level3"]],
        [False, 4, ["test_rich_traceback_omit_optional_local_flag", "level1", "level2", "level3"]],
        # fmt: on
    ),
)
def test_rich_traceback_omit_optional_local_flag(
    rich_traceback_omit_for_level2: bool,
    expected_frames_length: int,
    expected_frame_names: List[str],
):
    def level1():
        return level2()

    def level2():
        # true-ish values are enough to trigger the opt-out:
        _rich_traceback_omit = 1 if rich_traceback_omit_for_level2 else 0
        return level3()

    def level3():
        return 1 / 0

    try:
        level1()
    except Exception:
        exc_type, exc_value, traceback = sys.exc_info()
        trace = Traceback.from_exception(exc_type, exc_value, traceback).trace
        frames = trace.stacks[0].frames
        assert len(frames) == expected_frames_length
        frame_names = [f.name for f in frames]
        assert frame_names == expected_frame_names


@pytest.mark.skipif(
    sys.version_info.minor >= 11, reason="Not applicable after Python 3.11"
)
def test_traceback_finely_grained_missing() -> None:
    """Before 3.11, the last_instruction should be None"""
    try:
        1 / 0
    except:
        traceback = Traceback()
        last_instruction = traceback.trace.stacks[-1].frames[-1].last_instruction
        assert last_instruction is None


@pytest.mark.skipif(
    sys.version_info.minor < 11, reason="Not applicable before Python 3.11"
)
def test_traceback_finely_grained() -> None:
    """Check that last instruction is populated."""
    try:
        1 / 0
    except:
        traceback = Traceback()
        last_instruction = traceback.trace.stacks[-1].frames[-1].last_instruction
        assert last_instruction is not None
        assert isinstance(last_instruction, tuple)
        assert len(last_instruction) == 2
        start, end = last_instruction
        print(start, end)
        assert start[0] == end[0]


@pytest.mark.skipif(
    sys.version_info.minor < 11, reason="Not supported before Python 3.11"
)
def test_notes() -> None:
    """Check traceback captures __note__."""
    try:
        1 / 0
    except Exception as error:
        error.add_note("Hello")
        error.add_note("World")
        traceback = Traceback()

        assert traceback.trace.stacks[0].notes == ["Hello", "World"]


def test_recursive_exception() -> None:
    """Regression test for https://github.com/Textualize/rich/issues/3708

    Test this doesn't create an infinite loop.

    """
    console = Console()

    def foo() -> None:
        try:
            raise RuntimeError("Hello")
        except Exception as e:
            raise e from e

    def bar() -> None:
        try:
            foo()
        except Exception as e:
            assert e is e.__cause__
            console.print_exception(show_locals=True)

    bar()


def test_notes_dont_leak_across_chained_exceptions():
    """Test that __notes__ from one exception don't appear on chained exceptions.

    Regression test for https://github.com/Textualize/rich/issues/3960
    """
    console = Console(width=100, file=io.StringIO())

    try:
        try:
            try:
                raise ValueError("outer")
            except ValueError as e:
                e.__notes__ = ["note on outer"]
                raise RuntimeError("inner") from e
        except RuntimeError as e:
            e.__notes__ = ["note on inner"]
            raise
    except RuntimeError:
        console.print_exception()

    output = console.file.getvalue()

    # The inner (RuntimeError) should only have "note on inner"
    # The outer (ValueError) should only have "note on outer"
    # They should NOT have each other's notes

    # Find the section for RuntimeError and ValueError
    # RuntimeError comes first (it's the outermost), ValueError is the cause
    lines = output.split("\n")

    # Track which notes appear near which exception
    runtime_error_lines = []
    value_error_lines = []
    current_section = None

    for line in lines:
        if "RuntimeError" in line:
            current_section = "runtime"
        elif "ValueError" in line:
            current_section = "value"

        if "note on" in line:
            if current_section == "runtime":
                runtime_error_lines.append(line.strip())
            elif current_section == "value":
                value_error_lines.append(line.strip())

    # RuntimeError should have its own note but NOT ValueError's note
    assert any("note on inner" in l for l in runtime_error_lines), f"RuntimeError should have 'note on inner', got: {runtime_error_lines}"
    assert not any("note on outer" in l for l in runtime_error_lines), f"RuntimeError should NOT have 'note on outer', got: {runtime_error_lines}"

    # ValueError should have its own note but NOT RuntimeError's note
    assert any("note on outer" in l for l in value_error_lines), f"ValueError should have 'note on outer', got: {value_error_lines}"
    assert not any("note on inner" in l for l in value_error_lines), f"ValueError should NOT have 'note on inner', got: {value_error_lines}"
