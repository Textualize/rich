from time import sleep

from rich.console import Console
from rich.status import Status
from rich.table import Table


def test_status():

    console = Console(
        color_system=None, width=80, legacy_windows=False, get_time=lambda: 0.0
    )
    status = Status("foo", console=console)
    assert status.console == console
    status.update(status="bar", spinner="dots2", spinner_style="red", speed=2.0)

    assert isinstance(status.renderable, Table)

    # TODO: Testing output is tricky with threads
    with status:
        sleep(0.2)


def test_renderable():
    console = Console(
        color_system=None, width=80, legacy_windows=False, get_time=lambda: 0.0
    )
    status = Status("foo", console=console)
    console.begin_capture()
    console.print(status)
    assert console.end_capture() == "⠋ foo\n"
