import datetime
import io
import os
import sys
import tempfile
from typing import Optional, Tuple, Type, Union
from unittest import mock

import pytest

from rich import errors
from rich.color import ColorSystem
from rich.console import (
    CaptureError,
    Console,
    ConsoleDimensions,
    ConsoleOptions,
    ScreenUpdate,
    group,
)
from rich.control import Control
from rich.measure import measure_renderables
from rich.pager import SystemPager
from rich.panel import Panel
from rich.region import Region
from rich.segment import Segment
from rich.status import Status
from rich.style import Style
from rich.text import Text


def test_dumb_terminal():
    console = Console(force_terminal=True, _environ={})
    assert console.color_system is not None

    console = Console(force_terminal=True, _environ={"TERM": "dumb"})
    assert console.color_system is None
    width, height = console.size
    assert width == 80
    assert height == 25


def test_soft_wrap():
    console = Console(file=io.StringIO(), width=20, soft_wrap=True)
    console.print("foo " * 10)
    assert console.file.getvalue() == "foo " * 20


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
        ConsoleDimensions(80, 25),
        max_height=25,
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


def test_console_options_update_height():
    options = ConsoleOptions(
        ConsoleDimensions(80, 25),
        max_height=25,
        legacy_windows=False,
        min_width=10,
        max_width=20,
        is_terminal=False,
        encoding="utf-8",
    )
    assert options.height is None
    render_options = options.update_height(12)
    assert options.height is None
    assert render_options.height == 12
    assert render_options.max_height == 12


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

    console = Console(width=99, height=101, legacy_windows=False)
    w, h = console.size
    assert w == 99 and h == 101


@pytest.mark.parametrize(
    "is_windows,no_descriptor_size,stdin_size,stdout_size,stderr_size,expected_size",
    [
        # on Windows we'll use `os.get_terminal_size()` without arguments...
        (True, (133, 24), ValueError, ValueError, ValueError, (133, 24)),
        (False, (133, 24), ValueError, ValueError, ValueError, (80, 25)),
        # ...while on other OS we'll try to pass stdin, then stdout, then stderr to it:
        (False, ValueError, (133, 24), ValueError, ValueError, (133, 24)),
        (False, ValueError, ValueError, (133, 24), ValueError, (133, 24)),
        (False, ValueError, ValueError, ValueError, (133, 24), (133, 24)),
        (False, ValueError, ValueError, ValueError, ValueError, (80, 25)),
    ],
)
@mock.patch("rich.console.os.get_terminal_size")
def test_size_can_fall_back_to_std_descriptors(
    get_terminal_size_mock: mock.MagicMock,
    is_windows: bool,
    no_descriptor_size: Union[Tuple[int, int], Type[ValueError]],
    stdin_size: Union[Tuple[int, int], Type[ValueError]],
    stdout_size: Union[Tuple[int, int], Type[ValueError]],
    stderr_size: Union[Tuple[int, int], Type[ValueError]],
    expected_size,
):
    def get_terminal_size_mock_impl(fileno: int = None) -> Tuple[int, int]:
        value = {
            None: no_descriptor_size,
            sys.__stdin__.fileno(): stdin_size,
            sys.__stdout__.fileno(): stdout_size,
            sys.__stderr__.fileno(): stderr_size,
        }[fileno]
        if value is ValueError:
            raise value
        return value

    get_terminal_size_mock.side_effect = get_terminal_size_mock_impl

    console = Console(legacy_windows=False)
    with mock.patch("rich.console.WINDOWS", new=is_windows):
        w, h = console.size
    assert (w, h) == expected_size


def test_repr():
    console = Console()
    assert isinstance(repr(console), str)
    assert isinstance(str(console), str)


def test_print():
    console = Console(file=io.StringIO(), color_system="truecolor")
    console.print("foo")
    assert console.file.getvalue() == "foo\n"


