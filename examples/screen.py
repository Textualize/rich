"""
Demonstration of Console.screen() 
"""

from time import sleep

from rich.console import Console
from rich.align import Align
from rich.screen import Screen
from rich.panel import Panel

console = Console()

with console.screen():
    panel = Panel(
        Align.center("[blink]Don't Panic!", vertical="middle"),
        style="bold white on red",
    )
    console.print(Screen(panel), end="")
    sleep(5)
