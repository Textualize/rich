from rich.console import Console


def test_jupyter():
    console = Console(force_jupyter=True)
    assert console.width == 93
    assert console.color_system == "truecolor"
