"""

This example demonstrates how to make colorful bars.

"""

from rich.block_bar import BlockBar
from rich.console import Console
from rich.table import Table

table = Table()
table.add_column("Score")

table.add_row(BlockBar(size=100, begin=0, end=5, width=30, color="bright_red"))
table.add_row(BlockBar(size=100, begin=0, end=35, width=30, color="bright_yellow"))
table.add_row(BlockBar(size=100, begin=0, end=87, width=30, color="bright_green"))

console = Console()
console.print(table, justify="center")
