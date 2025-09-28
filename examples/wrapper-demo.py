from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()


def cprint(text, style="bold green", panel=False):
    """
    Quick styled text printing using Rich.

    Parameters:
        text (str): The message to print.
        style (str): Rich style string (e.g., "bold red").
        panel (bool): If True, wraps the text inside a Rich Panel.

    Example:
        cprint("Hello!", style="bold magenta")
        cprint("Important message", panel=True)
    """
    if panel:
        console.print(Panel(text, style=style))
    else:
        console.print(text, style=style)


def ctable(headers, rows, header_style="cyan", row_style=None, title=None):
    """
    Quick table rendering using Rich.

    Parameters:
        headers (list[str]): Column headers.
        rows (list[list[str]]): Table rows.
        header_style (str): Style for header row.
        row_style (str): Style for all row cells (optional).
        title (str): Optional table title.

    Example:
        ctable(
            headers=["Name", "Score"],
            rows=[["Ehsan", "100"], ["Ali", "95"]],
            header_style="bright_white",
            row_style="green",
            title="Scoreboard"
        )
    """
    table = Table(show_header=True, header_style=header_style, box=box.ROUNDED)
    if title:
        table.title = title

    for h in headers:
        table.add_column(h)

    for row in rows:
        styled_row = [
            f"[{row_style}]{cell}[/{row_style}]" if row_style else cell
            for cell in row
        ]
        table.add_row(*styled_row)

    console.print(table)


def cstatus(message, style="bold yellow"):
    """
    Show a temporary status spinner using Rich.

    Parameters:
        message (str): Status message to display.
        style (str): Style for the status text.

    Example:
        cstatus("Processing data...")
    """
    with console.status(f"[{style}]{message}[/{style}]"):
        import time
        time.sleep(3)  # Simulate processing


if __name__ == "__main__":
    cprint("Hello Ehsan! This is a simple styled message.", style="bold magenta")
    cprint("This message is wrapped inside a panel.", style="bold blue", panel=True)

    ctable(
        headers=["Name", "Score"],
        rows=[["Ehsan", "100"], ["Ali", "95"]],
        header_style="bright_white",
        row_style="green",
        title="Scoreboard"
    )

    cstatus("Processing data...")