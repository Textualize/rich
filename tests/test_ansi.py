import io

from rich.ansi import AnsiDecoder
from rich.console import Console
from rich.style import Style
from rich.text import Span, Text


def test_decode():
    console = Console(force_terminal=True, color_system="truecolor")
    console.begin_capture()
    console.print("Hello")
    console.print("[b]foo[/b]")
    console.print("[link http://example.org]bar")
    console.print("[#ff0000 on color(200)]red")
    terminal_codes = console.end_capture()

    decoder = AnsiDecoder()
    lines = list(decoder.decode(terminal_codes))

    parse = Style.parse
    expected = [
        Text("Hello"),
        Text("foo", spans=[Span(0, 3, parse("bold"))]),
        Text("bar", spans=[Span(0, 3, parse("link http://example.org"))]),
        Text("red", spans=[Span(0, 3, parse("#ff0000 on color(200)"))]),
    ]

    assert lines == expected