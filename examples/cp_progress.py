"""
A very minimal `cp` clone that displays a progress bar.
"""
import os
import shutil
import sys

from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

progress = Progress(
    TextColumn("[bold blue]{task.description}", justify="right"),
    BarColumn(bar_width=None),
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    DownloadColumn(),
    "•",
    TransferSpeedColumn(),
    "•",
    TimeRemainingColumn(),
)

if __name__ == "__main__":
    if len(sys.argv) == 3:

        with progress:
            desc=os.path.basename(sys.argv[1])
            with progress.read(sys.argv[1], description=desc) as src:
                with open(sys.argv[2], "wb") as dst:
                    shutil.copyfileobj(src, dst)
    else:
        print("Usage:\n\tpython cp_progress.py SRC DST")
