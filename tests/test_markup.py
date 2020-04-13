import pytest

from rich.markup import MarkupError, _parse, render
from rich.text import Span


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


def test_markup_error():
    with pytest.raises(MarkupError):
        assert render("foo[/]")
    with pytest.raises(MarkupError):
        assert render("foo[/bar]")
    with pytest.raises(MarkupError):
        assert render("[foo]hello[/bar]")
