import time
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

def test_buffered_output():
    """Test the new buffering methods."""
    console = Console()
    
    # Test basic buffered output
    console.print("\n[bold]1. Basic Buffered Output[/bold]")
    console.print_buffered("Loading", end="")
    for _ in range(5):
        time.sleep(0.2)
        console.print_buffered(".", end="", flush=True)
    console.print_buffered(" Done!")
    
    # Test progress updates
    console.print("\n[bold]2. Progress Updates[/bold]")
    for i in range(101):
        console.print_progress(f"Progress: {i}%", end="")
        time.sleep(0.02)
    console.print()  # New line after progress
    
    # Test spinner animation
    console.print("\n[bold]3. Spinner Animation[/bold]")
    spinner_chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    for _ in range(20):
        for char in spinner_chars:
            console.print_progress(f"Loading {char}", end="")
            time.sleep(0.1)
    console.print()
    
    # Test table updates
    console.print("\n[bold]4. Table Updates[/bold]")
    table = Table()
    table.add_column("Task")
    table.add_column("Status")
    
    tasks = ["Task 1", "Task 2", "Task 3", "Task 4"]
    for task in tasks:
        table.add_row(task, "Processing...")
        console.print(table)
        time.sleep(0.5)
        table.rows[-1][1] = "Done!"
        console.print_progress(table)
    console.print()
    
    # Test context manager
    console.print("\n[bold]5. Buffered Output Context[/bold]")
    with console.buffered_output(buffer_size=1024):
        for i in range(5):
            console.print_buffered(f"Buffered line {i+1}")
            time.sleep(0.2)
    
    # Test performance measurement
    console.print("\n[bold]6. Performance Measurement[/bold]")
    results = console.measure_performance(iterations=100)
    console.print(f"Buffered time: {results['buffered']:.4f}s")
    console.print(f"Unbuffered time: {results['unbuffered']:.4f}s")
    console.print(f"Ratio: {results['ratio']:.2f}x")

if __name__ == "__main__":
    test_buffered_output() 