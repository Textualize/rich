import pytest

from rich.markup_validator import MarkupValidator
from rich.errors import MarkupError


def test_simple_valid():
    v = MarkupValidator()
    assert v.validate("[b]bold[/b]")


def test_nested_valid():
    v = MarkupValidator()
    assert v.validate("[b][i]inner[/i][/b]")


def test_mismatch_tags():
    v = MarkupValidator()
    with pytest.raises(MarkupError) as exc:
        v.validate("[b]bad[/i]")
    assert "mismatched" in str(exc.value) or "expected" in str(exc.value)


def test_unclosed_tag():
    v = MarkupValidator()
    with pytest.raises(MarkupError) as exc:
        v.validate("[b]open")
    assert "unclosed" in str(exc.value)


def test_extra_closing():
    v = MarkupValidator()
    with pytest.raises(MarkupError):
        v.validate("text[/b]")


def test_with_attributes():
    v = MarkupValidator()
    assert v.validate("[link=https://example.com]click[/link]")


def test_empty_brackets_are_invalid():
    v = MarkupValidator()
    with pytest.raises(MarkupError):
        v.validate("[]")


def test_space_in_opening_tag_uses_first_token():
    v = MarkupValidator()
    # '[bold red]' should push 'bold' and be closed by '[/bold]'
    assert v.validate("[bold red]text[/bold]")


def test_nameless_closing_pops_top():
    v = MarkupValidator()
    # nameless closing pops the most recent tag ('b'), leaving 'a' unclosed
    with pytest.raises(MarkupError) as exc:
        v.validate("[a][b]x[/]")
    assert "unclosed" in str(exc.value)


def test_nameless_closing_then_close_parent():
    v = MarkupValidator()
    # nameless close pops 'b', then closing [/a] closes 'a'
    assert v.validate("[a][b]x[/][/a]")


def test_nameless_closing_with_empty_stack_is_invalid():
    v = MarkupValidator()
    with pytest.raises(MarkupError):
        v.validate("text[/]")


def test_escaped_brackets():
    v = MarkupValidator()
    # the '[' is escaped, so it should not be treated as a tag start
    assert v.validate(r"This is \[bold] text")

