from contextlib import contextmanager
from dataclasses import dataclass, field
import sys
from time import monotonic
from threading import Event, RLock, Thread
from typing import Callable, Dict, List, Optional, NewType, Union

from .bar import Bar
from .console import Console, RenderableType
from .live_render import LiveRender
from .table import Table


TaskID = NewType("TaskID", int)
WidgetCallable = Callable[["Task"], RenderableType]


class ProgressError(Exception):
    pass


class MissingWidget(ProgressError):
    pass


@dataclass
class Task:
    name: str
    total: int
    completed: int
    visible: bool = True
    fields: Dict[str, str] = field(default_factory=dict)

    @property
    def percentage(self) -> float:
        if not self.total:
            return 0.0
        completed = (self.completed / self.total) * 100.0
        completed = min(100, max(0.0, completed))
        return completed


class RefreshThread(Thread):
    """A thread that calls refresh on the Process object at regular intervals."""

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
            try:
                self.progress.refresh()
            except Exception as error:
                raise


def bar_widget(task: Task) -> Bar:
    """Gets a progress bar widget for a task."""
    return Bar(total=task.total, completed=task.completed, width=40)


class Progress:
    def __init__(
        self,
        *columns: Union[str, WidgetCallable],
        console: Console = None,
        refresh_per_second: int = 15,
        auto_refresh: bool = True
    ) -> None:
        self.columns = columns or ("{task.name}", bar_widget, "{task.percentage:.0f}%")
        self.console = console or Console(file=sys.stderr)
        self.refresh_per_second = refresh_per_second
        self.auto_refresh = auto_refresh
        self._tasks: Dict[TaskID, Task] = {}
        self._live_render = LiveRender(self._table)
        self._task_index: TaskID = TaskID(0)
        self._lock = RLock()
        self._refresh_thread: Optional[RefreshThread] = None
        self._refresh_count = 0

    def __enter__(self) -> "Progress":
        self.console.show_cursor(False)
        if self.auto_refresh:
            self._refresh_thread = RefreshThread(self, self.refresh_per_second)
            self._refresh_thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.auto_refresh:
                self._refresh_thread.stop()
                self._refresh_thread = None
            self.refresh()
            self.console.line()
        finally:
            self.console.show_cursor(True)

    def update(
        self,
        task_id: TaskID,
        total: int = None,
        completed: int = None,
        advance: int = None,
        visible: bool = None,
        **fields: RenderableType
    ) -> None:
        with self._lock:
            task = self._tasks[task_id]
            if total is not None:
                task.total = total
            if advance is not None:
                task.completed += advance
            if completed is not None:
                task.completed = completed
            if visible is not None:
                task.visible = True

    def refresh(self) -> None:
        with self._lock:
            self._live_render.set_renderable(self._table)
            self.console.print(self._live_render)
            self._refresh_count += 1

    @property
    def _table(self) -> Table:
        table = Table.grid()
        table.padding = (0, 1, 0, 0)
        for _, task in self._tasks.items():
            if task.visible:
                row: List[RenderableType] = []
                for column in self.columns:
                    if isinstance(column, str):
                        row.append(column.format(task=task))
                    else:
                        widget = column(task)
                        row.append(widget)
                table.add_row(*row)
        return table

    def add_task(
        self,
        name: str,
        total: int = 100,
        completed: int = 0,
        visible: bool = True,
        **fields: str
    ) -> TaskID:
        with self._lock:
            task = Task(name, total, completed, visible=visible, fields=fields)
            self._tasks[self._task_index] = task
            self.refresh()
            try:
                return self._task_index
            finally:
                self._task_index = TaskID(int(self._task_index) + 1)

    def remove_task(self, task_id: TaskID) -> None:
        """Delete a task if it exists.
        
        Args:
            task_id (TaskID): A task ID.
        
        """
        self._tasks.pop(task_id)


if __name__ == "__main__":
    import time

    with Progress() as progress:
        task_id = progress.add_task("Processing...")

        for i in range(100):
            progress.update(task_id, completed=i)
            time.sleep(0.05)
