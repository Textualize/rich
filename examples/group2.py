from rich import print
from rich.console import group
from rich.panel import Panel


@group()
def get_panels():
    yield Panel("Hello", style="on blue")
    yield Panel("World", style="on red")


print(Panel(get_panels()))
