from rich.color import ColorSystem
from rich.console import Console, ConsoleOptions
from rich.style import Style


def test_console_options_update():
    options = ConsoleOptions(
        min_width=10, max_width=20, is_terminal=False, encoding="utf-8"
    )
    options1 = options.update(width=15)
    assert options1.min_width == 15 and options1.max_width == 15

    options2 = options.update(min_width=5, max_width=15, justify="right")
    assert (
        options2.min_width == 5
        and options2.max_width == 15
        and options2.justify == "right"
    )

    options_copy = options.update()
    assert options_copy == options and options_copy is not options


def test_init():
    console = Console(color_system=None)
    assert console._color_system == None
    console = Console(color_system="standard")
    assert console._color_system == ColorSystem.STANDARD
    console = Console(color_system="auto")


def test_size():
    console = Console()
    w, h = console.size
    assert console.width == w

    console = Console(width=99, height=101)
    w, h = console.size
    assert w == 99 and h == 101
