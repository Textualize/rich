import pytest

from rich.box import ASCII, DOUBLE, HEAVY, ROUNDED, SQUARE
from rich.console import ConsoleDimensions, ConsoleOptions


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


def test_box_substitute():
    options = ConsoleOptions(
        ConsoleDimensions(80, 25),
        legacy_windows=True,
        min_width=1,
        max_width=100,
        is_terminal=True,
        encoding="utf-8",
        max_height=25,
    )
    assert HEAVY.substitute(options) == SQUARE

    options.legacy_windows = False
    assert HEAVY.substitute(options) == HEAVY

    options.encoding = "ascii"
    assert HEAVY.substitute(options) == ASCII
