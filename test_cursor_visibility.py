from rich.progress import Progress
import time
import sys

def test_cursor_visibility():
    """Test cursor visibility is maintained even when progress is interrupted."""
    print("Starting progress bar. Press Ctrl+C to interrupt after a few seconds.")
    print("You should still see the cursor after interruption.")
    
    try:
        with Progress() as progress:
            task = progress.add_task("[green]Processing...", total=100)
            
            # Simulate long-running task
            for i in range(100):
                time.sleep(0.1)
                progress.update(task, completed=i+1)
                
    except KeyboardInterrupt:
        print("\nProgress was interrupted!")
        # The cursor should be visible here thanks to our fix
        
    # This line helps verify cursor is visible
    input("If you can see your cursor, press Enter to continue...")

if __name__ == "__main__":
    test_cursor_visibility() 