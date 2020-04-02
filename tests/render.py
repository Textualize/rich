import io

from rich.console import Console, RenderableType


def render(renderable: RenderableType) -> str:
    console = Console(width=100, file=io.StringIO(), color_system="truecolor")
    console.print(renderable)
    output = console.file.getvalue()
    return output
