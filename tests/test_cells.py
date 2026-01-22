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
    ],
)
def test_split_graphemes(
    text: str, expected_spans: list[CellSpan], expected_cell_length: int
):
    spans, cell_length = split_graphemes(text)
    assert cell_len(text) == expected_cell_length
    assert spans == expected_spans
    assert cell_length == expected_cell_length
