from __future__ import annotations

import string

import pytest

from rich import cells
from rich.cells import (
    CellSpan,
    _is_single_cell_widths,
    cell_len,
    chop_cells,
    get_character_cell_size,
    set_cell_size,
    split_graphemes,
    split_text,
)


@pytest.mark.parametrize(
    "character,size",
    [
        ("\0", 0),
        ("\u200d", 0),
        ("a", 1),
        ("💩", 2),
        (chr(917999 + 1), 0),
    ],
)
def test_get_character_cell_size(character: str, size: int) -> None:
    """Test single character cell size."""
    assert get_character_cell_size(character) == size


def test_cell_len_long_string():
    # Long strings don't use cached cell length implementation
    assert cells.cell_len("abc" * 200) == 3 * 200
    # Boundary case
    assert cells.cell_len("a" * 512) == 512


def test_cell_len_short_string():
    # Short strings use cached cell length implementation
    assert cells.cell_len("abc" * 100) == 3 * 100
    # Boundary case
    assert cells.cell_len("a" * 511) == 511


def test_set_cell_size():
    assert cells.set_cell_size("foo", 0) == ""
    assert cells.set_cell_size("f", 0) == ""
    assert cells.set_cell_size("", 0) == ""
    assert cells.set_cell_size("😽😽", 0) == ""
    assert cells.set_cell_size("foo", 2) == "fo"
    assert cells.set_cell_size("foo", 3) == "foo"
    assert cells.set_cell_size("foo", 4) == "foo "
    assert cells.set_cell_size("😽😽", 4) == "😽😽"
    assert cells.set_cell_size("😽😽", 3) == "😽 "
    assert cells.set_cell_size("😽😽", 2) == "😽"
    assert cells.set_cell_size("😽😽", 1) == " "
    assert cells.set_cell_size("😽😽", 5) == "😽😽 "


def test_set_cell_size_infinite():
    for size in range(38):
        assert (
            cells.cell_len(
                cells.set_cell_size(
                    "เป็นเกมที่ต้องมีความอดทนมากที่สุดตั้งเเต่เคยเล่นมา", size
                )
            )
            == size
        )


FM = "👩\u200d🔧"


@pytest.mark.parametrize(
    "text,offset,left,right",
    [
        # Edge cases
        ("", -1, "", ""),
        ("x", -1, "", "x"),
        ("x", 1, "x", ""),
        ("x", 2, "x", ""),
        ("", 0, "", ""),
        ("", 1, "", ""),
        ("a", 0, "", "a"),
        ("a", 1, "a", ""),
        # Check simple double width character
        ("💩", 0, "", "💩"),
        ("💩", 1, " ", " "),  # Split in the middle of a double wide results in spaces
        ("💩", 2, "💩", ""),
        ("💩x", 1, " ", " x"),
        ("💩x", 2, "💩", "x"),
        ("💩x", 3, "💩x", ""),
        # Check same for multi-codepoint emoji
        (FM, 0, "", FM),
        (FM, 1, " ", " "),  # Split in the middle of a double wide results in spaces
        (FM, 2, FM, ""),
        (FM + "x", 1, " ", " x"),
        (FM + "x", 2, FM, "x"),
        (FM + "x", 3, FM + "x", ""),
        # Edge cases
        ("xxxxxxxxxxxxxxx💩💩", 10, "xxxxxxxxxx", "xxxxx💩💩"),
        ("xxxxxxxxxxxxxxx💩💩", 15, "xxxxxxxxxxxxxxx", "💩💩"),
        ("xxxxxxxxxxxxxxx💩💩", 16, "xxxxxxxxxxxxxxx ", " 💩"),
        ("💩💩", 3, "💩 ", " "),
        ("💩💩xxxxxxxxxx", 2, "💩", "💩xxxxxxxxxx"),
        ("💩💩xxxxxxxxxx", 3, "💩 ", " xxxxxxxxxx"),
        ("💩💩xxxxxxxxxx", 4, "💩💩", "xxxxxxxxxx"),
    ],
)
def test_split_text(text: str, offset: int, left: str, right: str) -> None:
    """Check that split_text works on grapheme boundaries"""
    assert split_text(text, offset) == (left, right)


def test_chop_cells():
    """Simple example of splitting cells into lines of width 3."""
    text = "abcdefghijk"
    assert chop_cells(text, 3) == ["abc", "def", "ghi", "jk"]


def test_chop_cells_double_width_boundary():
    """The available width lies within a double-width character."""
    text = "ありがとう"
    assert chop_cells(text, 3) == ["あ", "り", "が", "と", "う"]


def test_chop_cells_mixed_width():
    """Mixed single and double-width characters."""
    text = "あ1り234が5と6う78"
    assert chop_cells(text, 3) == ["あ1", "り2", "34", "が5", "と6", "う7", "8"]


@pytest.mark.parametrize(
    "text,expected",
    [
        ("", []),
        ("\x1b", []),
        ("\x1b\x1b", []),
        ("\x1b\x1b\x1b", []),
        ("\x1b\x1b\x1b\x1b", []),
    ],
)
def test_chop_cells_zero_width(text: str, expected: list[str]) -> None:
    """Test zer width characters being chopped."""
    assert chop_cells(text, 3) == expected


