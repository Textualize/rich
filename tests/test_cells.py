from rich import cells
from rich.cells import fold_to_width


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


def test_fold_to_width():
    """Simple example of splitting cells into lines of width 3."""
    text = "abcdefghijk"
    assert fold_to_width(text, 3) == ["abc", "def", "ghi", "jk"]


def test_fold_to_width_double_width_boundary():
    """The available width lies within a double-width character."""
    text = "ありがとう"
    assert fold_to_width(text, 3) == ["あ", "り", "が", "と", "う"]


def test_fold_to_width_mixed_width():
    """Mixed single and double-width characters."""
    text = "あ1り2が3と4う56"
    assert fold_to_width(text, 3) == ["あ1", "り2", "が3", "と4", "う5", "6"]
