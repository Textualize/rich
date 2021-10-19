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

    console.print(table)


# Prints table
print_table()

# Get console output as text
file1 = "table_export_plaintext.txt"
text = console.export_text()
with open(file1, "w") as file:
    file.write(text)
print(f"Exported console output as plain text to {file1}")

# Calling print_table again because console output buffer
# is flushed once export function is called
print_table()

# Get console output as html
# use clear=False so output is not flushed after export
file2 = "table_export_html.html"
html = console.export_html(clear=False)
with open(file2, "w") as file:
    file.write(html)
print(f"Exported console output as html to {file2}")

# Export text output to table_export.txt
file3 = "table_export_plaintext2.txt"
console.save_text(file3, clear=False)
print(f"Exported console output as plain text to {file3}")

# Export html output to table_export.html
file4 = "table_export_html2.html"
console.save_html(file4)
print(f"Exported console output as html to {file4}")
