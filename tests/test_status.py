from time import sleep

from rich.console import Console
from rich.spinner import Spinner
from rich.status import Status


def test_status():
    console = Console(
        color_system=None, width=80, legacy_windows=False, get_time=lambda: 0.0
    )
    status = Status("foo", console=console)
    assert status.console == console
    previous_status_renderable = status.renderable
    status.update(status="bar", spinner_style="red", speed=2.0)

    assert previous_status_renderable == status.renderable
    assert isinstance(status.renderable, Spinner)
    status.update(spinner="dots2")
    assert previous_status_renderable != status.renderable

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
