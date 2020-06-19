import pytest

from rich.box import ASCII, DOUBLE, ROUNDED, HEAVY


def test_str():
    assert str(ASCII) == "+--+\n| ||\n|-+|\n| ||\n|-+|\n|-+|\n| ||\n+--+\n"


def test_repr():
    assert repr(ASCII) == "Box(...)"


def test_get_top():
    top = HEAVY.get_top(widths=[1, 2])
    assert top == "┏━┳━━┓"


def test_get_row():
    head_row = DOUBLE.get_row(widths=[3, 2, 1], level="head")
    assert head_row == "╠═══╬══╬═╣"

    row = ASCII.get_row(widths=[1, 2, 3], level="row")
    assert row == "|-+--+---|"

    foot_row = ROUNDED.get_row(widths=[2, 1, 3], level="foot")
    assert foot_row == "├──┼─┼───┤"

    with pytest.raises(ValueError):
        ROUNDED.get_row(widths=[1, 2, 3], level="FOO")


def test_get_bottom():
    bottom = HEAVY.get_bottom(widths=[1, 2, 3])
    assert bottom == "┗━┻━━┻━━━┛"
