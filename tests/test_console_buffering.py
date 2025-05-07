from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import time
import sys

def test_buffered_output():
    """Test buffered output behavior."""
    console = Console()
    
    # Example 1: Basic buffering issue
    console.print("\n[bold red]Example 1: Basic Buffering[/bold red]")
    console.print("This text might be buffered:", end="")
    for i in range(5):
        console.print(".", end="")
        time.sleep(0.5)  # Simulate work
    console.print("\n")

    # Example 2: Progress bar with buffering
    console.print("\n[bold blue]Example 2: Progress Bar Buffering[/bold blue]")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Processing...", total=100)
        for i in range(100):
            progress.update(task, advance=1)
            time.sleep(0.05)  # Simulate work

    # Example 3: Real-time updates with flush
    console.print("\n[bold green]Example 3: Real-time Updates with flush[/bold green]")
    for i in range(10):
        console.print(f"Update {i+1}/10", end="\r")
        time.sleep(0.2)
    console.print("\n")

    # Example 4: Mixed content buffering
    console.print("\n[bold yellow]Example 4: Mixed Content Buffering[/bold yellow]")
    console.print("Loading: ", end="")
    for char in "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏":
        console.print(char, end="")
        time.sleep(0.1)
    console.print("\n")

    # Example 5: Table updates with buffering
    console.print("\n[bold magenta]Example 5: Table Updates with Buffering[/bold magenta]")
    from rich.table import Table
    table = Table()
    table.add_column("Status")
    table.add_column("Progress")
    
    for i in range(5):
        table.add_row("Processing", f"{i*20}%")
        console.print(table)
        time.sleep(0.5)
        console.clear()

if __name__ == "__main__":
    test_buffered_output() 