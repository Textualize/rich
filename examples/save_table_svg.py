"""
Demonstrates how to export a SVG
"""

from rich.console import Console
from rich.table import Table

table = Table(title="Star Wars Movies")

table.add_column("Released", style="cyan", no_wrap=True)
table.add_column("Title", style="magenta")
table.add_column("Box Office", justify="right", style="green")

table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")
table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
table.add_row("Dec 15, 2017", "Star Wars Ep. V111: The Last Jedi", "$1,332,539,889")
table.add_row("Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889")

console = Console(record=True)
console.print(table, justify="center")
console.save_svg("table.svg", title="save_table_svg.py")

import os
import webbrowser

webbrowser.open(f"file://{os.path.abspath('table.svg')}")
