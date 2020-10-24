import io
import os
import sys
import tempfile
from typing import Optional

import pytest

from rich import errors
from rich.color import ColorSystem
from rich.console import CaptureError, Console, ConsoleOptions, render_group
from rich.measure import measure_renderables
from rich.pager import SystemPager
from rich.panel import Panel
from rich.style import Style


def test_dumb_terminal():
    console = Console(force_terminal=True)
    assert console.color_system is not None

    console = Console(force_terminal=True, _environ={"TERM": "dumb"})
    assert console.color_system is None
    width, height = console.size
    assert width == 80
    assert height == 25


@pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")
def test_16color_terminal():
    console = Console(
        force_terminal=True, _environ={"TERM": "xterm-16color"}, legacy_windows=False
    )
    assert console.color_system == "standard"


@pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")
def test_truecolor_terminal():
    console = Console(
        force_terminal=True,
        legacy_windows=False,
        _environ={"COLORTERM": "truecolor", "TERM": "xterm-16color"},
    )
    assert console.color_system == "truecolor"


def test_console_options_update():
    options = ConsoleOptions(
        legacy_windows=False,
        min_width=10,
        max_width=20,
        is_terminal=False,
        encoding="utf-8",
    )
    options1 = options.update(width=15)
    assert options1.min_width == 15 and options1.max_width == 15

    options2 = options.update(min_width=5, max_width=15, justify="right")
    assert (
        options2.min_width == 5
        and options2.max_width == 15
        and options2.justify == "right"
    )

    options_copy = options.update()
    assert options_copy == options and options_copy is not options


def test_init():
    console = Console(color_system=None)
    assert console._color_system == None
    console = Console(color_system="standard")
    assert console._color_system == ColorSystem.STANDARD
    console = Console(color_system="auto")


def test_size():
    console = Console()
    w, h = console.size
    assert console.width == w

    console = Console(width=99, height=101)
    w, h = console.size
    assert w == 99 and h == 101


def test_repr():
    console = Console()
    assert isinstance(repr(console), str)
    assert isinstance(str(console), str)


def test_print():
    console = Console(file=io.StringIO(), color_system="truecolor")
    console.print("foo")
    assert console.file.getvalue() == "foo\n"


def test_print_empty():
    console = Console(file=io.StringIO(), color_system="truecolor")
    console.print()
    assert console.file.getvalue() == "\n"


def test_markup_highlight():
    console = Console(file=io.StringIO(), color_system="truecolor")
    console.print("'[bold]foo[/bold]'")
    assert (
        console.file.getvalue()
        == "\x1b[32m'\x1b[0m\x1b[1;32mfoo\x1b[0m\x1b[32m'\x1b[0m\n"
    )


def test_print_style():
    console = Console(file=io.StringIO(), color_system="truecolor")
    console.print("foo", style="bold")
    assert console.file.getvalue() == "\x1b[1mfoo\x1b[0m\n"


def test_show_cursor():
    console = Console(file=io.StringIO(), force_terminal=True, legacy_windows=False)
    console.show_cursor(False)
    console.print("foo")
    console.show_cursor(True)
    assert console.file.getvalue() == "\x1b[?25lfoo\n\x1b[?25h"


def test_clear():
    console = Console(file=io.StringIO(), force_terminal=True)
    console.clear()
    console.clear(home=False)
    assert console.file.getvalue() == "\033[2J\033[H" + "\033[2J"


def test_clear_no_terminal():
    console = Console(file=io.StringIO())
    console.clear()
    console.clear(home=False)
    assert console.file.getvalue() == ""


def test_get_style():
    console = Console()
    console.get_style("repr.brace") == Style(bold=True)


def test_get_style_default():
    console = Console()
    console.get_style("foobar", default="red") == Style(color="red")


def test_get_style_error():
    console = Console()
    with pytest.raises(errors.MissingStyle):
        console.get_style("nosuchstyle")
    with pytest.raises(errors.MissingStyle):
        console.get_style("foo bar")


def test_render_error():
    console = Console()
    with pytest.raises(errors.NotRenderableError):
        list(console.render([], console.options))


def test_control():
    console = Console(file=io.StringIO(), force_terminal=True)
    console.control("FOO")
    console.print("BAR")
    assert console.file.getvalue() == "FOOBAR\n"


