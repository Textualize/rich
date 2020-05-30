from abc import ABC, abstractmethod
from collections import deque
from collections.abc import Sized
from contextlib import contextmanager
from dataclasses import dataclass, replace, field
from datetime import timedelta
from math import ceil, floor
import sys
from time import monotonic
from threading import Event, RLock, Thread
from typing import (
    Any,
    Callable,
    cast,
    Deque,
    Dict,
    Iterable,
    List,
    Optional,
    NamedTuple,
    Sequence,
    Tuple,
    TypeVar,
    NewType,
    Union,
)

from . import get_console
from .bar import Bar
from .console import Console, JustifyValues, RenderGroup, RenderableType
from .highlighter import Highlighter
from . import filesize
from .live_render import LiveRender
from .style import Style, StyleType
from .table import Table
from .text import Text


TaskID = NewType("TaskID", int)

ProgressType = TypeVar("ProgressType")


GetTimeCallable = Callable[[], float]


def track(
    sequence: Union[Sequence[ProgressType], Iterable[ProgressType]],
    description="Working...",
    total: int = None,
    auto_refresh=True,
    console: Optional[Console] = None,
    get_time: Callable[[], float] = None,
) -> Iterable[ProgressType]:
    """Track progress of processing a sequence.
    
    Args:
        sequence (Iterable[ProgressType]): A sequence (must support "len") you wish to iterate over.
        description (str, optional): Description of task show next to progress bar. Defaults to "Working".
        total: (int, optional): Total number of steps. Default is len(sequence).
        auto_refresh (bool, optional): Automatic refresh, disable to force a refresh after each iteration. Default is True.
        console (Console, optional): Console to write to. Default creates internal Console instance.
    
    Returns:
        Iterable[ProgressType]: An iterable of the values in the sequence.
    
    """
    progress = Progress(auto_refresh=auto_refresh, console=console, get_time=get_time)

    task_total = total
    if task_total is None:
        if isinstance(sequence, Sized):
            task_total = len(sequence)
        else:
            raise ValueError(
                f"unable to get size of {sequence!r}, please specify 'total'"
            )

    task_id = progress.add_task(description, total=task_total)
    with progress:
        for completed, value in enumerate(sequence, 1):
            yield value
            progress.update(task_id, completed=completed)
            if not auto_refresh:
                progress.refresh()


class ProgressColumn(ABC):
    """Base class for a widget to use in progress display."""

    max_refresh: Optional[float] = None

    def __init__(self) -> None:
        self._renderable_cache: Dict[TaskID, Tuple[float, RenderableType]] = {}
        self._update_time: Optional[float] = None

    def __call__(self, task: "Task") -> RenderableType:
        """Called by the Progress object to return a renderable for the given task.
        
        Args:
            task (Task): An object containing information regarding the task.
        
        Returns:
            RenderableType: Anything renderable (including str).
        """
        current_time = task.get_time()  # type: ignore
        if self.max_refresh is not None and not task.completed:
            try:
                timestamp, renderable = self._renderable_cache[task.id]
            except KeyError:
                pass
            else:
                if timestamp + self.max_refresh > current_time:
                    return renderable

        renderable = self.render(task)
        self._renderable_cache[task.id] = (current_time, renderable)
        return renderable

    @abstractmethod
    def render(self, task: "Task") -> RenderableType:
        """Should return a renderable object."""


class TextColumn(ProgressColumn):
    """A column containing text."""

    def __init__(
        self,
        text_format: str,
        style: StyleType = "none",
        justify: JustifyValues = "left",
        markup: bool = True,
        highlighter: Highlighter = None,
    ) -> None:
        self.text_format = text_format
        self.justify = justify
        self.style = style
        self.markup = markup
        self.highlighter = highlighter
        super().__init__()

    def render(self, task: "Task"):
        _text = self.text_format.format(task=task)
        if self.markup:
            text = Text.from_markup(_text, style=self.style, justify=self.justify)
        else:
            text = Text(_text, style=self.style, justify=self.justify)
        if self.highlighter:
            self.highlighter.highlight(text)
        return text


