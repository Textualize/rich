from rich import print
from rich.console import render_group
from rich.panel import Panel


@render_group()
def get_panels():
    yield Panel("Hello", style="on blue")
    yield Panel("World", style="on red")


print(Panel(get_panels()))
