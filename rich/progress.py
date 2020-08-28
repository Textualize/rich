import io
import sys
from abc import ABC, abstractmethod
from collections import deque
from collections.abc import Sized
from dataclasses import dataclass, field
from datetime import timedelta
from math import ceil
from threading import Event, RLock, Thread
from time import monotonic
from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    Callable,
    Deque,
    Dict,
    Iterable,
    List,
    NamedTuple,
    NewType,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)

from . import filesize, get_console
from .bar import Bar
from .console import (
    Console,
    ConsoleRenderable,
    JustifyMethod,
    RenderableType,
    RenderGroup,
    RenderHook,
)
from .control import Control
from .highlighter import Highlighter
from .jupyter import JupyterMixin
from .live_render import LiveRender
from .style import StyleType
from .table import Table
from .text import Text

TaskID = NewType("TaskID", int)

ProgressType = TypeVar("ProgressType")


GetTimeCallable = Callable[[], float]


class _TrackThread(Thread):
    """A thread to periodically update progress."""

    def __init__(self, progress: "Progress", task_id: "TaskID", update_period: float):
        self.progress = progress
        self.task_id = task_id
        self.update_period = update_period
        self.done = Event()

        self.completed = 0
        super().__init__()

    def run(self) -> None:
        task_id = self.task_id
        advance = self.progress.advance
        update_period = self.update_period
        last_completed = 0
        wait = self.done.wait
        while not wait(update_period):
            completed = self.completed
            if last_completed != completed:
                advance(task_id, completed - last_completed)
                last_completed = completed
        self.progress.update(self.task_id, completed=self.completed, refresh=True)

    def __enter__(self) -> "_TrackThread":
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.done.set()
        self.join()