def test_capture():
    console = Console()
    with console.capture() as capture:
        with pytest.raises(CaptureError):
            capture.get()
        console.print("Hello")
    assert capture.get() == "Hello\n"


def test_input(monkeypatch, capsys):
    def fake_input(prompt):
        console.file.write(prompt)
        return "bar"

    monkeypatch.setattr("builtins.input", fake_input)
    console = Console()
    user_input = console.input(prompt="foo:")
    assert capsys.readouterr().out == "foo:"
    assert user_input == "bar"


def test_input_legacy_windows(monkeypatch, capsys):
    def fake_input(prompt):
        console.file.write(prompt)
        return "bar"

    monkeypatch.setattr("builtins.input", fake_input)
    console = Console(legacy_windows=True)
    user_input = console.input(prompt="foo:")
    assert capsys.readouterr().out == "foo:"
    assert user_input == "bar"


def test_input_password(monkeypatch, capsys):
    def fake_input(prompt, stream=None):
        console.file.write(prompt)
        return "bar"

    import rich.console

    monkeypatch.setattr(rich.console, "getpass", fake_input)
    console = Console()
    user_input = console.input(prompt="foo:", password=True)
    assert capsys.readouterr().out == "foo:"
    assert user_input == "bar"


def test_justify_none():
    console = Console(file=io.StringIO(), force_terminal=True, width=20)
    console.print("FOO", justify=None)
    assert console.file.getvalue() == "FOO\n"


def test_justify_left():
    console = Console(file=io.StringIO(), force_terminal=True, width=20)
    console.print("FOO", justify="left")
    assert console.file.getvalue() == "FOO                 \n"


def test_justify_center():
    console = Console(file=io.StringIO(), force_terminal=True, width=20)
    console.print("FOO", justify="center")
    assert console.file.getvalue() == "        FOO         \n"


def test_justify_right():
    console = Console(file=io.StringIO(), force_terminal=True, width=20)
    console.print("FOO", justify="right")
    assert console.file.getvalue() == "                 FOO\n"


def test_justify_renderable_none():
    console = Console(
        file=io.StringIO(), force_terminal=True, width=20, legacy_windows=False
    )
    console.print(Panel("FOO", expand=False, padding=0), justify=None)
    assert console.file.getvalue() == "╭───╮\n│FOO│\n╰───╯\n"


def test_justify_renderable_left():
    console = Console(
        file=io.StringIO(), force_terminal=True, width=10, legacy_windows=False
    )
    console.print(Panel("FOO", expand=False, padding=0), justify="left")
    assert console.file.getvalue() == "╭───╮     \n│FOO│     \n╰───╯     \n"


def test_justify_renderable_center():
    console = Console(
        file=io.StringIO(), force_terminal=True, width=10, legacy_windows=False
    )
    console.print(Panel("FOO", expand=False, padding=0), justify="center")
    assert console.file.getvalue() == "  ╭───╮   \n  │FOO│   \n  ╰───╯   \n"


def test_justify_renderable_right():
    console = Console(
        file=io.StringIO(), force_terminal=True, width=20, legacy_windows=False
    )
    console.print(Panel("FOO", expand=False, padding=0), justify="right")
    assert (
        console.file.getvalue()
        == "               ╭───╮\n               │FOO│\n               ╰───╯\n"
    )


class BrokenRenderable:
    def __rich_console__(self, console, options):
        pass


def test_render_broken_renderable():
    console = Console()
    broken = BrokenRenderable()
    with pytest.raises(errors.NotRenderableError):
        list(console.render(broken, console.options))


def test_export_text():
    console = Console(record=True, width=100)
    console.print("[b]foo")
    text = console.export_text()
    expected = "foo\n"
    assert text == expected


def test_export_html():
    console = Console(record=True, width=100)
    console.print("[b]foo [link=https://example.org]Click[/link]")
    html = console.export_html()
    expected = '<!DOCTYPE html>\n<head>\n<meta charset="UTF-8">\n<style>\n.r1 {font-weight: bold}\nbody {\n    color: #000000;\n    background-color: #ffffff;\n}\n</style>\n</head>\n<html>\n<body>\n    <code>\n        <pre style="font-family:Menlo,\'DejaVu Sans Mono\',consolas,\'Courier New\',monospace"><span class="r1">foo </span><a href="https://example.org"><span class="r1">Click</span></a>\n</pre>\n    </code>\n</body>\n</html>\n'
    assert html == expected