class BarColumn(ProgressColumn):
    """Renders a progress bar."""

    def __init__(self, bar_width: Optional[int] = 40) -> None:
        self.bar_width = bar_width
        super().__init__()

    def render(self, task: "Task") -> Bar:
        """Gets a progress bar widget for a task."""
        return Bar(
            total=max(0, task.total),
            completed=max(0, task.completed),
            width=None if self.bar_width is None else max(1, self.bar_width),
            pulse=not task.started,
            animation_time=task.get_time(),
        )


class TimeRemainingColumn(ProgressColumn):
    """Renders estimated time remaining."""

    # Only refresh twice a second to prevent jitter
    max_refresh = 0.5

    def render(self, task: "Task") -> Text:
        """Show time remaining."""
        remaining = task.time_remaining
        if remaining is None:
            return Text("-:--:--", style="progress.remaining")
        remaining_delta = timedelta(seconds=int(remaining))
        return Text(str(remaining_delta), style="progress.remaining")


class FileSizeColumn(ProgressColumn):
    """Renders completed filesize."""

    def render(self, task: "Task") -> Text:
        """Show data completed."""
        data_size = filesize.decimal(int(task.completed))
        return Text(data_size, style="progress.filesize")


class TotalFileSizeColumn(ProgressColumn):
    """Renders total filesize."""

    def render(self, task: "Task") -> Text:
        """Show data completed."""
        data_size = filesize.decimal(int(task.total))
        return Text(data_size, style="progress.filesize.total")


class DownloadColumn(ProgressColumn):
    """Renders file size downloaded and total, e.g. '0.5/2.3 GB'."""

    def render(self, task: "Task") -> Text:
        """Calculate common unit for completed and total."""
        completed = int(task.completed)
        total = int(task.total)
        unit, suffix = filesize.pick_unit_and_suffix(
            total, ["bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"], 1024
        )
        completed_ratio = completed / unit
        total_ratio = total / unit
        precision = 0 if unit == 1 else 1
        completed_str = f"{completed_ratio:,.{precision}f}"
        total_str = f"{total_ratio:,.{precision}f}"
        download_status = f"{completed_str}/{total_str} {suffix}"
        download_text = Text(download_status, style="progress.download")
        return download_text


class TransferSpeedColumn(ProgressColumn):
    """Renders human readable transfer speed."""

    def render(self, task: "Task") -> Text:
        """Show data transfer speed."""
        speed = task.speed
        if speed is None:
            return Text("?", style="progress.data.speed")
        data_speed = filesize.decimal(int(speed))
        return Text(f"{data_speed}/s", style="progress.data.speed")


class ProgressSample(NamedTuple):
    """Sample of progress for a given time."""

    timestamp: float
    completed: float


@dataclass
class Task:
    """Information regarding a progress task.
    
    This object should be considered read-only outside of the :class:`~Progress` class.

    """

    id: TaskID
    """Task ID associated with this task (used in Progress methods)."""

    description: str
    """str: Description of the task."""

    total: float
    """str: Total number of steps in this task."""

    completed: float
    """float: Number of steps completed"""

    _get_time: GetTimeCallable
    """Callable to get the current time."""

    visible: bool = True
    """bool: Indicates if this task is visible in the progress display."""

    fields: Dict[str, Any] = field(default_factory=dict)
    """Arbitrary fields passed in via Progress.update."""

    start_time: Optional[float] = field(default=None, init=False, repr=False)
    """Optional[float]: Time this task was started, or None if not started."""

    stop_time: Optional[float] = field(default=None, init=False, repr=False)
    """Optional[float]: Time this task was stopped, or None if not stopped."""

    _progress: Deque[ProgressSample] = field(
        default_factory=deque, init=False, repr=False
    )

    def get_time(self) -> float:
        """Get the current time, in seconds."""
        return self._get_time()  # type: ignore

    @property
    def started(self) -> bool:
        """bool: Check if the task as started."""
        return self.start_time is not None

    @property
    def remaining(self) -> float:
        """float: Get the number of steps remaining."""
        return self.total - self.completed

    @property
    def elapsed(self) -> Optional[float]:
        """Optional[float]: Time elapsed since task was started, or ``None`` if the task hasn't started."""
        if self.start_time is None:
            return None
        if self.stop_time is not None:
            return self.stop_time - self.start_time
        return self.get_time() - self.start_time

    @property
    def finished(self) -> bool:
        """bool: Check if the task has completed."""
        return self.completed >= self.total

    @property
    def percentage(self) -> float:
        """float: Get progress of task as a percantage."""
        if not self.total:
            return 0.0
        completed = (self.completed / self.total) * 100.0
        completed = min(100.0, max(0.0, completed))
        return completed

    @property
    def speed(self) -> Optional[float]:
        """Optional[float]: Get the estimated speed in steps per second."""
        if self.start_time is None:
            return None
        progress = list(self._progress)
        if not progress:
            return None
        total_time = progress[-1].timestamp - progress[0].timestamp
        if total_time == 0:
            return None
        total_completed = sum(sample.completed for sample in progress[1:])
        speed = total_completed / total_time
        return speed

    @property
    def time_remaining(self) -> Optional[float]:
        """Optional[float]: Get estimated time to completion, or ``None`` if no data."""
        if self.finished:
            return 0.0
        speed = self.speed
        if not speed:
            return None
        estimate = ceil(self.remaining / speed)
        return estimate