def test_print_multiple():
    console = Console(file=io.StringIO(), color_system="truecolor")
    console.print("foo", "bar")
    assert console.file.getvalue() == "foo bar\n"


def test_print_text():
    console = Console(file=io.StringIO(), color_system="truecolor")
    console.print(Text("foo", style="bold"))
    assert console.file.getvalue() == "\x1B[1mfoo\x1B[0m\n"


def test_print_text_multiple():
    console = Console(file=io.StringIO(), color_system="truecolor")
    console.print(Text("foo", style="bold"), Text("bar"), "baz")
    assert console.file.getvalue() == "\x1B[1mfoo\x1B[0m bar baz\n"


def test_print_json():
    console = Console(file=io.StringIO(), color_system="truecolor")
    console.print_json('[false, true, null, "foo"]', indent=4)
    result = console.file.getvalue()
    print(repr(result))
    expected = '\x1b[1m[\x1b[0m\n    \x1b[3;91mfalse\x1b[0m,\n    \x1b[3;92mtrue\x1b[0m,\n    \x1b[3;35mnull\x1b[0m,\n    \x1b[32m"foo"\x1b[0m\n\x1b[1m]\x1b[0m\n'
    assert result == expected


def test_print_json_error():
    console = Console(file=io.StringIO(), color_system="truecolor")
    with pytest.raises(TypeError):
        console.print_json(["foo"], indent=4)


def test_print_json_data():
    console = Console(file=io.StringIO(), color_system="truecolor")
    console.print_json(data=[False, True, None, "foo"], indent=4)
    result = console.file.getvalue()
    print(repr(result))
    expected = '\x1b[1m[\x1b[0m\n    \x1b[3;91mfalse\x1b[0m,\n    \x1b[3;92mtrue\x1b[0m,\n    \x1b[3;35mnull\x1b[0m,\n    \x1b[32m"foo"\x1b[0m\n\x1b[1m]\x1b[0m\n'
    assert result == expected


def test_print_json_ensure_ascii():
    console = Console(file=io.StringIO(), color_system="truecolor")
    console.print_json(data={"foo": "💩"}, ensure_ascii=False)
    result = console.file.getvalue()
    print(repr(result))
    expected = '\x1b[1m{\x1b[0m\n  \x1b[1;34m"foo"\x1b[0m: \x1b[32m"💩"\x1b[0m\n\x1b[1m}\x1b[0m\n'
    assert result == expected


def test_print_json_indent_none():
    console = Console(file=io.StringIO(), color_system="truecolor")
    data = {"name": "apple", "count": 1}
    console.print_json(data=data, indent=None)
    result = console.file.getvalue()
    expected = '\x1b[1m{\x1b[0m\x1b[1;34m"name"\x1b[0m: \x1b[32m"apple"\x1b[0m, \x1b[1;34m"count"\x1b[0m: \x1b[1;36m1\x1b[0m\x1b[1m}\x1b[0m\n'
    assert result == expected


def test_log():
    console = Console(
        file=io.StringIO(),
        width=80,
        color_system="truecolor",
        log_time_format="TIME",
        log_path=False,
        _environ={},
    )
    console.log("foo", style="red")
    expected = "\x1b[2;36mTIME\x1b[0m\x1b[2;36m \x1b[0m\x1b[31mfoo                                                                        \x1b[0m\n"
    result = console.file.getvalue()
    print(repr(result))
    assert result == expected


def test_log_milliseconds():
    def time_formatter(timestamp: datetime) -> Text:
        return Text("TIME")

    console = Console(
        file=io.StringIO(), width=40, log_time_format=time_formatter, log_path=False
    )
    console.log("foo")
    result = console.file.getvalue()
    assert result == "TIME foo                                \n"


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
    console = Console(
        file=io.StringIO(), force_terminal=True, legacy_windows=False, _environ={}
    )
    console.show_cursor(False)
    console.print("foo")
    console.show_cursor(True)
    assert console.file.getvalue() == "\x1b[?25lfoo\n\x1b[?25h"


