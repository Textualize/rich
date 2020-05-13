import io
import logging

from rich.console import Console
from rich.logging import RichHandler

handler = RichHandler(
    console=Console(file=io.StringIO(), force_terminal=True, width=80)
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
    expected = "\x1b[2;36m[DATE]\x1b[0m\x1b[2;36m \x1b[0m\x1b[32mDEBUG\x1b[0m    foo                                         \x1b[2m test_logging.py:17\x1b[0m\x1b[2m \x1b[0m\n"
    assert render == expected


if __name__ == "__main__":
    render = make_log()
    print(render)
    print(repr(render))
