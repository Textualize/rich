from rich.console import Console
import time
import sys

def test_buffered_output_fix():
    """Test the fixed buffered output behavior."""
    console = Console()
    
    # Example 1: Basic buffering fix
    console.print("\n[bold red]Example 1: Fixed Basic Buffering[/bold red]")
    console.print_buffered("This text will appear smoothly:", end="")
    for i in range(5):
        console.print_buffered(".", end="")
        time.sleep(0.5)
    console.print_buffered("\n")

    # Example 2: Progress updates fix
    console.print("\n[bold blue]Example 2: Fixed Progress Updates[/bold blue]")
    for i in range(10):
        console.print_progress(f"Progress: {i*10}%", end="\r")
        time.sleep(0.2)
    console.print_buffered("\n")

    # Example 3: Spinner animation fix
    console.print("\n[bold green]Example 3: Fixed Spinner Animation[/bold green]")
    spinner = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    for char in spinner:
        console.print_progress(f"Loading: {char}", end="\r")
        time.sleep(0.1)
    console.print_buffered("\n")

    # Example 4: Table updates fix
    console.print("\n[bold yellow]Example 4: Fixed Table Updates[/bold yellow]")
    from rich.table import Table
    table = Table()
    table.add_column("Status")
    table.add_column("Progress")
    
    for i in range(5):
        table.add_row("Processing", f"{i*20}%")
        console.print_progress(table)
        time.sleep(0.5)
        console.clear()
    console.print_buffered("\n")

if __name__ == "__main__":
    test_buffered_output_fix() 