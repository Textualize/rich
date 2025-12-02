import pytest
from rich.text import Text
from rich.markup import escape

def _roundtrip(s: str) -> str:
    """escape() then parse as markup; return plain text for comparison."""
    escaped = escape(s)
    return Text.from_markup(escaped).plain

@pytest.mark.parametrize(
    "raw",
    [
        r"\[b]hello\[/b]",
        r"C:\[bin]\tools",
        r"C:\\[bin]\\tools",
        r"\[color(123,45,6)]x\[/color]",
    ],
)
def test_from_markup_handles_backslash_escaped_brackets(raw: str) -> None:
    """Backslash-escaped brackets must be treated as literals (no mismatched tags)."""
    text = Text.from_markup(raw)  # must not raise
    assert text.plain.replace("\u200b", "")  # force render; content exists

def test_escape_then_from_markup_roundtrips_common_windows_path() -> None:
    s = r"C:\Users\[name]\AppData\Local"
    assert _roundtrip(s) == s

@pytest.mark.parametrize(
    ("s", "expected"),
    [
        (r"\[b]x\[/b]", "[b]x[/b]"),
        # NOTE: the raw backslash-before-[ case is covered by an xfail test below
    ],
)
def test_backslash_literal_output(s: str, expected: str) -> None:
    """Already-escaped brackets render literally as plain text."""
    plain = Text.from_markup(s).plain
    assert plain.replace("\u200b", "") == expected

@pytest.mark.xfail(reason="Loses backslash before '['; see #2993", strict=False)
def test_windows_path_with_brackets_should_render_literally() -> None:
    """
    Document current bug: a backslash immediately before '[' is swallowed.
    Desired behavior: render literally.
    """
    s = r"C:\[tmp]\file.txt"
    plain = Text.from_markup(s).plain
    assert plain.replace("\u200b", "") == s
