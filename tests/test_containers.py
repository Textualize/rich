from rich.console import Console
from rich.containers import Lines, Renderables
from rich.style import Style
from rich.text import Span, Text


def test_renderables_measure():
    console = Console()
    text = Text("foo")
    renderables = Renderables([text])

    result = renderables.__rich_measure__(console, console.options)
    _min, _max = result
    assert _min == 3
    assert _max == 3

    assert list(renderables) == [text]


def test_renderables_empty():
    console = Console()
    renderables = Renderables()

    result = renderables.__rich_measure__(console, console.options)
    _min, _max = result
    assert _min == 1
    assert _max == 1


def test_lines_rich_console():
    console = Console()
    lines = Lines([Text("foo")])

    result = list(lines.__rich_console__(console, console.options))
    assert result == [Text("foo")]


def test_lines_justify():
    console = Console()
    lines1 = Lines([Text("foo", style="b"), Text("test", style="b")])
    lines1.justify(console, 10, justify="left")
    assert lines1._lines == [Text("foo       "), Text("test      ")]
    lines1.justify(console, 10, justify="center")
    assert lines1._lines == [Text("   foo    "), Text("   test   ")]
    lines1.justify(console, 10, justify="right")
    assert lines1._lines == [Text("       foo"), Text("      test")]

    lines2 = Lines([Text("foo bar", style="b"), Text("test", style="b")])
    lines2.justify(console, 7, justify="full")
    print(repr(lines2._lines[0].spans))
    assert lines2._lines == [
        Text(
            "foo bar",
            spans=[Span(0, 3, "b"), Span(3, 4, Style.parse("bold")), Span(4, 7, "b")],
        ),
        Text("test"),
    ]
