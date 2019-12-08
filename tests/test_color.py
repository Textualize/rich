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
    assert str(Color.parse("red")) == "\x1b[31m⬤  \x1b[0m<color 'red' (standard)>"


def test_repr() -> None:
    assert repr(Color.parse("red")) == "<color 'red' (standard)>"


def test_system() -> None:
    assert Color.parse("default").system == ColorSystem.STANDARD
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


def test_default() -> None:
    assert Color.default() == Color("default", ColorType.DEFAULT, None, None)


def test_parse_error() -> None:
    with pytest.raises(ColorParseError):
        Color.parse("256")
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


def test_get_ansi_codes() -> None:
    assert Color.parse("default").get_ansi_codes() == ["39"]
    assert Color.parse("default").get_ansi_codes(False) == ["49"]
    assert Color.parse("red").get_ansi_codes() == ["31"]
    assert Color.parse("red").get_ansi_codes(False) == ["41"]
    assert Color.parse("1").get_ansi_codes() == ["38", "5", "1"]
    assert Color.parse("1").get_ansi_codes(False) == ["48", "5", "1"]
    assert Color.parse("#ff0000").get_ansi_codes() == ["38", "2", "255", "0", "0"]
    assert Color.parse("#ff0000").get_ansi_codes(False) == ["48", "2", "255", "0", "0"]


def test_downgrade() -> None:

    assert Color.parse("9").downgrade(0) == Color("9", ColorType.EIGHT_BIT, 9, None)

    assert Color.parse("#000000").downgrade(ColorSystem.EIGHT_BIT) == Color(
        "#000000", ColorType.EIGHT_BIT, 0, None
    )

    assert Color.parse("#ffffff").downgrade(ColorSystem.EIGHT_BIT) == Color(
        "#ffffff", ColorType.EIGHT_BIT, 15, None
    )

    assert Color.parse("#404142").downgrade(ColorSystem.EIGHT_BIT) == Color(
        "#404142", ColorType.EIGHT_BIT, 237, None
    )

    assert Color.parse("#ff0000").downgrade(ColorSystem.EIGHT_BIT) == Color(
        "#ff0000", ColorType.EIGHT_BIT, 196, None
    )
    assert Color.parse("#ff0000").downgrade(ColorSystem.STANDARD) == Color(
        "#ff0000", ColorType.STANDARD, 1, None
    )

    assert Color.parse("9").downgrade(ColorSystem.STANDARD) == Color(
        "9", ColorType.STANDARD, 1, None
    )


def test_parse_rgb_hex() -> None:
    assert parse_rgb_hex("aabbcc") == ColorTriplet(0xAA, 0xBB, 0xCC)


def test_blend_rgb() -> None:
    assert blend_rgb(
        ColorTriplet(10, 20, 30), ColorTriplet(30, 40, 50)
    ) == ColorTriplet(20, 30, 40)