def test_export_html_inline():
    console = Console(record=True, width=100)
    console.print("[b]foo [link=https://example.org]Click[/link]")
    html = console.export_html(inline_styles=True)
    expected = '<!DOCTYPE html>\n<head>\n<meta charset="UTF-8">\n<style>\n\nbody {\n    color: #000000;\n    background-color: #ffffff;\n}\n</style>\n</head>\n<html>\n<body>\n    <code>\n        <pre style="font-family:Menlo,\'DejaVu Sans Mono\',consolas,\'Courier New\',monospace"><span style="font-weight: bold">foo </span><a href="https://example.org"><span style="font-weight: bold">Click</span></a>\n</pre>\n    </code>\n</body>\n</html>\n'
    assert html == expected


def test_save_text():
    console = Console(record=True, width=100)
    console.print("foo")
    with tempfile.TemporaryDirectory() as path:
        export_path = os.path.join(path, "rich.txt")
        console.save_text(export_path)
        with open(export_path, "rt") as text_file:
            assert text_file.read() == "foo\n"


def test_save_html():
    expected = "<!DOCTYPE html>\n<head>\n<meta charset=\"UTF-8\">\n<style>\n\nbody {\n    color: #000000;\n    background-color: #ffffff;\n}\n</style>\n</head>\n<html>\n<body>\n    <code>\n        <pre style=\"font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace\">foo\n</pre>\n    </code>\n</body>\n</html>\n"
    console = Console(record=True, width=100)
    console.print("foo")
    with tempfile.TemporaryDirectory() as path:
        export_path = os.path.join(path, "example.html")
        console.save_html(export_path)
        with open(export_path, "rt") as html_file:
            assert html_file.read() == expected


def test_no_wrap():
    console = Console(width=10, file=io.StringIO())
    console.print("foo bar baz egg", no_wrap=True)
    assert console.file.getvalue() == "foo bar ba\n"


def test_soft_wrap():
    console = Console(width=10, file=io.StringIO())
    console.print("foo bar baz egg", soft_wrap=True)
    assert console.file.getvalue() == "foo bar baz egg\n"


def test_unicode_error() -> None:
    try:
        with tempfile.TemporaryFile("wt", encoding="ascii") as tmpfile:
            console = Console(file=tmpfile)
            console.print(":vampire:")
    except UnicodeEncodeError as error:
        assert "PYTHONIOENCODING" in str(error)
    else:
        assert False, "didn't raise UnicodeEncodeError"


def test_bell() -> None:
    console = Console(force_terminal=True)
    console.begin_capture()
    console.bell()
    assert console.end_capture() == "\x07"


def test_pager() -> None:
    console = Console()

    pager_content: Optional[str] = None

    def mock_pager(content: str) -> None:
        nonlocal pager_content
        pager_content = content

    pager = SystemPager()
    pager._pager = mock_pager

    with console.pager(pager):
        console.print("[bold]Hello World")
    assert pager_content == "Hello World\n"

    with console.pager(pager, styles=True, links=False):
        console.print("[bold link https:/example.org]Hello World")

    assert pager_content == "Hello World\n"


def test_out() -> None:
    console = Console(width=10)
    console.begin_capture()
    console.out(*(["foo bar"] * 5), sep=".", end="X")
    assert console.end_capture() == "foo bar.foo bar.foo bar.foo bar.foo barX"


def test_render_group() -> None:
    @render_group(fit=False)
    def renderable():
        yield "one"
        yield "two"
        yield "three"  # <- largest width of 5
        yield "four"

    renderables = [renderable() for _ in range(4)]
    console = Console(width=42)
    min_width, _ = measure_renderables(console, renderables, 42)
    assert min_width == 42


def test_render_group_fit() -> None:
    @render_group()
    def renderable():
        yield "one"
        yield "two"
        yield "three"  # <- largest width of 5
        yield "four"

    renderables = [renderable() for _ in range(4)]

    console = Console(width=42)

    min_width, _ = measure_renderables(console, renderables, 42)
    assert min_width == 5
