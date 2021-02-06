import pytest

from rich.console import Console
from rich.markup import escape, MarkupError, _parse, render, Tag, RE_TAGS
from rich.text import Span


def test_re_no_match():
    assert RE_TAGS.match("[True]") == None
    assert RE_TAGS.match("[False]") == None
    assert RE_TAGS.match("[None]") == None
    assert RE_TAGS.match("[1]") == None
    assert RE_TAGS.match("[2]") == None
    assert RE_TAGS.match("[]") == None


def test_re_match():
    assert RE_TAGS.match("[true]")
    assert RE_TAGS.match("[false]")
    assert RE_TAGS.match("[none]")
    assert RE_TAGS.match("[color(1)]")
    assert RE_TAGS.match("[#ff00ff]")
    assert RE_TAGS.match("[/]")


def test_escape():
    # Potential tags
    assert escape("foo[bar]") == r"foo\[bar]"
    assert escape(r"foo\[bar]") == r"foo\\\[bar]"

    # Not tags (escape not required)
    assert escape("[5]") == "[5]"
    assert escape("\\[5]") == "\\[5]"


def test_render_escape():
    console = Console(width=80, color_system=None)
    console.begin_capture()
    console.print(
        escape(r"[red]"), escape(r"\[red]"), escape(r"\\[red]"), escape(r"\\\[red]")
    )
    result = console.end_capture()
    expected = r"[red] \[red] \\[red] \\\[red]" + "\n"
    assert result == expected


def test_parse():
    result = list(_parse(r"[foo]hello[/foo][bar]world[/]\[escaped]"))
    expected = [
        (0, None, Tag(name="foo", parameters=None)),
        (10, "hello", None),
        (10, None, Tag(name="/foo", parameters=None)),
        (16, None, Tag(name="bar", parameters=None)),
        (26, "world", None),
        (26, None, Tag(name="/", parameters=None)),
        (29, "[escaped]", None),
    ]
    print(repr(result))
    assert result == expected


def test_parse_link():
    result = list(_parse("[link=foo]bar[/link]"))
    expected = [
        (0, None, Tag(name="link", parameters="foo")),
        (13, "bar", None),
        (13, None, Tag(name="/link", parameters=None)),
    ]
    assert result == expected


def test_render():
    result = render("[bold]FOO[/bold]")
    assert str(result) == "FOO"
    assert result.spans == [Span(0, 3, "bold")]


def test_render_not_tags():
    result = render('[[1], [1,2,3,4], ["hello"], [None], [False], [True]] []')
    assert str(result) == '[[1], [1,2,3,4], ["hello"], [None], [False], [True]] []'
    assert result.spans == []


def test_render_link():
    result = render("[link=foo]FOO[/link]")
    assert str(result) == "FOO"
    assert result.spans == [Span(0, 3, "link foo")]


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


def test_escape_escape():
    # Escaped escapes (i.e. double backslash)should be treated as literal
    result = render(r"\\[bold]FOO")
    assert str(result) == r"\FOO"

    # Single backslash makes the tag literal
    result = render(r"\[bold]FOO")
    assert str(result) == "[bold]FOO"

    # Double backslash produces a backslash
    result = render(r"\\[bold]some text[/]")
    assert str(result) == r"\some text"

    # Triple backslash parsed as literal backslash plus escaped tag
    result = render(r"\\\[bold]some text\[/]")
    assert str(result) == r"\[bold]some text[/]"

    # Backslash escaping only happens when preceding a tag
    result = render(r"\\")
    assert str(result) == r"\\"

    result = render(r"\\\\")
    assert str(result) == r"\\\\"
