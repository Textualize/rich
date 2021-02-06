# encoding=utf-8

import io
from time import sleep

import pytest

from rich.progress_bar import ProgressBar
from rich.console import Console
from rich.highlighter import NullHighlighter
from rich.progress import (
    BarColumn,
    FileSizeColumn,
    TotalFileSizeColumn,
    DownloadColumn,
    TransferSpeedColumn,
    RenderableColumn,
    SpinnerColumn,
    Progress,
    Task,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    track,
    _TrackThread,
    TaskID,
)
from rich.text import Text


class MockClock:
    """A clock that is manually advanced."""

    def __init__(self, time=0.0, auto=True) -> None:
        self.time = time
        self.auto = auto

    def __call__(self) -> float:
        try:
            return self.time
        finally:
            if self.auto:
                self.time += 1

    def tick(self, advance: float = 1) -> None:
        self.time += advance


def test_bar_columns():
    bar_column = BarColumn(100)
    assert bar_column.bar_width == 100
    task = Task(1, "test", 100, 20, _get_time=lambda: 1.0)
    bar = bar_column(task)
    assert isinstance(bar, ProgressBar)
    assert bar.completed == 20
    assert bar.total == 100


def test_text_column():
    text_column = TextColumn("[b]foo", highlighter=NullHighlighter())
    task = Task(1, "test", 100, 20, _get_time=lambda: 1.0)
    text = text_column.render(task)
    assert str(text) == "foo"

    text_column = TextColumn("[b]bar", markup=False)
    task = Task(1, "test", 100, 20, _get_time=lambda: 1.0)
    text = text_column.render(task)
    assert text == Text("[b]bar")


def test_time_remaining_column():
    class FakeTask(Task):
        time_remaining = 60

    column = TimeRemainingColumn()
    task = Task(1, "test", 100, 20, _get_time=lambda: 1.0)
    text = column(task)
    assert str(text) == "-:--:--"

    text = column(FakeTask(1, "test", 100, 20, _get_time=lambda: 1.0))
    assert str(text) == "0:01:00"


def test_renderable_column():
    column = RenderableColumn("foo")
    task = Task(1, "test", 100, 20, _get_time=lambda: 1.0)
    assert column.render(task) == "foo"


def test_spinner_column():
    column = SpinnerColumn()
    column.set_spinner("dots2")
    task = Task(1, "test", 100, 20, _get_time=lambda: 1.0)
    result = column.render(task)
    print(repr(result))
    expected = "⡿"
    assert str(result) == expected


def test_download_progress_uses_decimal_units() -> None:

    column = DownloadColumn()
    test_task = Task(1, "test", 1000, 500, _get_time=lambda: 1.0)
    rendered_progress = str(column.render(test_task))
    expected = "0.5/1.0 KB"
    assert rendered_progress == expected


def test_download_progress_uses_binary_units() -> None:

    column = DownloadColumn(binary_units=True)
    test_task = Task(1, "test", 1024, 512, _get_time=lambda: 1.0)
    rendered_progress = str(column.render(test_task))
    expected = "0.5/1.0 KiB"
    assert rendered_progress == expected


def test_task_ids():
    progress = make_progress()
    assert progress.task_ids == [0, 1, 2, 4]


def test_finished():
    progress = make_progress()
    assert not progress.finished


def make_progress() -> Progress:
    _time = 0.0

    def fake_time():
        nonlocal _time
        try:
            return _time
        finally:
            _time += 1

    console = Console(
        file=io.StringIO(),
        force_terminal=True,
        color_system="truecolor",
        width=80,
        legacy_windows=False,
    )
    progress = Progress(console=console, get_time=fake_time, auto_refresh=False)
    task1 = progress.add_task("foo")
    task2 = progress.add_task("bar", total=30)
    progress.advance(task2, 16)
    task3 = progress.add_task("baz", visible=False)
    task4 = progress.add_task("egg")
    progress.remove_task(task4)
    task4 = progress.add_task("foo2", completed=50, start=False)
    progress.stop_task(task4)
    progress.start_task(task4)
    progress.update(
        task4, total=200, advance=50, completed=200, visible=True, refresh=True
    )
    progress.stop_task(task4)
    return progress


def render_progress() -> str:
    progress = make_progress()
    progress.start()  # superfluous noop
    with progress:
        pass
    progress.stop()  # superfluous noop
    progress_render = progress.console.file.getvalue()
    return progress_render