def test_is_single_cell_widths() -> None:
    # Check _is_single_cell_widths reports correctly
    for character in string.printable:
        if ord(character) >= 32:
            assert _is_single_cell_widths(character)

    BOX = "┌─┬┐│ ││├─┼┤│ ││├─┼┤├─┼┤│ ││└─┴┘"

    for character in BOX:
        assert _is_single_cell_widths(character)

    for character in "💩😽":
        assert not _is_single_cell_widths(character)

    for character in "わさび":
        assert not _is_single_cell_widths(character)


@pytest.mark.parametrize(
    "text,expected_spans,expected_cell_length",
    [
        ("", [], 0),
        ("a", [(0, 1, 1)], 1),
        ("ab", [(0, 1, 1), (1, 2, 1)], 2),
        ("💩", [(0, 1, 2)], 2),
        ("わさび", [(0, 1, 2), (1, 2, 2), (2, 3, 2)], 6),
        (
            "👩\u200d🔧",
            [(0, 3, 2)],
            2,
        ),  # 3 code points for female mechanic: female, joiner, spanner
        ("a👩\u200d🔧", [(0, 1, 1), (1, 4, 2)], 3),
        ("a👩\u200d🔧b", [(0, 1, 1), (1, 4, 2), (4, 5, 1)], 4),
        ("⬇", [(0, 1, 1)], 1),
        ("⬇️", [(0, 2, 2)], 2),  # Variation selector, makes it double width
        ("♻", [(0, 1, 1)], 1),
        ("♻️", [(0, 2, 2)], 2),
        ("♻♻️", [(0, 1, 1), (1, 3, 2)], 3),
        ("\x1b", [(0, 1, 0)], 0),  # One escape should have zero width
        ("\x1b\x1b", [(0, 2, 0)], 0),  # Two escapes should have zero width
        (
            "\ufe0f",
            [(0, 1, 0)],
            0,
        ),  # Variation selector 16, without anything to change should have zero width
        (
            "\ufe0f\ufe0f",
            [(0, 2, 0)],
            0,
        ),  # 2 X variation selector 16, without anything to change should have zero width
        (
            "\u200d",
            [(0, 1, 0)],
            0,
        ),  # A zero width joiner with nothing prior should have zero width
        (
            "\u200d\u200d",
            [(0, 2, 0)],
            0,
        ),  # Two ZWJs should have zero width
        (
            "\x1b\ufe0f",
            [(0, 2, 0)],
            0,
        ),  # VS16 after escape (zero-width, doesn't set last_measured_character) should have zero width
        (
            "\u200d\ufe0f",
            [(0, 2, 0)],
            0,
        ),  # VS16 after ZWJ (zero-width, doesn't set last_measured_character) should have zero width
    ],
)
def test_split_graphemes(
    text: str, expected_spans: list[CellSpan], expected_cell_length: int
):
    spans, cell_length = split_graphemes(text)
    print(spans)
    assert cell_len(text) == expected_cell_length
    assert spans == expected_spans
    assert cell_length == expected_cell_length


def test_nerd_font():
    """Regression test for https://github.com/Textualize/rich/issues/3943"""
    # Not allocated by unicode, but used by nerd fonts
    assert cell_len("\U000f024d") == 1


def test_zwj():
    """Test special case of zero width joiners"""
    assert cell_len("") == 0
    assert cell_len("\u200d") == 0
    assert cell_len("1\u200d") == 1
    # This sequence should really produce 2, but it aligns with with wcwidth
    # What gets written to the terminal is anybody's guess, I've seen multiple variations
    assert cell_len("1\u200d2") == 1


def test_non_printable():
    """Non printable characters should report a width of 0."""
    for ordinal in range(31):
        character = chr(ordinal)
        assert cell_len(character) == 0


def test_cell_len_edge_cases() -> None:
    """cell_len for empty strings, ZWJ sequences, and mixed CJK."""
    assert cell_len("") == 0
    assert cell_len("👩\u200d🔧") == 2
    assert cell_len("👩\u200d👩\u200d👧\u200d👧") == 2
    assert cell_len("あ1り2") == 6


def test_set_cell_size_edge_cases() -> None:
    """set_cell_size for empty strings and exact-boundary cases."""
    assert set_cell_size("", 0) == ""
    assert set_cell_size("", 3) == "   "
    assert set_cell_size("foo", 3) == "foo"
    assert set_cell_size("あい", 4) == "あい"
    assert set_cell_size("あ1り2", 6) == "あ1り2"
    assert set_cell_size("👩\u200d🔧", 2) == "👩\u200d🔧"
    assert set_cell_size("👩\u200d🔧", 1) == " "


def test_chop_cells_edge_cases() -> None:
    """chop_cells for empty strings, ZWJ sequences, and mixed CJK boundaries."""
    assert chop_cells("", 3) == []
    assert chop_cells("👩\u200d🔧", 2) == ["👩\u200d🔧"]
    assert chop_cells("👩\u200d🔧👩\u200d🔧", 2) == ["👩\u200d🔧", "👩\u200d🔧"]
    assert chop_cells("あ1り2", 3) == ["あ1", "り2"]
    assert chop_cells("あ1り2", 6) == ["あ1り2"]
