from rich.console import Console
from rich.containers import Lines, Renderables
from rich.text import Text


def test_renderables_measure():
    console = Console()
    text = Text("foo")
    renderables = Renderables([text])

    result = renderables.__rich_measure__(console, console.width)
    _min, _max = result
    assert _min == 3
    assert _max == 3

    assert list(renderables) == [text]


def test_renderables_empty():
    console = Console()
    renderables = Renderables()

    result = renderables.__rich_measure__(console, console.width)
    _min, _max = result
    assert _min == 1
    assert _max == 1


def test_lines_rich_console():
    console = Console()
    lines = Lines([Text("foo")])

    result = list(lines.__rich_console__(console, console.options))
    assert result == [Text("foo")]

