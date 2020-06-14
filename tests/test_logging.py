import io
import logging

from rich.console import Console
from rich.logging import RichHandler

handler = RichHandler(
    console=Console(
        file=io.StringIO(), force_terminal=True, width=80, color_system="truecolor"
    )
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
    expected = "\x1b[2;36m[DATE]\x1b[0m\x1b[2;36m \x1b[0m\x1b[32mDEBUG\x1b[0m    foo                                           \x1b]8;id=3292318898;file:///Users/willmcgugan/projects/rich/tests/test_logging.py\x1b\\\x1b[2mtest_logging.py\x1b[0m\x1b]8;;\x1b\\\x1b[2m:19\x1b[0m\n"
    assert render == expected


if __name__ == "__main__":
    render = make_log()
    print(render)
    print(repr(render))
