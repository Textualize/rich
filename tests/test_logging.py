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
    expected = "\x1b[2;36m[DATE]\x1b[0m\x1b[2;36m \x1b[0m\x1b[32mDEBUG\x1b[0m    foo                                           \x1b[2mtest_logging.py:17\x1b[0m\n"
    assert render == expected


def test_emoji():
    from rich.emoji import Emoji

    log.debug(":thumbs_up:")
    assert Emoji.replace(":thumbs_up:") in handler.console.file.getvalue()


if __name__ == "__main__":
    render = make_log()
    print(render)
    print(repr(render))
