import io
import re

from rich.__main__ import make_test_card
from rich.console import Console, RenderableType

from ._card_render import expected

re_link_ids = re.compile(r"id=[\d\.\-]*?;.*?\x1b")


def replace_link_ids(render: str) -> str:
    """Link IDs have a random ID and system path which is a problem for
    reproducible tests.

    """
    return re_link_ids.sub("id=0;foo\x1b", render)


def render(renderable: RenderableType) -> str:
    console = Console(
        width=100, file=io.StringIO(), color_system="truecolor", legacy_windows=False
    )
    console.print(renderable)
    output = replace_link_ids(console.file.getvalue())
    return output


def test_card_render():
    card = make_test_card()
    result = render(card)
    assert result == expected


if __name__ == "__main__":
    card = make_test_card()
    with open("_card_render.py", "wt") as fh:
        card_render = render(card)
        print(card_render)
        fh.write(f"expected={card_render!r}")
