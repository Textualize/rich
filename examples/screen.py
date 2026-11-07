"""
Demonstration of Console.screen()
"""

from time import sleep

from rich.align import Align
from rich.console import Console
from rich.panel import Panel

console = Console()

with console.screen(style="bold white on red") as screen:
    text = Align.center("[blink]Don't Panic![/blink]", vertical="middle")
    screen.update(Panel(text))
    sleep(5)
