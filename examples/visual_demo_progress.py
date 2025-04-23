"""Visual demonstration of the indeterminate progress bar feature."""

import time
from rich.console import Console
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
    IndeterminateTaskProgressColumn,
    TaskProgressColumn,
)
from rich.panel import Panel
from rich.layout import Layout


def visual_demo():
    """A comprehensive visual demonstration of indeterminate progress bars."""
    console = Console()
    
    console.print("[bold blue]Indeterminate Progress Bar Demonstration[/bold blue]\n")
    console.print("This demo shows the new features for issue #3572:")
    console.print("- Indeterminate progress with animated pulse")
    console.print("- Elapsed time display during indeterminate state")
    console.print("- ?/total indicator for indeterminate tasks")
    console.print("- Transition from indeterminate to determinate state\n")
    
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        IndeterminateTaskProgressColumn(),
        console=console,
        refresh_per_second=20,  # Higher refresh rate for smoother animation
    ) as progress:
        
        # Regular progress bar for comparison
        regular_task = progress.add_task("[green]Regular task", total=100)
        
        # Indeterminate task with expected total
        indeterminate_task1 = progress.add_task(
            "[yellow]Indexing",
            indeterminate=True,
            expected_total=10
        )
        
        # Indeterminate task without expected total
        indeterminate_task2 = progress.add_task(
            "[cyan]Searching",
            indeterminate=True
        )
        
        # Simulate work
        for i in range(100):
            # Update regular task
            progress.update(regular_task, advance=1)
            
            # Let indeterminate tasks animate
            time.sleep(0.05)
            
            # Show message periodically
            if i % 20 == 0 and i > 0:
                console.print(f"[dim]Still processing... ({i}% of demo complete)[/dim]")
        
        # Convert indeterminate tasks to determinate and complete them
        console.print("\n[bold]Converting indeterminate tasks to determinate...[/bold]")
        
        # Complete the indexing task
        progress.update(
            indeterminate_task1,
            indeterminate=False,
            total=10,
            completed=10
        )
        
        # Complete the searching task
        progress.update(
            indeterminate_task2,
            indeterminate=False,
            total=1,
            completed=1
        )
        
        time.sleep(1)  # Show completed state
        
    console.print("\n[bold green]Demo complete![/bold green]")
    console.print("All tasks successfully transitioned from indeterminate to complete state.")


if __name__ == "__main__":
    visual_demo()