def test_expand_bar() -> None:
    console = Console(
        file=io.StringIO(),
        force_terminal=True,
        width=10,
        color_system="truecolor",
        legacy_windows=False,
    )
    progress = Progress(
        BarColumn(bar_width=None),
        console=console,
        get_time=lambda: 1.0,
        auto_refresh=False,
    )
    progress.add_task("foo")
    with progress:
        pass
    expected = "\x1b[?25l\x1b[38;5;237m━━━━━━━━━━\x1b[0m\r\x1b[2K\x1b[38;5;237m━━━━━━━━━━\x1b[0m\n\x1b[?25h"
    render_result = console.file.getvalue()
    print("RESULT\n", repr(render_result))
    print("EXPECTED\n", repr(expected))
    assert render_result == expected


def test_render() -> None:
    expected = "\x1b[?25lfoo  \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m  0%\x1b[0m \x1b[36m-:--:--\x1b[0m\nbar  \x1b[38;2;249;38;114m━━━━━━━━━━━━━━━━━━━━━\x1b[0m\x1b[38;5;237m╺\x1b[0m\x1b[38;5;237m━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m 53%\x1b[0m \x1b[36m-:--:--\x1b[0m\nfoo2 \x1b[38;2;114;156;31m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m100%\x1b[0m \x1b[36m0:00:00\x1b[0m\r\x1b[2K\x1b[1A\x1b[2K\x1b[1A\x1b[2Kfoo  \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m  0%\x1b[0m \x1b[36m-:--:--\x1b[0m\nbar  \x1b[38;2;249;38;114m━━━━━━━━━━━━━━━━━━━━━\x1b[0m\x1b[38;5;237m╺\x1b[0m\x1b[38;5;237m━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m 53%\x1b[0m \x1b[36m-:--:--\x1b[0m\nfoo2 \x1b[38;2;114;156;31m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m100%\x1b[0m \x1b[36m0:00:00\x1b[0m\n\x1b[?25h"
    render_result = render_progress()
    print(repr(render_result))
    assert render_result == expected


def test_track() -> None:

    console = Console(
        file=io.StringIO(),
        force_terminal=True,
        width=60,
        color_system="truecolor",
        legacy_windows=False,
    )
    test = ["foo", "bar", "baz"]
    expected_values = iter(test)
    for value in track(
        test, "test", console=console, auto_refresh=False, get_time=MockClock(auto=True)
    ):
        assert value == next(expected_values)
    result = console.file.getvalue()
    print(repr(result))
    expected = "\x1b[?25l\r\x1b[2Ktest \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m  0%\x1b[0m \x1b[36m-:--:--\x1b[0m\r\x1b[2Ktest \x1b[38;2;249;38;114m━━━━━━━━━━━━━\x1b[0m\x1b[38;5;237m╺\x1b[0m\x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m 33%\x1b[0m \x1b[36m-:--:--\x1b[0m\r\x1b[2Ktest \x1b[38;2;249;38;114m━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m\x1b[38;2;249;38;114m╸\x1b[0m\x1b[38;5;237m━━━━━━━━━━━━━\x1b[0m \x1b[35m 67%\x1b[0m \x1b[36m0:00:06\x1b[0m\r\x1b[2Ktest \x1b[38;2;114;156;31m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m100%\x1b[0m \x1b[36m0:00:00\x1b[0m\r\x1b[2Ktest \x1b[38;2;114;156;31m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m100%\x1b[0m \x1b[36m0:00:00\x1b[0m\n\x1b[?25h"
    print("--")
    print("RESULT:")
    print(result)
    print(repr(result))
    print("EXPECTED:")
    print(expected)
    print(repr(expected))

    assert result == expected

    with pytest.raises(ValueError):
        for n in track(5):
            pass


def test_progress_track() -> None:
    console = Console(
        file=io.StringIO(),
        force_terminal=True,
        width=60,
        color_system="truecolor",
        legacy_windows=False,
    )
    progress = Progress(
        console=console, auto_refresh=False, get_time=MockClock(auto=True)
    )
    test = ["foo", "bar", "baz"]
    expected_values = iter(test)
    with progress:
        for value in progress.track(test, description="test"):
            assert value == next(expected_values)
    result = console.file.getvalue()
    print(repr(result))
    expected = "\x1b[?25l\r\x1b[2Ktest \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m  0%\x1b[0m \x1b[36m-:--:--\x1b[0m\r\x1b[2Ktest \x1b[38;2;249;38;114m━━━━━━━━━━━━━\x1b[0m\x1b[38;5;237m╺\x1b[0m\x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m 33%\x1b[0m \x1b[36m-:--:--\x1b[0m\r\x1b[2Ktest \x1b[38;2;249;38;114m━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m\x1b[38;2;249;38;114m╸\x1b[0m\x1b[38;5;237m━━━━━━━━━━━━━\x1b[0m \x1b[35m 67%\x1b[0m \x1b[36m0:00:06\x1b[0m\r\x1b[2Ktest \x1b[38;2;114;156;31m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m100%\x1b[0m \x1b[36m0:00:00\x1b[0m\r\x1b[2Ktest \x1b[38;2;114;156;31m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m100%\x1b[0m \x1b[36m0:00:00\x1b[0m\n\x1b[?25h"

    print(expected)
    print(repr(expected))
    print(result)
    print(repr(result))

    assert result == expected

    with pytest.raises(ValueError):
        for n in progress.track(5):
            pass


