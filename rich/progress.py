from contextlib import contextmanager
from dataclasses import dataclass, field
from time import monotonic
from threading import Event, Lock, Thread
from typing import Callable, Dict, List, Optional, Union

from .bar import Bar
from .console import Console, RenderableType
from .live_render import LiveRender
from .table import Table

WidgetCallable = Callable[["Task"], RenderableType]


class ProgressError(Exception):
    pass


class MissingWidget(ProgressError):
    pass


@dataclass
class Task:
    total: int
    completed: int
    fields: Dict[str, str] = field(default_factory=dict)

    @property
    def percentage(self) -> float:
        if not self.total:
            return 0.0
        completed = (self.completed / self.total) * 100.0
        completed = min(100, max(0.0, completed))
        return completed


class RefreshThread(Thread):
    def __init__(self, progress: "Progress", refresh_per_second: int = 10) -> None:
        self.progress = progress
        self.refresh_per_second = refresh_per_second
        self.done = Event()
        super().__init__()

    def stop(self) -> None:
        self.done.set()
        self.join()

    def run(self) -> None:
        while not self.done.wait(1.0 / self.refresh_per_second):
            if self.progress._refresh_count:
                try:
                    self.progress.refresh()
                except Exception as error:
                    raise


def bar_widget(task: Task) -> Bar:
    """Gets a progress bar widget for a task."""
    return Bar(total=task.total, completed=task.completed, width=20)


class Progress:
    def __init__(
        self,
        *columns: Union[str, WidgetCallable],
        console: Console = None,
        refresh_per_second: int = 10
    ) -> None:
        self.columns = columns or ("$bar", "{percentage:2.0f}%")
        self.console = console or Console()
        self.refresh_per_second = refresh_per_second
        self._tasks: Dict[int, Task] = {}
        self._table = Table.grid()
        self._live_render = LiveRender(self._table)
        self._task_index = 0
        self._lock = Lock()
        self._refresh_thread: Optional[RefreshThread] = None
        self._refresh_count = 0

    def __getitem__(self, index: int) -> Task:
        return self._tasks[index]

    def __enter__(self) -> "Progress":
        self.console.show_cursor(False)
        self._refresh_thread = RefreshThread(self, self.refresh_per_second)
        self._refresh_thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._refresh_thread.stop()
        self._refresh_thread = None
        self.refresh()
        self.console.show_cursor(True)
        self.console.line()

    def update(
        self,
        bar_no=0,
        total: int = None,
        completed: int = None,
        **fields: RenderableType
    ) -> None:
        task = self._tasks[bar_no]
        if total is not None:
            task.total = total
        if completed is not None:
            task.completed = completed

    def refresh(self) -> None:
        with self._lock:
            self._live_render.renderable = self.table
            self.console.print(self._live_render)
            self._refresh_count += 1

    @property
    def table(self) -> Table:
        table = Table.grid()
        table.padding = (0, 1, 0, 0)

        for _, task in self._tasks.items():
            row: List[RenderableType] = []
            for column in self.columns:
                if isinstance(column, str):
                    row.append(column.format(task=task))
                else:
                    widget = column(task)
                    row.append(widget)
            table.add_row(*row)
        return table

    def add_task(self, total: int = 100, completed: int = 0, *fields: str) -> Task:
        task = Task(total, completed)
        self._tasks[self._task_index] = task
        try:
            return task
        finally:
            self._task_index += 1


if __name__ == "__main__":
    import time

    with Progress(bar_widget, "{task.percentage:.0f}%") as progress:
        task = progress.add_task()
        progress.refresh()
        for _ in range(100):
            task.completed += 1
            time.sleep(0.05)
