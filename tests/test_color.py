from rich.color import (
    blend_rgb,
    parse_rgb_hex,
    Color,
    ColorParseError,
    ColorSystem,
    ColorType,
    ColorTriplet,
)

from rich import themes

import pytest


def test_str() -> None:
    print(repr(str(Color.parse("red"))))
    assert str(Color.parse("red")) == "\x1b[31m⬤  \x1b[0m<color 'red' (standard)>"


def test_repr() -> None:
    assert repr(Color.parse("red")) == "<color 'red' (standard)>"


def test_system() -> None:
    assert Color.parse("red").system == ColorSystem.STANDARD
    assert Color.parse("#ff0000").system == ColorSystem.TRUECOLOR


def test_truecolor() -> None:
    assert Color.parse("#ff0000").get_truecolor(themes.DEFAULT) == ColorTriplet(
        255, 0, 0
    )
    assert Color.parse("red").get_truecolor(themes.DEFAULT) == ColorTriplet(128, 0, 0)
    assert Color.parse("1").get_truecolor(themes.DEFAULT) == ColorTriplet(128, 0, 0)
    assert Color.parse("17").get_truecolor(themes.DEFAULT) == ColorTriplet(0, 0, 95)
    assert Color.parse("default").get_truecolor(themes.DEFAULT) == ColorTriplet(0, 0, 0)
    assert Color.parse("default").get_truecolor(
        themes.DEFAULT, foreground=False
    ) == ColorTriplet(255, 255, 255)


def test_parse_success() -> None:
    assert Color.parse("default") == Color("default", ColorType.DEFAULT, None, None)
    assert Color.parse("red") == Color("red", ColorType.STANDARD, 1, None)
    assert Color.parse("red+") == Color("red+", ColorType.EIGHT_BIT, 9, None)
    assert Color.parse("100") == Color("100", ColorType.EIGHT_BIT, 100, None)
    assert Color.parse("#112233") == Color(
        "#112233", ColorType.TRUECOLOR, None, ColorTriplet(0x11, 0x22, 0x33)
    )
    assert Color.parse("rgb(90,100,110)") == Color(
        "rgb(90,100,110)", ColorType.TRUECOLOR, None, ColorTriplet(90, 100, 110)
    )


def test_from_triplet() -> None:
    assert Color.from_triplet(ColorTriplet(0x10, 0x20, 0x30)) == Color(
        "#102030", ColorType.TRUECOLOR, None, ColorTriplet(0x10, 0x20, 0x30)
    )


def test_parse_error() -> None:
    with pytest.raises(ColorParseError):
        Color.parse("rgb(999,0,0)")
    with pytest.raises(ColorParseError):
        Color.parse("rgb(0,0)")
    with pytest.raises(ColorParseError):
        Color.parse("rgb(0,0,0,0)")
    with pytest.raises(ColorParseError):
        Color.parse("nosuchcolor")
    with pytest.raises(ColorParseError):
        Color.parse("#xxyyzz")


def test_parse_rb_hex() -> None:
    assert parse_rgb_hex("aabbcc") == ColorTriplet(0xAA, 0xBB, 0xCC)


def test_blend_rgb() -> None:
    assert blend_rgb(
        ColorTriplet(10, 20, 30), ColorTriplet(30, 40, 50)
    ) == ColorTriplet(20, 30, 40)