def test_columns() -> None:

    console = Console(
        file=io.StringIO(),
        force_terminal=True,
        width=80,
        log_time_format="[TIME]",
        color_system="truecolor",
        legacy_windows=False,
        log_path=False,
    )
    progress = Progress(
        "test",
        TextColumn("{task.description}"),
        BarColumn(bar_width=None),
        TimeRemainingColumn(),
        TimeElapsedColumn(),
        FileSizeColumn(),
        TotalFileSizeColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        transient=True,
        console=console,
        auto_refresh=False,
        get_time=MockClock(),
    )
    task1 = progress.add_task("foo", total=10)
    task2 = progress.add_task("bar", total=7)
    with progress:
        for n in range(4):
            progress.advance(task1, 3)
            progress.advance(task2, 4)
        print("foo")
        console.log("hello")
        console.print("world")
        progress.refresh()
    from .render import replace_link_ids

    result = replace_link_ids(console.file.getvalue())
    print(repr(result))
    expected = "\x1b[?25ltest foo \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[36m-:--:--\x1b[0m \x1b[33m0:00:37\x1b[0m \x1b[32m0 bytes\x1b[0m \x1b[32m10 bytes\x1b[0m \x1b[32m0/10 bytes\x1b[0m \x1b[31m?\x1b[0m\ntest bar \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[36m-:--:--\x1b[0m \x1b[33m0:00:36\x1b[0m \x1b[32m0 bytes\x1b[0m \x1b[32m7 bytes \x1b[0m \x1b[32m0/7 bytes \x1b[0m \x1b[31m?\x1b[0m\r\x1b[2K\x1b[1A\x1b[2Kfoo\ntest foo \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[36m-:--:--\x1b[0m \x1b[33m0:00:37\x1b[0m \x1b[32m0 bytes\x1b[0m \x1b[32m10 bytes\x1b[0m \x1b[32m0/10 bytes\x1b[0m \x1b[31m?\x1b[0m\ntest bar \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[36m-:--:--\x1b[0m \x1b[33m0:00:36\x1b[0m \x1b[32m0 bytes\x1b[0m \x1b[32m7 bytes \x1b[0m \x1b[32m0/7 bytes \x1b[0m \x1b[31m?\x1b[0m\r\x1b[2K\x1b[1A\x1b[2K\x1b[2;36m[TIME]\x1b[0m\x1b[2;36m \x1b[0mhello                                                                    \ntest foo \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[36m-:--:--\x1b[0m \x1b[33m0:00:37\x1b[0m \x1b[32m0 bytes\x1b[0m \x1b[32m10 bytes\x1b[0m \x1b[32m0/10 bytes\x1b[0m \x1b[31m?\x1b[0m\ntest bar \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[36m-:--:--\x1b[0m \x1b[33m0:00:36\x1b[0m \x1b[32m0 bytes\x1b[0m \x1b[32m7 bytes \x1b[0m \x1b[32m0/7 bytes \x1b[0m \x1b[31m?\x1b[0m\r\x1b[2K\x1b[1A\x1b[2Kworld\ntest foo \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[36m-:--:--\x1b[0m \x1b[33m0:00:37\x1b[0m \x1b[32m0 bytes\x1b[0m \x1b[32m10 bytes\x1b[0m \x1b[32m0/10 bytes\x1b[0m \x1b[31m?\x1b[0m\ntest bar \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[36m-:--:--\x1b[0m \x1b[33m0:00:36\x1b[0m \x1b[32m0 bytes\x1b[0m \x1b[32m7 bytes \x1b[0m \x1b[32m0/7 bytes \x1b[0m \x1b[31m?\x1b[0m\r\x1b[2K\x1b[1A\x1b[2Ktest foo \x1b[38;2;114;156;31m━━━━━━━━━━━━━━━━\x1b[0m \x1b[36m0:00:00\x1b[0m \x1b[33m0:01:00\x1b[0m \x1b[32m12 bytes\x1b[0m \x1b[32m10 bytes\x1b[0m \x1b[32m12/10 bytes\x1b[0m \x1b[31m1 byte/s\x1b[0m\ntest bar \x1b[38;2;114;156;31m━━━━━━━━━━━━━━━━\x1b[0m \x1b[36m0:00:00\x1b[0m \x1b[33m0:00:45\x1b[0m \x1b[32m16 bytes\x1b[0m \x1b[32m7 bytes \x1b[0m \x1b[32m16/7 bytes \x1b[0m \x1b[31m1 byte/s\x1b[0m\r\x1b[2K\x1b[1A\x1b[2Ktest foo \x1b[38;2;114;156;31m━━━━━━━━━━━━━━━━\x1b[0m \x1b[36m0:00:00\x1b[0m \x1b[33m0:01:00\x1b[0m \x1b[32m12 bytes\x1b[0m \x1b[32m10 bytes\x1b[0m \x1b[32m12/10 bytes\x1b[0m \x1b[31m1 byte/s\x1b[0m\ntest bar \x1b[38;2;114;156;31m━━━━━━━━━━━━━━━━\x1b[0m \x1b[36m0:00:00\x1b[0m \x1b[33m0:00:45\x1b[0m \x1b[32m16 bytes\x1b[0m \x1b[32m7 bytes \x1b[0m \x1b[32m16/7 bytes \x1b[0m \x1b[31m1 byte/s\x1b[0m\n\x1b[?25h\r\x1b[1A\x1b[2K\x1b[1A\x1b[2K"
    assert result == expected


