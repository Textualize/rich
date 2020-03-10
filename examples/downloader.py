from concurrent.futures import ThreadPoolExecutor
from functools import partial
import os.path
import sys
from typing import Iterable
from urllib.request import urlopen

from rich.progress import (
    bar_widget,
    data_speed_widget,
    file_size_widget,
    remaining_widget,
    Progress,
    TaskID,
)


progress = Progress(
    "[bold blue]{task.fields[filename]}",
    bar_widget,
    "[progress.percentage]{task.percentage:>3.0f}%",
    "•",
    file_size_widget,
    "•",
    data_speed_widget,
    "•",
    remaining_widget,
)


def copy_url(task_id: TaskID, url: str, path: str) -> None:
    """Copy data from a url to a local file."""
    response = urlopen(url)
    # This will break if the response doesn't content content length
    progress.update(task_id, total=int(response.info()["Content-length"]))
    with open(path, "wb") as dest_file:
        for data in iter(partial(response.read, 32768), b""):
            dest_file.write(data)
            progress.update(task_id, advance=len(data))


def download(urls: Iterable[str], dest_dir: str):
    """Download multuple files to the given directory."""
    with progress:
        with ThreadPoolExecutor(max_workers=4) as pool:
            for url in urls:
                filename = url.split("/")[-1]
                task_id = progress.add_task("download", filename=filename)
                dest_path = os.path.join(dest_dir, filename)
                pool.submit(copy_url, task_id, url, dest_path)


if __name__ == "__main__":
    if sys.argv[1:]:
        download(sys.argv[1:], "./")
    else:
        print("Usage:\n\tpython downloader.py URL1 URL2 URL3 (etc)")
