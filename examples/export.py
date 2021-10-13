"""
Demonstrates export console output
"""

from rich.console import Console
from rich.table import Table

console = Console(record=True)


def print_table():
    table = Table(title="Star Wars Movies")

    table.add_column("Released", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Box Office", justify="right", style="green")

    table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")
    table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
    table.add_row("Dec 15, 2017", "Star Wars Ep. V111: The Last Jedi", "$1,332,539,889")
    table.add_row("Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889")

    console.print(table, justify="center")


# Prints table
print_table()

# Get console output as text
text = console.export_text()

# Calling print_table again because console output buffer
# is flushed once export function is called
print_table()

# Get console output as html
# use clear=False so output is not flushed after export
html = console.export_html(clear=False)

# Export text output to table_export.txt
console.save_text("table_export.txt", clear=False)

# Export html output to table_export.html
console.save_html("table_export.html")