def test_clear():
    console = Console(file=io.StringIO(), force_terminal=True, _environ={})
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
    console = Console(file=io.StringIO(), force_terminal=True, _environ={})
    console.control(Control.clear())
    console.print("BAR")
    assert console.file.getvalue() == "\x1b[2JBAR\n"


def test_capture():
    console = Console()
    with console.capture() as capture:
        with pytest.raises(CaptureError):
            capture.get()
        console.print("Hello")
    assert capture.get() == "Hello\n"


def test_input(monkeypatch, capsys):
    def fake_input(prompt=""):
        console.file.write(prompt)
        return "bar"

    monkeypatch.setattr("builtins.input", fake_input)
    console = Console()
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


def test_status():
    console = Console(file=io.StringIO(), force_terminal=True, width=20)
    status = console.status("foo")
    assert isinstance(status, Status)


def test_justify_none():
    console = Console(file=io.StringIO(), force_terminal=True, width=20)
    console.print("FOO", justify=None)
    assert console.file.getvalue() == "FOO\n"


def test_justify_left():
    console = Console(file=io.StringIO(), force_terminal=True, width=20, _environ={})
    console.print("FOO", justify="left")
    assert console.file.getvalue() == "FOO                 \n"


def test_justify_center():
    console = Console(file=io.StringIO(), force_terminal=True, width=20, _environ={})
    console.print("FOO", justify="center")
    assert console.file.getvalue() == "        FOO         \n"


def test_justify_right():
    console = Console(file=io.StringIO(), force_terminal=True, width=20, _environ={})
    console.print("FOO", justify="right")
    assert console.file.getvalue() == "                 FOO\n"


def test_justify_renderable_none():
    console = Console(
        file=io.StringIO(),
        force_terminal=True,
        width=20,
        legacy_windows=False,
        _environ={},
    )
    console.print(Panel("FOO", expand=False, padding=0), justify=None)
    assert console.file.getvalue() == "╭───╮\n│FOO│\n╰───╯\n"


def test_justify_renderable_left():
    console = Console(
        file=io.StringIO(),
        force_terminal=True,
        width=10,
        legacy_windows=False,
        _environ={},
    )
    console.print(Panel("FOO", expand=False, padding=0), justify="left")
    assert console.file.getvalue() == "╭───╮     \n│FOO│     \n╰───╯     \n"


def test_justify_renderable_center():
    console = Console(
        file=io.StringIO(),
        force_terminal=True,
        width=10,
        legacy_windows=False,
        _environ={},
    )
    console.print(Panel("FOO", expand=False, padding=0), justify="center")
    assert console.file.getvalue() == "  ╭───╮   \n  │FOO│   \n  ╰───╯   \n"


