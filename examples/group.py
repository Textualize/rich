from rich import print
from rich.console import RenderGroup
from rich.panel import Panel

panel_group = RenderGroup(
    Panel("Hello", style="on blue"),
    Panel("World", style="on red"),
)
print(Panel(panel_group))
