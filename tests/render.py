import io
import re

from rich.console import Console, RenderableType


re_link_ids = re.compile(r"id=\d*?;")


def replace_link_ids(render: str) -> str:
    """Link IDs have a random ID which is a problem for reproducable tests."""
    return re_link_ids.sub("id=0", render)


def render(renderable: RenderableType) -> str:
    console = Console(width=100, file=io.StringIO(), color_system="truecolor")
    console.print(renderable)
    output = replace_link_ids(console.file.getvalue())
    return output
