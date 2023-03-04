import pytest

from rich.ansi import AnsiDecoder
from rich.console import Console
from rich.style import Style
from rich.text import Span, Text


def test_decode():
    console = Console(
        force_terminal=True, legacy_windows=False, color_system="truecolor"
    )
    console.begin_capture()
    console.print("Hello")
    console.print("[b]foo[/b]")
    console.print("[link http://example.org]bar")
    console.print("[#ff0000 on color(200)]red")
    console.print("[color(200) on #ff0000]red")
    terminal_codes = console.end_capture()

    decoder = AnsiDecoder()
    lines = list(decoder.decode(terminal_codes))

    expected = [
        Text("Hello"),
        Text("foo", spans=[Span(0, 3, Style.parse("bold"))]),
        Text("bar", spans=[Span(0, 3, Style.parse("link http://example.org"))]),
        Text("red", spans=[Span(0, 3, Style.parse("#ff0000 on color(200)"))]),
        Text("red", spans=[Span(0, 3, Style.parse("color(200) on #ff0000"))]),
    ]

    assert lines == expected


def test_decode_example():
    ansi_bytes = b"\x1b[01m\x1b[KC:\\Users\\stefa\\AppData\\Local\\Temp\\tmp3ydingba:\x1b[m\x1b[K In function '\x1b[01m\x1b[Kmain\x1b[m\x1b[K':\n\x1b[01m\x1b[KC:\\Users\\stefa\\AppData\\Local\\Temp\\tmp3ydingba:3:5:\x1b[m\x1b[K \x1b[01;35m\x1b[Kwarning: \x1b[m\x1b[Kunused variable '\x1b[01m\x1b[Ka\x1b[m\x1b[K' [\x1b[01;35m\x1b[K-Wunused-variable\x1b[m\x1b[K]\n    3 | int \x1b[01;35m\x1b[Ka\x1b[m\x1b[K=1;\n      |     \x1b[01;35m\x1b[K^\x1b[m\x1b[K\n"
    ansi_text = ansi_bytes.decode("utf-8")

    text = Text.from_ansi(ansi_text)

    console = Console(
        force_terminal=True, legacy_windows=False, color_system="truecolor"
    )
    with console.capture() as capture:
        console.print(text)
    result = capture.get()
    print(repr(result))
    expected = "\x1b[1mC:\\Users\\stefa\\AppData\\Local\\Temp\\tmp3ydingba:\x1b[0m In function '\x1b[1mmain\x1b[0m':\n\x1b[1mC:\\Users\\stefa\\AppData\\Local\\Temp\\tmp3ydingba:3:5:\x1b[0m \x1b[1;35mwarning: \x1b[0munused variable '\x1b[1ma\x1b[0m' \n[\x1b[1;35m-Wunused-variable\x1b[0m]\n    3 | int \x1b[1;35ma\x1b[0m=1;\n      |     \x1b[1;35m^\x1b[0m\n"
    assert result == expected


@pytest.mark.parametrize(
    "ansi_bytes, expected_text",
    [
        # https://github.com/Textualize/rich/issues/2688
        (
            b"\x1b[31mFound 4 errors in 2 files (checked 18 source files)\x1b(B\x1b[m\n",
            "Found 4 errors in 2 files (checked 18 source files)",
        ),
        # https://mail.python.org/pipermail/python-list/2007-December/424756.html
        (b"Hallo", "Hallo"),
        (b"\x1b(BHallo", "Hallo"),
        (b"\x1b(JHallo", "Hallo"),
        (b"\x1b(BHal\x1b(Jlo", "Hallo"),
    ],
)
def test_decode_issue_2688(ansi_bytes, expected_text):
    text = Text.from_ansi(ansi_bytes.decode())

    assert str(text) == expected_text