def test_task_create() -> None:
    task = Task(TaskID(1), "foo", 100, 0, _get_time=lambda: 1)
    assert task.elapsed is None
    assert not task.finished
    assert task.percentage == 0.0
    assert task.speed is None
    assert task.time_remaining is None


def test_task_start() -> None:
    current_time = 1

    def get_time():
        nonlocal current_time
        return current_time

    task = Task(TaskID(1), "foo", 100, 0, _get_time=get_time)
    task.start_time = get_time()
    assert task.started == True
    assert task.elapsed == 0
    current_time += 1
    assert task.elapsed == 1
    current_time += 1
    task.stop_time = get_time()
    current_time += 1
    assert task.elapsed == 2


def test_task_zero_total() -> None:
    task = Task(TaskID(1), "foo", 0, 0, _get_time=lambda: 1)
    assert task.percentage == 0


def test_progress_create() -> None:
    progress = Progress()
    assert progress.finished
    assert progress.tasks == []
    assert progress.task_ids == []


def test_track_thread() -> None:
    progress = Progress()
    task_id = progress.add_task("foo")
    track_thread = _TrackThread(progress, task_id, 0.1)
    assert track_thread.completed == 0
    from time import sleep

    with track_thread:
        track_thread.completed = 1
        sleep(0.3)
        assert progress.tasks[task_id].completed >= 1
        track_thread.completed += 1


def test_reset() -> None:
    progress = Progress()
    task_id = progress.add_task("foo")
    progress.advance(task_id, 1)
    progress.advance(task_id, 1)
    progress.advance(task_id, 1)
    progress.advance(task_id, 7)
    task = progress.tasks[task_id]
    assert task.completed == 10
    progress.reset(
        task_id,
        total=200,
        completed=20,
        visible=False,
        description="bar",
        example="egg",
    )
    assert task.total == 200
    assert task.completed == 20
    assert task.visible == False
    assert task.description == "bar"
    assert task.fields == {"example": "egg"}
    assert not task._progress


def test_progress_max_refresh() -> None:
    """Test max_refresh argment."""
    time = 0.0

    def get_time() -> float:
        nonlocal time
        try:
            return time
        finally:
            time = time + 1.0

    console = Console(
        color_system=None, width=80, legacy_windows=False, force_terminal=True
    )
    column = TextColumn("{task.description}")
    column.max_refresh = 3
    progress = Progress(
        column,
        get_time=get_time,
        auto_refresh=False,
        console=console,
    )
    console.begin_capture()
    with progress:
        task_id = progress.add_task("start")
        for tick in range(6):
            progress.update(task_id, description=f"tick {tick}")
            progress.refresh()
    result = console.end_capture()
    print(repr(result))
    assert (
        result
        == "\x1b[?25l\r\x1b[2Kstart\r\x1b[2Kstart\r\x1b[2Ktick 1\r\x1b[2Ktick 1\r\x1b[2Ktick 3\r\x1b[2Ktick 3\r\x1b[2Ktick 5\r\x1b[2Ktick 5\n\x1b[?25h"
    )


if __name__ == "__main__":
    _render = render_progress()
    print(_render)
    print(repr(_render))