def test_justify_renderable_right():
    console = Console(
        file=io.StringIO(),
        force_terminal=True,
        width=20,
        legacy_windows=False,
        _environ={},
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
    console.print("[b]foo <script> 'test' [link=https://example.org]Click[/link]")
    html = console.export_html()
    expected = '<!DOCTYPE html>\n<head>\n<meta charset="UTF-8">\n<style>\n.r1 {font-weight: bold}\n.r2 {color: #ff00ff; text-decoration-color: #ff00ff; font-weight: bold}\n.r3 {color: #008000; text-decoration-color: #008000; font-weight: bold}\nbody {\n    color: #000000;\n    background-color: #ffffff;\n}\n</style>\n</head>\n<html>\n<body>\n    <code>\n        <pre style="font-family:Menlo,\'DejaVu Sans Mono\',consolas,\'Courier New\',monospace"><span class="r1">foo &lt;</span><span class="r2">script</span><span class="r1">&gt; </span><span class="r3">&#x27;test&#x27;</span><span class="r1"> </span><a class="r1" href="https://example.org">Click</a>\n</pre>\n    </code>\n</body>\n</html>\n'
    assert html == expected


def test_export_html_inline():
    console = Console(record=True, width=100)
    console.print("[b]foo [link=https://example.org]Click[/link]")
    html = console.export_html(inline_styles=True)
    expected = '<!DOCTYPE html>\n<head>\n<meta charset="UTF-8">\n<style>\n\nbody {\n    color: #000000;\n    background-color: #ffffff;\n}\n</style>\n</head>\n<html>\n<body>\n    <code>\n        <pre style="font-family:Menlo,\'DejaVu Sans Mono\',consolas,\'Courier New\',monospace"><span style="font-weight: bold">foo </span><span style="font-weight: bold"><a href="https://example.org">Click</a></span>\n</pre>\n    </code>\n</body>\n</html>\n'
    assert html == expected


EXPECTED_SVG = """\
<svg width="1484.0" height="384" viewBox="0 0 1484.0 384"
     xmlns="http://www.w3.org/2000/svg">
    <style>
        @font-face {
            font-family: "Rich Fira Code";
            src: local("FiraCode-Regular"),
                 url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff2/FiraCode-Regular.woff2") format("woff2"),
                 url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff/FiraCode-Regular.woff") format("woff");
            font-style: normal;
            font-weight: 400;
        }
        @font-face {
            font-family: "Rich Fira Code";
            src: local("FiraCode-Bold"),
                 url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff2/FiraCode-Bold.woff2") format("woff2"),
                 url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff/FiraCode-Bold.woff") format("woff");
            font-style: bold;
            font-weight: 700;
        }
        .rich-svg-${SVG_HASH}-terminal-wrapper span {
            display: inline-block;
            white-space: pre;
            vertical-align: top;
            font-size: 18px;
            font-family:'Rich Fira Code','Cascadia Code',Monaco,Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace;
        }
        .rich-svg-${SVG_HASH}-terminal-wrapper a {
            text-decoration: none;
            color: inherit;
        }
        .rich-svg-${SVG_HASH}-terminal-body .blink {
           animation: rich-svg-${SVG_HASH}-blinker 1s infinite;
        }
        @keyframes rich-svg-${SVG_HASH}-blinker {
            from { opacity: 1.0; }
            50% { opacity: 0.3; }
            to { opacity: 1.0; }
        }
        .rich-svg-${SVG_HASH}-terminal-wrapper {
            padding: 140px;
            padding-top: 100px;
        }
        .rich-svg-${SVG_HASH}-terminal {
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #0c0c0c;
            border-radius: 14px;
            box-shadow: 0 0 0 1px #484848;
        }
        .rich-svg-${SVG_HASH}-terminal:after {
            position: absolute;
            width: 100%;
            height: 100%;
            content: '';
            border-radius: 14px;
            background: rgb(71,77,102);
            background: linear-gradient(90deg, #804D69 0%, #4E4B89 100%);
            transform: rotate(-4.5deg);
            z-index: -1;
        }
        .rich-svg-${SVG_HASH}-terminal-header {
            position: relative;
            width: 100%;
            background-color: #2e2e2e;
            margin-bottom: 12px;
            font-weight: bold;
            border-radius: 14px 14px 0 0;
            color: #f2f2f2;
            font-size: 18px;
            box-shadow: inset 0px -1px 0px 0px #4e4e4e,
                        inset 0px -4px 8px 0px #1a1a1a;
        }
        .rich-svg-${SVG_HASH}-terminal-title-tab {
            display: inline-block;
            margin-top: 14px;
            margin-left: 124px;
            font-family: sans-serif;
            padding: 14px 28px;
            border-radius: 6px 6px 0 0;
            background-color: #0c0c0c;
            box-shadow: inset 0px 1px 0px 0px #4e4e4e,
                        0px -4px 4px 0px #1e1e1e,
                        inset 1px 0px 0px 0px #4e4e4e,
                        inset -1px 0px 0px 0px #4e4e4e;
        }
        .rich-svg-${SVG_HASH}-terminal-traffic-lights {
            position: absolute;
            top: 24px;
            left: 20px;
        }
        .rich-svg-${SVG_HASH}-terminal-body {
            line-height: 22px;
            padding: 14px;
        }
        .rich-svg-${SVG_HASH}-terminal-body .r1 {color: #f2f2f2; text-decoration-color: #f2f2f2;background-color: #0c0c0c;}
.rich-svg-${SVG_HASH}-terminal-body .r2 {color: #2472c8; text-decoration-color: #2472c8; background-color: #cd3131; font-weight: bold}
.rich-svg-${SVG_HASH}-terminal-body .r3 {;color: #f2f2f2; text-decoration-color: #f2f2f2;;background-color: #0c0c0c;}
    </style>
    <foreignObject x="0" y="0" width="100%" height="100%">
        <body xmlns="http://www.w3.org/1999/xhtml">
            <div class="rich-svg-${SVG_HASH}-terminal-wrapper">
                <div class="rich-svg-${SVG_HASH}-terminal">
                    <div class="rich-svg-${SVG_HASH}-terminal-header">
                        <svg class="rich-svg-${SVG_HASH}-terminal-traffic-lights" width="90" height="21" viewBox="0 0 90 21" xmlns="http://www.w3.org/2000/svg">
                            <circle cx="14" cy="8" r="8" fill="#ff6159"/>
                            <circle cx="38" cy="8" r="8" fill="#ffbd2e"/>
                            <circle cx="62" cy="8" r="8" fill="#28c941"/>
                        </svg>
                        <div class="rich-svg-${SVG_HASH}-terminal-title-tab">Rich</div>
                    </div>
                    <div class="rich-svg-${SVG_HASH}-terminal-body">
                        <div><span class="r2">foo</span><span class="r1"> </span><span class="r3"><span class="blink"><a href="https://example.org">Click</a></span></span><span class="r1">                                                                                           </span></div>
<div><span class="r1"></span><span class="r1">                                                                                                    </span></div>
                    </div>
                </div>
            </div>
        </body>
    </foreignObject>
</svg>
"""


def test_export_svg():
    console = Console(record=True, width=100)
    console.print(
        "[b red on blue reverse]foo[/] [blink][link=https://example.org]Click[/link]"
    )
    svg = console.export_svg()
    svg_main_code_hash = (
        "857433718"  # hard-coded here after the 1st time we ran this test
    )
    expected_svg = EXPECTED_SVG.replace("${SVG_HASH}", svg_main_code_hash)
    assert svg == expected_svg


def test_save_svg():
    console = Console(record=True, width=100)
    console.print(
        "[b red on blue reverse]foo[/] [blink][link=https://example.org]Click[/link]"
    )
    svg_main_code_hash = "857433718"
    expected_svg = EXPECTED_SVG.replace("${SVG_HASH}", svg_main_code_hash)
    with tempfile.TemporaryDirectory() as path:
        export_path = os.path.join(path, "example.svg")
        console.save_svg(export_path)
        with open(export_path, "rt") as svg_file:
            assert svg_file.read() == expected_svg


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
    console = Console(force_terminal=True, _environ={})
    console.begin_capture()
    console.bell()
    assert console.end_capture() == "\x07"


def test_pager() -> None:
    console = Console(_environ={})

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
    @group(fit=False)
    def renderable():
        yield "one"
        yield "two"
        yield "three"  # <- largest width of 5
        yield "four"

    renderables = [renderable() for _ in range(4)]
    console = Console(width=42)
    min_width, _ = measure_renderables(console, console.options, renderables)
    assert min_width == 42


def test_render_group_fit() -> None:
    @group()
    def renderable():
        yield "one"
        yield "two"
        yield "three"  # <- largest width of 5
        yield "four"

    renderables = [renderable() for _ in range(4)]

    console = Console(width=42)

    min_width, _ = measure_renderables(console, console.options, renderables)
    assert min_width == 5


def test_get_time() -> None:
    console = Console(
        get_time=lambda: 99, get_datetime=lambda: datetime.datetime(1974, 7, 5)
    )
    assert console.get_time() == 99
    assert console.get_datetime() == datetime.datetime(1974, 7, 5)


def test_console_style() -> None:
    console = Console(
        file=io.StringIO(), color_system="truecolor", force_terminal=True, style="red"
    )
    console.print("foo")
    expected = "\x1b[31mfoo\x1b[0m\n"
    result = console.file.getvalue()
    assert result == expected


def test_no_color():
    console = Console(
        file=io.StringIO(), color_system="truecolor", force_terminal=True, no_color=True
    )
    console.print("[bold magenta on red]FOO")
    expected = "\x1b[1mFOO\x1b[0m\n"
    result = console.file.getvalue()
    print(repr(result))
    assert result == expected


def test_quiet():
    console = Console(file=io.StringIO(), quiet=True)
    console.print("Hello, World!")
    assert console.file.getvalue() == ""


def test_no_nested_live():
    console = Console()
    with pytest.raises(errors.LiveError):
        with console.status("foo"):
            with console.status("bar"):
                pass


@pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")
def test_screen():
    console = Console(
        color_system=None, force_terminal=True, force_interactive=True, _environ={}
    )
    with console.capture() as capture:
        with console.screen():
            console.print("Don't panic")
    expected = "\x1b[?1049h\x1b[H\x1b[?25lDon't panic\n\x1b[?1049l\x1b[?25h"
    result = capture.get()
    print(repr(result))
    assert result == expected


@pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")
def test_screen_update():
    console = Console(
        width=20, height=4, color_system="truecolor", force_terminal=True, _environ={}
    )
    with console.capture() as capture:
        with console.screen() as screen:
            screen.update("foo", style="blue")
            screen.update("bar")
            screen.update()
    result = capture.get()
    print(repr(result))
    expected = "\x1b[?1049h\x1b[H\x1b[?25l\x1b[34mfoo\x1b[0m\x1b[34m                 \x1b[0m\n\x1b[34m                    \x1b[0m\n\x1b[34m                    \x1b[0m\n\x1b[34m                    \x1b[0m\x1b[34mbar\x1b[0m\x1b[34m                 \x1b[0m\n\x1b[34m                    \x1b[0m\n\x1b[34m                    \x1b[0m\n\x1b[34m                    \x1b[0m\x1b[34mbar\x1b[0m\x1b[34m                 \x1b[0m\n\x1b[34m                    \x1b[0m\n\x1b[34m                    \x1b[0m\n\x1b[34m                    \x1b[0m\x1b[?1049l\x1b[?25h"
    assert result == expected


def test_height():
    console = Console(width=80, height=46)
    assert console.height == 46


def test_columns_env():
    console = Console(_environ={"COLUMNS": "314"}, legacy_windows=False)
    assert console.width == 314
    # width take precedence
    console = Console(width=40, _environ={"COLUMNS": "314"}, legacy_windows=False)
    assert console.width == 40
    # Should not fail
    console = Console(width=40, _environ={"COLUMNS": "broken"}, legacy_windows=False)


def test_lines_env():
    console = Console(_environ={"LINES": "220"})
    assert console.height == 220
    # height take precedence
    console = Console(height=40, _environ={"LINES": "220"})
    assert console.height == 40
    # Should not fail
    console = Console(width=40, _environ={"LINES": "broken"})


def test_screen_update_class():
    screen_update = ScreenUpdate([[Segment("foo")], [Segment("bar")]], 5, 10)
    assert screen_update.x == 5
    assert screen_update.y == 10

    console = Console(force_terminal=True)
    console.begin_capture()
    console.print(screen_update)
    result = console.end_capture()
    print(repr(result))
    expected = "\x1b[11;6Hfoo\x1b[12;6Hbar"
    assert result == expected


def test_is_alt_screen():
    console = Console(force_terminal=True)
    if console.legacy_windows:
        return
    assert not console.is_alt_screen
    with console.screen():
        assert console.is_alt_screen
    assert not console.is_alt_screen


def test_set_console_title():
    console = Console(force_terminal=True, _environ={})
    if console.legacy_windows:
        return

    with console.capture() as captured:
        console.set_window_title("hello")

    result = captured.get()
    assert result == "\x1b]0;hello\x07"


def test_update_screen():
    console = Console(force_terminal=True, width=20, height=5, _environ={})
    if console.legacy_windows:
        return
    with pytest.raises(errors.NoAltScreen):
        console.update_screen("foo")
    console.begin_capture()
    with console.screen():
        console.update_screen("foo")
        console.update_screen("bar", region=Region(2, 3, 8, 4))
    result = console.end_capture()
    print(repr(result))
    expected = "\x1b[?1049h\x1b[H\x1b[?25l\x1b[1;1Hfoo                 \x1b[2;1H                    \x1b[3;1H                    \x1b[4;1H                    \x1b[5;1H                    \x1b[4;3Hbar     \x1b[5;3H        \x1b[6;3H        \x1b[7;3H        \x1b[?1049l\x1b[?25h"
    assert result == expected


def test_update_screen_lines():
    console = Console(force_terminal=True, width=20, height=5)
    if console.legacy_windows:
        return
    with pytest.raises(errors.NoAltScreen):
        console.update_screen_lines([])


def test_update_options_markup():
    console = Console()
    options = console.options
    assert options.update(markup=False).markup == False
    assert options.update(markup=True).markup == True


def test_print_width_zero():
    console = Console()
    with console.capture() as capture:
        console.print("Hello", width=0)
    assert capture.get() == ""


def test_size_properties():
    console = Console(width=80, height=25, legacy_windows=False)
    assert console.size == ConsoleDimensions(80, 25)
    console.size = (10, 20)
    assert console.size == ConsoleDimensions(10, 20)
    console.width = 5
    assert console.size == ConsoleDimensions(5, 20)
    console.height = 10
    assert console.size == ConsoleDimensions(5, 10)


def test_print_newline_start():
    console = Console(width=80, height=25)
    console.begin_capture()
    console.print("Foo", new_line_start=True)
    console.print("Foo\nbar\n", new_line_start=True)
    result = console.end_capture()

    assert result == "Foo\n\nFoo\nbar\n\n"


def test_is_terminal_broken_file():
    console = Console()

    def _mock_isatty():
        raise ValueError()

    console.file.isatty = _mock_isatty

    assert console.is_terminal == False


@pytest.mark.skipif(sys.platform == "win32", reason="not relevant on Windows")
def test_detect_color_system():
    console = Console(_environ={"TERM": "rxvt-unicode-256color"}, force_terminal=True)
    assert console._detect_color_system() == ColorSystem.EIGHT_BIT


def test_reset_height():
    """Test height is reset when rendering complex renderables."""
    # https://github.com/Textualize/rich/issues/2042
    class Panels:
        def __rich_console__(self, console, options):
            yield Panel("foo")
            yield Panel("bar")

    console = Console(
        force_terminal=True,
        color_system="truecolor",
        width=20,
        height=40,
        legacy_windows=False,
    )

    with console.capture() as capture:
        console.print(Panel(Panels()), height=12)
    result = capture.get()
    print(repr(result))
    expected = "╭──────────────────╮\n│ ╭──────────────╮ │\n│ │ foo          │ │\n│ ╰──────────────╯ │\n│ ╭──────────────╮ │\n│ │ bar          │ │\n│ ╰──────────────╯ │\n│                  │\n│                  │\n│                  │\n│                  │\n╰──────────────────╯\n"

    assert result == expected
