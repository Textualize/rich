"""Example usage of indeterminate progress bar with elapsed time."""

import time
from rich.console import Console
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
    IndeterminateTaskProgressColumn,
)


def main():
    """Demonstrate the indeterminate progress bar as requested in issue #3572."""
    console = Console()
    
    console.print("[bold]Indeterminate Progress Bar Example[/bold]\n")
    console.print("As requested in issue #3572: showing indeterminate state with elapsed time\n")
    
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeElapsedColumn(),
        IndeterminateTaskProgressColumn(),
        console=console,
        refresh_per_second=10,
    ) as progress:
        # Create an indeterminate task with expected total
        task_id = progress.add_task(
            "Indexing",
            indeterminate=True,
            expected_total=10
        )
        
        console.print("Task is running in indeterminate mode...\n")
        
        # Let it run for a few seconds showing the animation
        for i in range(30):
            time.sleep(0.1)
            if i % 10 == 0:
                console.print(f"Still working... ({i // 10 + 1}/3)")
        
        # Now convert to determinate and complete
        console.print("\nConverting to determinate and completing...")
        progress.update(
            task_id,
            indeterminate=False,
            total=10,
            completed=10
        )
        
        # Keep it displayed for a moment
        time.sleep(1)
        
        console.print("\n[bold green]Task completed![/bold green]")


if __name__ == "__main__":
    main()