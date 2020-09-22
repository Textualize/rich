import io
import logging

from rich.console import Console
from rich.logging import RichHandler

handler = RichHandler(
    console=Console(
        file=io.StringIO(), force_terminal=True, width=80, color_system="truecolor"
    ),
    enable_link_path=False,
)
logging.basicConfig(
    level="NOTSET", format="%(message)s", datefmt="[DATE]", handlers=[handler]
)
log = logging.getLogger("rich")


def make_log():
    log.debug("foo")
    render = handler.console.file.getvalue()
    return render


def test_log():
    render = make_log()
    print(repr(render))
    expected = "\x1b[2;36m[DATE]\x1b[0m\x1b[2;36m \x1b[0m\x1b[32mDEBUG\x1b[0m    foo                                           \x1b[2mtest_logging.py\x1b[0m\x1b[2m:20\x1b[0m\n"
    assert render == expected


def test_exception():
    console = Console(
        file=io.StringIO(), force_terminal=True, width=80, color_system="truecolor"
    )
    handler_with_tracebacks = RichHandler(
        console=console, enable_link_path=False, handle_tracebacks=True
    )
    log.addHandler(handler_with_tracebacks)

    try:
        1 / 0
    except ZeroDivisionError:
        log.exception("message")

    render = handler_with_tracebacks.console.file.getvalue()
    print(render)

    excpected = "ZeroDivisionError: \x1b[0mdivision by zero\n"
    assert excpected == render[-40:]
    assert render.count("\n") == 13


def test_exception_with_extra_lines():
    console = Console(
        file=io.StringIO(), force_terminal=True, width=80, color_system="truecolor"
    )
    handler_extra_lines = RichHandler(
        console=console,
        enable_link_path=False,
        markup=True,
        handle_tracebacks=True,
        tracebacks_extra_lines=5,
    )
    log.addHandler(handler_extra_lines)

    try:
        1 / 0
    except ZeroDivisionError:
        log.exception("message")

    render = handler_extra_lines.console.file.getvalue()
    print(render)

    excpected = "ZeroDivisionError: \x1b[0mdivision by zero\n"
    assert excpected == render[-40:]
    assert render.count("\n") == 17


if __name__ == "__main__":
    render = make_log()
    print(render)
    print(repr(render))
