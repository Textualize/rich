from rich.color_triplet import ColorTriplet


def test_hex():
    assert ColorTriplet(255, 255, 255).hex == "#ffffff"
    assert ColorTriplet(0, 255, 0).hex == "#00ff00"


def test_rgb():
    assert ColorTriplet(255, 255, 255).rgb == "rgb(255,255,255)"
    assert ColorTriplet(0, 255, 0).rgb == "rgb(0,255,0)"


def test_normalized():
    assert ColorTriplet(255, 255, 255).normalized == (1.0, 1.0, 1.0)
    assert ColorTriplet(0, 255, 0).normalized == (0.0, 1.0, 0.0)
