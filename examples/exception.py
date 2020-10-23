"""
Basic example to show how to print an traceback of an exception
"""

from rich.console import Console
from rich.panel import Panel

console = Console()


def zero(number: int) -> int:
    same_number = number
    result = same_number / 0
    return result


if __name__ == "__main__":
    console.print(Panel("[i] Print exception traceback[/i]"))
    try:
        zero(10)
    except:
        console.print_exception()
        console.print("[red]Exception catched")

    console.print(
        Panel(
            "[i] Print exception traceback with 5 extra lines and locals[/i]",
            style="yellow",
        )
    )
    try:
        zero(20)
    except:
        console.print_exception(extra_lines=5, show_locals=True)
        console.print("[red]Exception also catched")
