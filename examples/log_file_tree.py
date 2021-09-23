import sys
import time
from pathlib import Path

from rich.console import Console


def logtree(console: Console, start: Path, rate: int = 50):
    """Log the contents of start and its children to the console at the given rate (items/second)."""

    def _log_dir(target: Path, depth: int = 0):
        for path in target.iterdir():
            name = (
                f"[red]{path.name}[/red]/"
                if path.is_dir()
                else f"[green]{path.name}[/green]"
            )
            console.log("  " * depth, name)
            time.sleep(1 / rate)
            if path.is_dir():
                _log_dir(path, depth + 1)

    return _log_dir(start)


if __name__ == "__main__":
    logtree(
        Console(log_path=False), Path.cwd() if len(sys.argv) < 2 else Path(sys.argv[1])
    )
