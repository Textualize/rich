import pytest

from rich.color import (
    Color,
    ColorParseError,
    ColorSystem,
    ColorTriplet,
    ColorType,
    blend_rgb,
    parse_rgb_hex,
)
from rich.style import Style
from rich.text import Span, Text


def test_str() -> None:
    assert str(Color.parse("red")) == "Color('red', ColorType.STANDARD, number=1)"


def test_repr() -> None:
    assert repr(Color.parse("red")) == "Color('red', ColorType.STANDARD, number=1)"


def test_color_system_repr() -> None:
    assert repr(ColorSystem.EIGHT_BIT) == "ColorSystem.EIGHT_BIT"


def test_rich() -> None:
    color = Color.parse("red")
    as_text = color.__rich__()
    print(repr(as_text))
    print(repr(as_text.spans))
    assert as_text == Text(
        "<color 'red' (standard)⬤ >", spans=[Span(23, 24, Style(color=color))]
    )


def test_system() -> None:
    assert Color.parse("default").system == ColorSystem.STANDARD
    assert Color.parse("red").system == ColorSystem.STANDARD
    assert Color.parse("#ff0000").system == ColorSystem.TRUECOLOR


def test_windows() -> None:
    assert Color("red", ColorType.WINDOWS, number=1).get_ansi_codes() == ("31",)


def test_truecolor() -> None:
    assert Color.parse("#ff0000").get_truecolor() == ColorTriplet(255, 0, 0)
    assert Color.parse("red").get_truecolor() == ColorTriplet(128, 0, 0)
    assert Color.parse("color(1)").get_truecolor() == ColorTriplet(128, 0, 0)
    assert Color.parse("color(17)").get_truecolor() == ColorTriplet(0, 0, 95)
    assert Color.parse("default").get_truecolor() == ColorTriplet(0, 0, 0)
    assert Color.parse("default").get_truecolor(foreground=False) == ColorTriplet(
        255, 255, 255
    )
    assert Color("red", ColorType.WINDOWS, number=1).get_truecolor() == ColorTriplet(
        197, 15, 31
    )


def test_parse_success() -> None:
    assert Color.parse("default") == Color("default", ColorType.DEFAULT, None, None)
    assert Color.parse("red") == Color("red", ColorType.STANDARD, 1, None)
    assert Color.parse("bright_red") == Color("bright_red", ColorType.STANDARD, 9, None)
    assert Color.parse("yellow4") == Color("yellow4", ColorType.EIGHT_BIT, 106, None)
    assert Color.parse("color(100)") == Color(
        "color(100)", ColorType.EIGHT_BIT, 100, None
    )
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


def test_from_rgb() -> None:
    assert Color.from_rgb(0x10, 0x20, 0x30) == Color(
        "#102030", ColorType.TRUECOLOR, None, ColorTriplet(0x10, 0x20, 0x30)
    )


def test_from_ansi() -> None:
    assert Color.from_ansi(1) == Color("color(1)", ColorType.STANDARD, 1)


def test_default() -> None:
    assert Color.default() == Color("default", ColorType.DEFAULT, None, None)


def test_parse_error() -> None:
    with pytest.raises(ColorParseError):
        Color.parse("256")
    with pytest.raises(ColorParseError):
        Color.parse("color(256)")
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
    assert Color.parse("default").get_ansi_codes() == ("39",)
    assert Color.parse("default").get_ansi_codes(False) == ("49",)
    assert Color.parse("red").get_ansi_codes() == ("31",)
    assert Color.parse("red").get_ansi_codes(False) == ("41",)
    assert Color.parse("color(1)").get_ansi_codes() == ("31",)
    assert Color.parse("color(1)").get_ansi_codes(False) == ("41",)
    assert Color.parse("#ff0000").get_ansi_codes() == ("38", "2", "255", "0", "0")
    assert Color.parse("#ff0000").get_ansi_codes(False) == ("48", "2", "255", "0", "0")


def test_downgrade() -> None:

    assert Color.parse("color(9)").downgrade(0) == Color(
        "color(9)", ColorType.STANDARD, 9, None
    )

    assert Color.parse("#000000").downgrade(ColorSystem.EIGHT_BIT) == Color(
        "#000000", ColorType.EIGHT_BIT, 16, None
    )

    assert Color.parse("#ffffff").downgrade(ColorSystem.EIGHT_BIT) == Color(
        "#ffffff", ColorType.EIGHT_BIT, 231, None
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

    assert Color.parse("color(9)").downgrade(ColorSystem.STANDARD) == Color(
        "color(9)", ColorType.STANDARD, 9, None
    )

    assert Color.parse("color(20)").downgrade(ColorSystem.STANDARD) == Color(
        "color(20)", ColorType.STANDARD, 4, None
    )

    assert Color.parse("red").downgrade(ColorSystem.WINDOWS) == Color(
        "red", ColorType.WINDOWS, 1, None
    )

    assert Color.parse("bright_red").downgrade(ColorSystem.WINDOWS) == Color(
        "bright_red", ColorType.WINDOWS, 9, None
    )

    assert Color.parse("#ff0000").downgrade(ColorSystem.WINDOWS) == Color(
        "#ff0000", ColorType.WINDOWS, 1, None
    )

    assert Color.parse("color(255)").downgrade(ColorSystem.WINDOWS) == Color(
        "color(255)", ColorType.WINDOWS, 15, None
    )

    assert Color.parse("#00ff00").downgrade(ColorSystem.STANDARD) == Color(
        "#00ff00", ColorType.STANDARD, 2, None
    )


def test_parse_rgb_hex() -> None:
    assert parse_rgb_hex("aabbcc") == ColorTriplet(0xAA, 0xBB, 0xCC)


def test_blend_rgb() -> None:
    assert blend_rgb(
        ColorTriplet(10, 20, 30), ColorTriplet(30, 40, 50)
    ) == ColorTriplet(20, 30, 40)
