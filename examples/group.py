from rich import print
from rich.console import Group
from rich.panel import Panel

panel_group = Group(
    Panel("Hello", style="on blue"),
    Panel("World", style="on red"),
)
print(Panel(panel_group))
