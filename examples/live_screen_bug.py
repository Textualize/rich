from rich.console import Console
from rich.live import Live
import time

console = Console()

with Live("Live screen test", screen=True, refresh_per_second=4) as live:
    for i in range(5):
        console.print(f"Iteration {i}")
        time.sleep(0.5)
    console.log("This is a log message inside Live screen mode.")
    time.sleep(1)
