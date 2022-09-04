import io
import re

from rich.console import Console, RenderableType

re_link_ids = re.compile(r"id=[\d\.\-]*?;.*?\x1b")


def replace_link_ids(render: str) -> str:
    """Link IDs have a random ID and system path which is a problem for
    reproducible tests.

    """
    return re_link_ids.sub("id=0;foo\x1b", render)


def render(renderable: RenderableType, no_wrap: bool = False) -> str:
    console = Console(
        width=100, file=io.StringIO(), color_system="truecolor", legacy_windows=False
    )
    console.print(renderable, no_wrap=no_wrap)
    output = replace_link_ids(console.file.getvalue())
    return output
