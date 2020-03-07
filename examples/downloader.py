from concurrent.futures import ThreadPoolExecutor
import os.path
from urllib.request import urlopen

from rich.progress import bar_widget, Progress, Task


def copy_url(task: Task, url: str, path: str) -> None:
    response = urlopen(url)
    task.total = int(response.info()["Content-length"])
    with open(path, "wb") as dest_file:
        for data in iter(lambda: response.read(16384), b""):
            dest_file.write(data)
            task.completed += len(data)


def read_url(task: Task, url: str) -> None:
    all_data = []
    response = urlopen(url)
    task.total = int(response.info()["Content-length"])
    for data in iter(lambda: response.read(16384), b""):
        all_data.append(data)
        task.completed += len(data)
    return b"".join(all_data).decode("utf-8")


class Downloader:
    def __init__(self, url: str, dest_dir: str) -> None:
        self.url = url
        self.pool = ThreadPoolExecutor(max_workers=5)

    def start(self):
        with Progress(bar_widget, "{task.percentage:0.1f}%", "{url}") as progress:
            task = progress.add_task(url=self.url)
            self.pool.submit(task, download_url, url=self.url)

