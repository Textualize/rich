import pytest

from rich.markup import escape, MarkupError, _parse, render
from rich.text import Span


def test_escape():
    assert escape("foo[bar]") == "foo[[bar]]"


def test_parse():
    result = list(_parse("[foo]hello[/foo][bar]world[/][[escaped]]"))
    expected = [
        (None, "[foo]"),
        ("hello", None),
        (None, "[/foo]"),
        (None, "[bar]"),
        ("world", None),
        (None, "[/]"),
        ("[", None),
        ("escaped", None),
        ("]", None),
    ]
    assert result == expected


def test_render():
    result = render("[bold]FOO[/bold]")
    assert str(result) == "FOO"
    assert result.spans == [Span(0, 3, "bold")]


def test_render_combine():
    result = render("[green]X[blue]Y[/blue]Z[/green]")
    assert str(result) == "XYZ"
    assert result.spans == [
        Span(0, 3, "green"),
        Span(1, 2, "blue"),
    ]


def test_render_overlap():
    result = render("[green]X[bold]Y[/green]Z[/bold]")
    assert str(result) == "XYZ"
    assert result.spans == [
        Span(0, 2, "green"),
        Span(1, 3, "bold"),
    ]


def test_render_close():
    result = render("[bold]X[/]Y")
    assert str(result) == "XY"
    assert result.spans == [Span(0, 1, "bold")]


def test_render_close_ambiguous():
    result = render("[green]X[bold]Y[/]Z[/]")
    assert str(result) == "XYZ"
    assert result.spans == [Span(0, 3, "green"), Span(1, 2, "bold")]


def test_markup_error():
    with pytest.raises(MarkupError):
        assert render("foo[/]")
    with pytest.raises(MarkupError):
        assert render("foo[/bar]")
    with pytest.raises(MarkupError):
        assert render("[foo]hello[/bar]")