class _RefreshThread(Thread):
    """A thread that calls refresh() on the Process object at regular intervals."""

    def __init__(self, progress: "Progress", refresh_per_second: int = 10) -> None:
        self.progress = progress
        self.refresh_per_second = refresh_per_second
        self.done = Event()
        super().__init__()

    def stop(self) -> None:
        self.done.set()

    def run(self) -> None:
        while not self.done.wait(1.0 / self.refresh_per_second):
            self.progress.refresh()


class Progress:
    """Renders an auto-updating progress bar(s).
    
    Args:
        console (Console, optional): Optional Console instance. Default will an internal Console instance writing to stdout.
        auto_refresh (bool, optional): Enable auto refresh. If disabled, you will need to call `refresh()`.
        refresh_per_second (int, optional): Number of times per second to refresh the progress information. Defaults to 10.
        speed_estimate_period: (float, optional): Period (in seconds) used to calculate the speed estimate. Defaults to 30.
    """

    def __init__(
        self,
        *columns: Union[str, ProgressColumn],
        console: Console = None,
        auto_refresh: bool = True,
        refresh_per_second: int = 10,
        speed_estimate_period: float = 30.0,
        get_time: GetTimeCallable = None,
    ) -> None:
        assert refresh_per_second > 0, "refresh_per_second must be > 0"
        self._lock = RLock()
        self.columns = columns or (
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
        )
        self.console = console or get_console()
        self.auto_refresh = auto_refresh
        self.refresh_per_second = refresh_per_second
        self.speed_estimate_period = speed_estimate_period
        self.get_time = get_time or monotonic
        self._tasks: Dict[TaskID, Task] = {}
        self._live_render = LiveRender(self.get_renderable())
        self._task_index: TaskID = TaskID(0)
        self._refresh_thread: Optional[_RefreshThread] = None
        self._refresh_count = 0
        self._started = False

    @property
    def tasks(self) -> List[Task]:
        """Get a list of Task instances."""
        with self._lock:
            return list(self._tasks.values())

    @property
    def task_ids(self) -> List[TaskID]:
        """A list of task IDs."""
        with self._lock:
            return list(self._tasks.keys())

    @property
    def finished(self) -> bool:
        """Check if all tasks have been completed."""
        with self._lock:
            if not self._tasks:
                return True
            return all(task.finished for task in self._tasks.values())

    def start(self) -> None:
        """Start the progress display."""
        with self._lock:
            if self._started:
                return
            self._started = True
            self.console.show_cursor(False)
            self.refresh()
            if self.auto_refresh:
                self._refresh_thread = _RefreshThread(self, self.refresh_per_second)
                self._refresh_thread.start()

    def stop(self) -> None:
        """Stop the progress display."""
        with self._lock:
            if not self._started:
                return
            self._started = False
            try:
                if self.auto_refresh and self._refresh_thread is not None:
                    self._refresh_thread.stop()
                self.refresh()
                if self.console.is_terminal:
                    self.console.line()
            finally:
                self.console.show_cursor(True)
        if self._refresh_thread is not None:
            self._refresh_thread.join()
            self._refresh_thread = None

    def __enter__(self) -> "Progress":
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.stop()

    def track(
        self,
        sequence: Union[Iterable[ProgressType], Sequence[ProgressType]],
        total: int = None,
        task_id: Optional[TaskID] = None,
        description="Working...",
    ) -> Iterable[ProgressType]:
        """[summary]
        
        Args:
            sequence (Sequence[ProgressType]): [description]
            total: (int, optional): Total number of steps. Default is len(sequence).
            task_id: (TaskID): Task to track. Default is new task.
            description: (str, optional): Description of task, if new task is created.
        
        Returns:
            Iterable[ProgressType]: [description]
        """
        if total is None:
            if isinstance(sequence, Sized):
                task_total = len(sequence)
            else:
                raise ValueError(
                    f"unable to get size of {sequence!r}, please specify 'total'"
                )
        else:
            task_total = total

        if task_id is None:
            task_id = self.add_task(description, total=task_total)
        else:
            self.update(task_id, total=task_total)
        with self:
            for completed, value in enumerate(sequence, 1):
                yield value
                self.update(task_id, completed=completed)

    def start_task(self, task_id: TaskID) -> None:
        """Start a task.

        Starts a task (used when calculating elapsed time). You may need to call this manually,
        if you called `add_task` with ``start=False``.
        
        Args:
            task_id (TaskID): ID of task.
        """
        with self._lock:
            task = self._tasks[task_id]
            if task.start_time is None:
                task.start_time = self.get_time()

    def stop_task(self, task_id: TaskID) -> None:
        """Stop a task.

        This will freeze the elapsed time on the task.
        
        Args:
            task_id (TaskID): ID of task.
        """
        with self._lock:
            task = self._tasks[task_id]
            current_time = self.get_time()
            if task.start_time is None:
                task.start_time = current_time
            task.stop_time = current_time

    def update(
        self,
        task_id: TaskID,
        *,
        total: float = None,
        completed: float = None,
        advance: float = None,
        visible: bool = None,
        refresh: bool = False,
        **fields: Any,
    ) -> None:
        """Update information associated with a task.
        
        Args:
            task_id (TaskID): Task id (returned by add_task).            
            total (float, optional): Updates task.total if not None.
            completed (float, optional): Updates task.completed if not None.
            advance (float, optional): Add a value to task.completed if not None.
            visible (bool, optional): Set visible flag if not None.
            refresh (bool): Force a refresh of progress information. Default is False.
            **fields (Any): Additional data fields required for rendering.
        """
        current_time = self.get_time()
        with self._lock:
            task = self._tasks[task_id]
            completed_start = task.completed

            if total is not None:
                task.total = total
            if advance is not None:
                task.completed += advance
            if completed is not None:
                task.completed = completed
            if visible is not None:
                task.visible = visible
            task.fields.update(fields)

            update_completed = task.completed - completed_start
            old_sample_time = current_time - self.speed_estimate_period
            _progress = task._progress

            while _progress and _progress[0].timestamp < old_sample_time:
                _progress.popleft()
            task._progress.append(ProgressSample(current_time, update_completed))
            if refresh:
                self.refresh()

    def advance(self, task_id: TaskID, advance: float = 1) -> None:
        """Advance task by a number of steps.
        
        Args:
            task_id (TaskID): ID of task.
            advance (float): Number of steps to advance. Default is 1.
        """
        self.update(task_id, advance=advance)

    def refresh(self) -> None:
        """Refresh (render) the progress information."""
        with self._lock:
            self._live_render.set_renderable(self.get_renderable())
            if self.console.is_terminal:
                with self.console:
                    self.console.print(self._live_render.position_cursor())
                    self.console.print(self._live_render)
            self._refresh_count += 1

    def get_renderable(self) -> RenderableType:
        """Get a renderable for the progress display."""
        renderable = RenderGroup(*self.get_renderables())
        return renderable

    def get_renderables(self) -> Iterable[RenderableType]:
        """Get a number of renderables for the progress display."""
        table = self.make_tasks_table(self.tasks)
        yield table

    def make_tasks_table(self, tasks: Iterable[Task]) -> Table:
        """Get a table to render the Progress display.

        Args:
            tasks (Iterable[Task]): An iterable of Task instances, one per row of the table.

        Returns:
            Table: A table instance.
        """

        table = Table.grid()
        table.pad_edge = True
        table.padding = (0, 1, 0, 0)
        for _ in self.columns:
            table.add_column()
        for task in tasks:
            if task.visible:
                row: List[RenderableType] = []
                append = row.append
                for index, column in enumerate(self.columns):
                    if isinstance(column, str):
                        append(column.format(task=task))
                        table.columns[index].no_wrap = True
                    else:
                        widget = column(task)
                        append(widget)
                        if isinstance(widget, (str, Text)):
                            table.columns[index].no_wrap = True
                table.add_row(*row)
        return table

    def add_task(
        self,
        description: str,
        start: bool = True,
        total: int = 100,
        completed: int = 0,
        visible: bool = True,
        **fields: Any,
    ) -> TaskID:
        """Add a new 'task' to the Progress display.
        
        Args:
            description (str): A description of the task.
            start (bool, optional): Start the task immediately (to calculate elapsed time). If set to False,
                you will need to call `start` manually. Defaults to True.
            total (int, optional): Number of total steps in the progress if know. Defaults to 100.
            completed (int, optional): Number of steps completed so far.. Defaults to 0.
            visible (bool, optional): Enable display of the task. Defaults to True.
            **fields (str): Additional data fields required for rendering.
        
        Returns:
            TaskID: An ID you can use when calling `update`.
        """
        with self._lock:
            task = Task(
                self._task_index,
                description,
                total,
                completed,
                visible=visible,
                fields=fields,
                _get_time=self.get_time,
            )
            self._tasks[self._task_index] = task
            if start:
                self.start_task(self._task_index)
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
        with self._lock:
            del self._tasks[task_id]

    def print(
        self,
        *objects: Any,
        sep=" ",
        end="\n",
        style: Union[str, Style] = None,
        justify: JustifyValues = None,
        emoji: bool = None,
        markup: bool = None,
        highlight: bool = None,
    ) -> None:
        """Print to the terminal and preserve progress display. Parameters identical to :class:`~rich.console.Console.print`."""
        console = self.console
        with console:
            if console.is_terminal:
                console.print(self._live_render.position_cursor())
            console.print(
                *objects,
                sep=sep,
                end=end,
                style=style,
                justify=justify,
                emoji=emoji,
                markup=markup,
                highlight=highlight,
            )
            if console.is_terminal:
                console.print(self._live_render)

    def log(
        self,
        *objects: Any,
        sep=" ",
        end="\n",
        justify: JustifyValues = None,
        emoji: bool = None,
        markup: bool = None,
        highlight: bool = None,
        log_locals: bool = False,
        _stack_offset=1,
    ) -> None:
        """Log to the terminal and preserve progress display. Parameters identical to :class:`~rich.console.Console.log`."""
        console = self.console
        with console:
            if console.is_terminal:
                console.print(self._live_render.position_cursor())
            console.log(
                *objects,
                sep=sep,
                end=end,
                justify=justify,
                emoji=emoji,
                markup=markup,
                highlight=highlight,
                log_locals=log_locals,
                _stack_offset=_stack_offset + 1,
            )
            if console.is_terminal:
                console.print(self._live_render)


