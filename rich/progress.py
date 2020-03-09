from contextlib import contextmanager
from dataclasses import dataclass, field
import sys
from time import monotonic
from threading import Event, RLock, Thread
from typing import Any, Callable, Dict, List, Optional, NewType, Union

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
    total: float
    completed: float
    visible: bool = True
    fields: Dict[str, Any] = field(default_factory=dict)

    @property
    def finished(self) -> bool:
        return self.completed >= self.total

    @property
    def percentage(self) -> float:
        if not self.total:
            return 0.0
        completed = (self.completed / self.total) * 100.0
        completed = min(100, max(0.0, completed))
        return completed


class RefreshThread(Thread):
    """A thread that calls refresh() on the Process object at regular intervals."""

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
            self.progress.refresh()


def bar_widget(task: Task) -> Bar:
    """Gets a progress bar widget for a task."""
    return Bar(total=task.total, completed=task.completed, width=40)


class Progress:
    """Renders an auto-updating progress bar(s).
    
    Args:
        console (Console, optional): Optional Console instance. Default will create own internal Console instance.
        auto_refresh (bool, optional): Enable auto refresh. If disabled, you will need to call `refresh()`.
        refresh_per_second (int, optional): Number of times per second to refresh the progress information. Defaults to 15.
        
    """

    def __init__(
        self,
        *columns: Union[str, WidgetCallable],
        console: Console = None,
        auto_refresh: bool = True,
        refresh_per_second: int = 15
    ) -> None:
        self.columns = columns or (
            "{task.name}",
            bar_widget,
            "{task.percentage:>3.0f}%",
        )
        self.console = console or Console(file=sys.stderr)
        self.refresh_per_second = refresh_per_second
        self.auto_refresh = auto_refresh
        self._tasks: Dict[TaskID, Task] = {}
        self._live_render = LiveRender(self._table)
        self._task_index: TaskID = TaskID(0)
        self._lock = RLock()
        self._refresh_thread: Optional[RefreshThread] = None
        self._refresh_count = 0

    @property
    def tasks(self) -> List[TaskID]:
        """Get a list of task IDs."""
        with self._lock:
            return list(self._tasks.keys())

    @property
    def finished(self) -> bool:
        """Check if all tasks have been completed."""
        with self._lock:
            if not self._tasks:
                return True
            return all(task.finished for task in self._tasks.values())

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
        *,
        total: float = None,
        completed: float = None,
        advance: float = None,
        visible: bool = None,
        **fields: Any
    ) -> None:
        """Update information associated with a task.
        
        Args:
            task_id (TaskID): Task id (return by add_task).
            total (float, optional): Updates task.total if not None.
            completed (float, optional): Updates task.completed if not None.
            advance (float, optional): Add a value to task.completed if not None.
            visible (bool, optional): Set visible flag if not None.
        """
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
            task.fields.update(fields)

    def refresh(self) -> None:
        """Refresh (render) the progress information."""
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
        self.tasks.pop(task_id)


if __name__ == "__main__":

    import time

    with Progress() as progress:

        task1 = progress.add_task("[red]Downloading")
        task2 = progress.add_task("[green]Processing")
        task3 = progress.add_task("[cyan]Cooking")

        while not progress.finished:
            progress.update(task1, advance=1.0)
            progress.update(task2, advance=0.6)
            progress.update(task3, advance=1.7)
            time.sleep(0.05)