def track(
    sequence: Union[Sequence[ProgressType], Iterable[ProgressType]],
    description="Working...",
    total: int = None,
    auto_refresh=True,
    console: Optional[Console] = None,
    transient: bool = False,
    get_time: Callable[[], float] = None,
    refresh_per_second: int = None,
    style: StyleType = "bar.back",
    complete_style: StyleType = "bar.complete",
    finished_style: StyleType = "bar.finished",
    pulse_style: StyleType = "bar.pulse",
    update_period: float = 0.1,
) -> Iterable[ProgressType]:
    """Track progress by iterating over a sequence.

    Args:
        sequence (Iterable[ProgressType]): A sequence (must support "len") you wish to iterate over.
        description (str, optional): Description of task show next to progress bar. Defaults to "Working".
        total: (int, optional): Total number of steps. Default is len(sequence).
        auto_refresh (bool, optional): Automatic refresh, disable to force a refresh after each iteration. Default is True.
        transient: (bool, optional): Clear the progress on exit. Defaults to False.
        console (Console, optional): Console to write to. Default creates internal Console instance.
        refresh_per_second (Optional[int], optional): Number of times per second to refresh the progress information, or None to use default. Defaults to None.
        style (StyleType, optional): Style for the bar background. Defaults to "bar.back".
        complete_style (StyleType, optional): Style for the completed bar. Defaults to "bar.complete".
        finished_style (StyleType, optional): Style for a finished bar. Defaults to "bar.done".
        pulse_style (StyleType, optional): Style for pulsing bars. Defaults to "bar.pulse".
        update_period (float, optional): Minimum time (in seconds) between calls to update(). Defaults to 0.1.
    Returns:
        Iterable[ProgressType]: An iterable of the values in the sequence.

    """

    columns: List["ProgressColumn"] = (
        [TextColumn("[progress.description]{task.description}")] if description else []
    )
    columns.extend(
        (
            BarColumn(
                style=style,
                complete_style=complete_style,
                finished_style=finished_style,
                pulse_style=pulse_style,
            ),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
        )
    )
    progress = Progress(
        *columns,
        auto_refresh=auto_refresh,
        console=console,
        transient=transient,
        get_time=get_time,
        refresh_per_second=refresh_per_second,
    )

    yield from progress.track(
        sequence, total=total, description=description, update_period=update_period
    )


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
        justify: JustifyMethod = "left",
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
    """Renders a visual progress bar.

    Args:
        bar_width (Optional[int], optional): Width of bar or None for full width. Defaults to 40.
        style (StyleType, optional): Style for the bar background. Defaults to "bar.back".
        complete_style (StyleType, optional): Style for the completed bar. Defaults to "bar.complete".
        finished_style (StyleType, optional): Style for a finished bar. Defaults to "bar.done".
        pulse_style (StyleType, optional): Style for pulsing bars. Defaults to "bar.pulse".
    """

    def __init__(
        self,
        bar_width: Optional[int] = 40,
        style: StyleType = "bar.back",
        complete_style: StyleType = "bar.complete",
        finished_style: StyleType = "bar.finished",
        pulse_style: StyleType = "bar.pulse",
    ) -> None:
        self.bar_width = bar_width
        self.style = style
        self.complete_style = complete_style
        self.finished_style = finished_style
        self.pulse_style = pulse_style
        super().__init__()

    def render(self, task: "Task") -> Bar:
        """Gets a progress bar widget for a task."""
        return Bar(
            total=max(0, task.total),
            completed=max(0, task.completed),
            width=None if self.bar_width is None else max(1, self.bar_width),
            pulse=not task.started,
            animation_time=task.get_time(),
            style=self.style,
            complete_style=self.complete_style,
            finished_style=self.finished_style,
            pulse_style=self.pulse_style,
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
    """Timestamp of sample."""
    completed: float
    """Number of steps completed."""


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
    """dict: Arbitrary fields passed in via Progress.update."""

    start_time: Optional[float] = field(default=None, init=False, repr=False)
    """Optional[float]: Time this task was started, or None if not started."""

    stop_time: Optional[float] = field(default=None, init=False, repr=False)
    """Optional[float]: Time this task was stopped, or None if not stopped."""

    _progress: Deque[ProgressSample] = field(
        default_factory=deque, init=False, repr=False
    )

    def get_time(self) -> float:
        """float: Get the current time, in seconds."""
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
        """float: Get progress of task as a percentage."""
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
        progress = self._progress
        if not progress:
            return None
        total_time = progress[-1].timestamp - progress[0].timestamp
        if total_time == 0:
            return None
        iter_progress = iter(progress)
        next(iter_progress)
        total_completed = sum(sample.completed for sample in iter_progress)
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


class _FileProxy(io.TextIOBase):
    """Wraps a file (e.g. sys.stdout) and redirects writes to a console."""

    def __init__(self, console: Console, file: IO[str]) -> None:
        self.__console = console
        self.__file = file
        self.__buffer: List[str] = []

    def __getattr__(self, name: str) -> Any:
        return getattr(self.__file, name)

    def write(self, text: str) -> int:
        buffer = self.__buffer
        lines: List[str] = []
        while text:
            line, new_line, text = text.partition("\n")
            if new_line:
                lines.append("".join(buffer) + line)
                del buffer[:]
            else:
                buffer.append(line)
                break
        if lines:
            console = self.__console
            with console:
                output = "\n".join(lines)
                console.print(output, markup=False, emoji=False, highlight=False)
        return len(text)

    def flush(self) -> None:
        buffer = self.__buffer
        if buffer:
            self.__console.print("".join(buffer))
            del buffer[:]


class Progress(JupyterMixin, RenderHook):
    """Renders an auto-updating progress bar(s).

    Args:
        console (Console, optional): Optional Console instance. Default will an internal Console instance writing to stdout.
        auto_refresh (bool, optional): Enable auto refresh. If disabled, you will need to call `refresh()`.
        refresh_per_second (Optional[int], optional): Number of times per second to refresh the progress information or None to use default (10). Defaults to None.
        speed_estimate_period: (float, optional): Period (in seconds) used to calculate the speed estimate. Defaults to 30.
        transient: (bool, optional): Clear the progress on exit. Defaults to False.
        redirect_stout: (bool, optional): Enable redirection of stdout, so ``print`` may be used. Defaults to True.
        redirect_stout: (bool, optional): Enable redirection of stderr. Defaults to True.
        get_time: (Callable, optional): A callable that gets the current time, or None to use time.monotonic. Defaults to None.
    """

    def __init__(
        self,
        *columns: Union[str, ProgressColumn],
        console: Console = None,
        auto_refresh: bool = True,
        refresh_per_second: int = None,
        speed_estimate_period: float = 30.0,
        transient: bool = False,
        redirect_stdout: bool = True,
        redirect_stderr: bool = True,
        get_time: GetTimeCallable = None,
    ) -> None:
        assert (
            refresh_per_second is None or refresh_per_second > 0
        ), "refresh_per_second must be > 0"
        self._lock = RLock()
        self.columns = columns or (
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
        )
        self.console = console or get_console()
        self.auto_refresh = auto_refresh and not self.console.is_jupyter
        self.refresh_per_second = refresh_per_second or 10
        self.speed_estimate_period = speed_estimate_period
        self.transient = transient
        self._redirect_stdout = redirect_stdout
        self._redirect_stderr = redirect_stderr
        self.get_time = get_time or monotonic
        self._tasks: Dict[TaskID, Task] = {}
        self._live_render = LiveRender(self.get_renderable())
        self._task_index: TaskID = TaskID(0)
        self._refresh_thread: Optional[_RefreshThread] = None
        self._started = False
        self.print = self.console.print
        self.log = self.console.log
        self._restore_stdout: Optional[IO[str]] = None
        self._restore_stderr: Optional[IO[str]] = None
        self.ipy_widget: Optional[Any] = None

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

    def _enable_redirect_io(self):
        """Enable redirecting of stdout / stderr."""
        if self.console.is_terminal:
            if self._redirect_stdout:
                self._restore_stdout = sys.stdout
                sys.stdout = _FileProxy(self.console, sys.stdout)
            if self._redirect_stderr:
                self._restore_stderr = sys.stderr
                sys.stdout = _FileProxy(self.console, sys.stdout)

    def _disable_redirect_io(self):
        """Disable redirecting of stdout / stderr."""
        if self._restore_stdout:
            sys.stdout = self._restore_stdout
            self._restore_stdout = None
        if self._restore_stderr:
            sys.stderr = self._restore_stderr
            self._restore_stderr = None

    def start(self) -> None:
        """Start the progress display."""
        with self._lock:
            if self._started:
                return
            self._started = True
            self.console.show_cursor(False)
            self._enable_redirect_io()
            self.console.push_render_hook(self)
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
                self._disable_redirect_io()
                self.console.pop_render_hook()
        if self._refresh_thread is not None:
            self._refresh_thread.join()
            self._refresh_thread = None
        if self.transient:
            self.console.control(self._live_render.restore_cursor())
        if self.ipy_widget is not None and self.transient:  # pragma: no cover
            self.ipy_widget.clear_output()
            self.ipy_widget.close()

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
        update_period: float = 0.1,
    ) -> Iterable[ProgressType]:
        """Track progress by iterating over a sequence.

        Args:
            sequence (Sequence[ProgressType]): A sequence of values you want to iterate over and track progress.
            total: (int, optional): Total number of steps. Default is len(sequence).
            task_id: (TaskID): Task to track. Default is new task.
            description: (str, optional): Description of task, if new task is created.
            update_period (float, optional): Minimum time (in seconds) between calls to update(). Defaults to 0.1.

        Returns:
            Iterable[ProgressType]: An iterable of values taken from the provided sequence.
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
            if self.auto_refresh:
                with _TrackThread(self, task_id, update_period) as track_thread:
                    for value in sequence:
                        yield value
                        track_thread.completed += 1
            else:
                advance = self.advance
                refresh = self.refresh
                for value in sequence:
                    yield value
                    advance(task_id, 1)
                    refresh()

    def start_task(self, task_id: TaskID) -> None:
        """Start a task.

        Starts a task (used when calculating elapsed time). You may need to call this manually,
        if you called ``add_task`` with ``start=False``.

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
        description: str = None,
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
            description (str, optional): Change task description if not None.
            visible (bool, optional): Set visible flag if not None.
            refresh (bool): Force a refresh of progress information. Default is False.
            **fields (Any): Additional data fields required for rendering.
        """
        with self._lock:
            task = self._tasks[task_id]
            completed_start = task.completed

            if total is not None:
                task.total = total
            if advance is not None:
                task.completed += advance
            if completed is not None:
                task.completed = completed
            if description is not None:
                task.description = description
            if visible is not None:
                task.visible = visible
            task.fields.update(fields)
            update_completed = task.completed - completed_start

            if refresh:
                self.refresh()

            current_time = self.get_time()
            old_sample_time = current_time - self.speed_estimate_period
            _progress = task._progress

            popleft = _progress.popleft
            while _progress and _progress[0].timestamp < old_sample_time:
                popleft()
            while len(_progress) > 20:
                popleft()
            _progress.append(ProgressSample(current_time, update_completed))

    def advance(self, task_id: TaskID, advance: float = 1) -> None:
        """Advance task by a number of steps.

        Args:
            task_id (TaskID): ID of task.
            advance (float): Number of steps to advance. Default is 1.
        """
        current_time = self.get_time()
        with self._lock:
            task = self._tasks[task_id]
            completed_start = task.completed
            task.completed += advance
            update_completed = task.completed - completed_start
            old_sample_time = current_time - self.speed_estimate_period
            _progress = task._progress

            popleft = _progress.popleft
            while _progress and _progress[0].timestamp < old_sample_time:
                popleft()
            while len(_progress) > 10:
                popleft()
            _progress.append(ProgressSample(current_time, update_completed))

    def refresh(self) -> None:
        """Refresh (render) the progress information."""
        if self.console.is_jupyter:  # pragma: no cover
            try:
                from ipywidgets import Output
                from IPython.display import display
            except ImportError:
                import warnings

                warnings.warn('install "ipywidgets" for Jupyter support')
            else:
                with self._lock:
                    if self.ipy_widget is None:
                        self.ipy_widget = Output()
                        display(self.ipy_widget)

                    with self.ipy_widget:
                        self.ipy_widget.clear_output(wait=True)
                        self.console.print(self.get_renderable())

        elif self.console.is_terminal and not self.console.is_dumb_terminal:
            with self._lock:
                self._live_render.set_renderable(self.get_renderable())
                with self.console:
                    self.console.print(Control(""))

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

        table = Table.grid(padding=(0, 1))
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

    def process_renderables(
        self, renderables: List[ConsoleRenderable]
    ) -> List[ConsoleRenderable]:
        """Process renderables to restore cursor and display progress."""
        if self.console.is_terminal:
            renderables = [
                self._live_render.position_cursor(),
                *renderables,
                self._live_render,
            ]
        return renderables


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

    console = Console()
    with Progress(console=console, transient=True) as progress:

        task1 = progress.add_task("[red]Downloading", total=1000)
        task2 = progress.add_task("[green]Processing", total=1000)
        task3 = progress.add_task("[yellow]Thinking", total=1000, start=False)

        while not progress.finished:
            progress.update(task1, advance=0.5)
            progress.update(task2, advance=0.3)
            time.sleep(0.01)
            if random.randint(0, 100) < 1:
                progress.log(next(examples))