if __name__ == "__main__":  # pragma: no coverage

    import time
    import random

    from .panel import Panel
    from .syntax import Syntax
    from .table import Table
    from .rule import Rule

    syntax = Syntax(
        '''def loop_last(values: Iterable[T]) -> Iterable[Tuple[bool, T]]:
"""Iterate and generate a tup`le with a flag for last value."""
iter_values = iter(values)
try:
    previous_value = next(iter_values)
except StopIteration:
    return
for value in iter_values:
    yield False, previous_value
    previous_value = value
yield True, previous_value''',
        "python",
        line_numbers=True,
    )

    table = Table("foo", "bar", "baz")
    table.add_row("1", "2", "3")

    progress_renderables = [
        "Text may be printed while the progress bars are rendering.",
        Panel("In fact, [i]any[/i] renderable will work"),
        "Such as [magenta]tables[/]...",
        table,
        "Pretty printed structures...",
        {"type": "example", "text": "Pretty printed"},
        "Syntax...",
        syntax,
        Rule("Give it a try!"),
    ]

    from itertools import cycle

    examples = cycle(progress_renderables)

    with Progress() as progress:

        task1 = progress.add_task(" [red]Downloading", total=1000)
        task2 = progress.add_task(" [green]Processing", total=1000)
        task3 = progress.add_task(" [yellow]Thinking", total=1000, start=False)

        while not progress.finished:
            progress.update(task1, advance=0.5)
            progress.update(task2, advance=0.3)
            time.sleep(0.01)
            if random.randint(0, 100) < 1:
                progress.log(next(examples))
