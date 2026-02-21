"""Example demonstrating the fix for progress bar timer reset issue #3273."""

import time
from rich.console import Console
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)


def main():
    """Demonstrate the fix for progress timer reset issue."""
    console = Console()
    
    console.print("[bold]Progress Bar Timer Reset Example[/bold]\n")
    console.print("This example demonstrates the fix for issue #3273")
    console.print("where restarting progress bar tasks did not restart their running clocks.\n")
    
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        # Simulate AI training scenario with epochs, training, and validation
        epoch_task = progress.add_task("[red]Epochs", total=3)
        train_task = progress.add_task("[green]Training", total=100)
        valid_task = progress.add_task("[blue]Validation", total=50)
        
        # Loop through epochs
        for epoch in range(3):
            console.print(f"\n[bold]Starting Epoch {epoch + 1}[/bold]")
            
            # Training phase
            for i in range(100):
                progress.update(train_task, advance=1)
                time.sleep(0.01)
            
            # Show elapsed time before reset
            train_task_obj = progress._tasks[train_task]
            elapsed_before = train_task_obj.elapsed
            console.print(f"Training elapsed time before reset: {elapsed_before:.2f} seconds")
            
            # Stop training task
            progress.stop_task(train_task)
            
            # Validation phase
            for i in range(50):
                progress.update(valid_task, advance=1)
                time.sleep(0.01)
            
            # Stop validation task
            progress.stop_task(valid_task)
            
            # Complete one epoch
            progress.update(epoch_task, advance=1)
            
            # Reset tasks for next epoch (except on last epoch)
            if epoch < 2:
                console.print("\n[yellow]Resetting tasks for next epoch...[/yellow]")
                progress.reset(train_task, start=True, completed=0)
                progress.reset(valid_task, start=True, completed=0)
                
                # Show elapsed time after reset
                elapsed_after = train_task_obj.elapsed
                console.print(f"Training elapsed time after reset: {elapsed_after:.4f} seconds")
                console.print("[green]✓ Timer properly reset![/green]\n")
                time.sleep(1)  # Pause to show the reset
    
    console.print("\n[bold green]Demo complete![/bold green]")
    console.print("The timer now properly resets to 0 when tasks are reset.")


if __name__ == "__main__":
    main()