import pytest

from rich.console import ConsoleOptions, ConsoleDimensions
from rich.box import (
    ASCII,
    DOUBLE,
    ROUNDED,
    HEAVY,
    SQUARE,
    MINIMAL_HEAVY_HEAD,
    MINIMAL,
    SIMPLE_HEAVY,
    SIMPLE,
    HEAVY_EDGE,
    HEAVY_HEAD,
)


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


def test_box_substitute_for_same_box():
    options = ConsoleOptions(
        ConsoleDimensions(80, 25),
        legacy_windows=False,
        min_width=1,
        max_width=100,
        is_terminal=True,
        encoding="utf-8",
        max_height=25,
    )

    assert ROUNDED.substitute(options) == ROUNDED
    assert MINIMAL_HEAVY_HEAD.substitute(options) == MINIMAL_HEAVY_HEAD
    assert SIMPLE_HEAVY.substitute(options) == SIMPLE_HEAVY
    assert HEAVY.substitute(options) == HEAVY
    assert HEAVY_EDGE.substitute(options) == HEAVY_EDGE
    assert HEAVY_HEAD.substitute(options) == HEAVY_HEAD


def test_box_substitute_for_different_box_legacy_windows():
    options = ConsoleOptions(
        ConsoleDimensions(80, 25),
        legacy_windows=True,
        min_width=1,
        max_width=100,
        is_terminal=True,
        encoding="utf-8",
        max_height=25,
    )

    assert ROUNDED.substitute(options) == SQUARE
    assert MINIMAL_HEAVY_HEAD.substitute(options) == MINIMAL
    assert SIMPLE_HEAVY.substitute(options) == SIMPLE
    assert HEAVY.substitute(options) == SQUARE
    assert HEAVY_EDGE.substitute(options) == SQUARE
    assert HEAVY_HEAD.substitute(options) == SQUARE


def test_box_substitute_for_different_box_ascii_encoding():
    options = ConsoleOptions(
        ConsoleDimensions(80, 25),
        legacy_windows=True,
        min_width=1,
        max_width=100,
        is_terminal=True,
        encoding="ascii",
        max_height=25,
    )

    assert ROUNDED.substitute(options) == ASCII
    assert MINIMAL_HEAVY_HEAD.substitute(options) == ASCII
    assert SIMPLE_HEAVY.substitute(options) == ASCII
    assert HEAVY.substitute(options) == ASCII
    assert HEAVY_EDGE.substitute(options) == ASCII
    assert HEAVY_HEAD.substitute(options) == ASCII
