import io
from time import time

import pytest

from rich.bar import Bar
from rich.console import Console
from rich.highlighter import NullHighlighter
from rich.progress import (
    BarColumn,
    FileSizeColumn,
    TotalFileSizeColumn,
    DownloadColumn,
    TransferSpeedColumn,
    Progress,
    Task,
    TextColumn,
    TimeRemainingColumn,
    track,
)
from rich.text import Text


def test_bar_columns():
    bar_column = BarColumn(100)
    assert bar_column.bar_width == 100
    task = Task(1, "test", 100, 20)
    bar = bar_column(task)
    assert isinstance(bar, Bar)
    assert bar.completed == 20
    assert bar.total == 100


def test_text_column():
    text_column = TextColumn("[b]foo", highlighter=NullHighlighter())
    task = Task(1, "test", 100, 20)
    text = text_column.render(task)
    assert str(text) == "foo"

    text_column = TextColumn("[b]bar", markup=False)
    task = Task(1, "test", 100, 20)
    text = text_column.render(task)
    assert text == Text("[b]bar")


def test_time_remaining_column():
    class FakeTask(Task):
        time_remaining = 60

    column = TimeRemainingColumn()
    task = Task(1, "test", 100, 20)
    text = column(task)
    assert str(text) == "-:--:--"

    text = column(FakeTask(1, "test", 100, 20))
    assert str(text) == "0:01:00"


def test_task_ids():
    progress = make_progress()
    assert progress.task_ids == [0, 1, 2, 4]


def test_finished():
    progress = make_progress()
    assert not progress.finished


def make_progress() -> Progress:
    console = Console(file=io.StringIO(), force_terminal=True)
    progress = Progress(console=console)
    task1 = progress.add_task("foo")
    task2 = progress.add_task("bar", 30)
    progress.advance(task2, 16)
    task3 = progress.add_task("baz", visible=False)
    task4 = progress.add_task("egg")
    progress.remove_task(task4)
    task4 = progress.add_task("foo2", completed=50, start=False)
    progress.start_task(task4)
    progress.update(
        task4, total=200, advance=50, completed=200, visible=True, refresh=True
    )
    return progress


def render_progress() -> str:
    progress = make_progress()
    progress_render = progress.console.file.getvalue()
    return progress_render


def test_expand_bar() -> None:
    console = Console(file=io.StringIO(), force_terminal=True, width=10)
    progress = Progress(BarColumn(bar_width=None), console=console)
    progress.add_task("foo")
    progress.refresh()
    expected = "\x1b[38;5;237m━━━━━━━━━\x1b[0m \r\x1b[2K\x1b[38;5;237m━━━━━━━━━\x1b[0m "
    assert console.file.getvalue() == expected


def test_render() -> None:
    expected = "foo \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m  0%\x1b[0m \x1b[36m-:--:--\x1b[0m \r\x1b[2Kfoo \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m  0%\x1b[0m \x1b[36m-:--:--\x1b[0m \nbar \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m  0%\x1b[0m \x1b[36m-:--:--\x1b[0m \r\x1b[1A\x1b[2Kfoo \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m  0%\x1b[0m \x1b[36m-:--:--\x1b[0m \nbar \x1b[38;5;13m━━━━━━\x1b[0m\x1b[38;5;237m╺\x1b[0m\x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m 16%\x1b[0m \x1b[36m-:--:--\x1b[0m \r\x1b[1A\x1b[2Kfoo \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m  0%\x1b[0m \x1b[36m-:--:--\x1b[0m \nbar \x1b[38;5;13m━━━━━━\x1b[0m\x1b[38;5;237m╺\x1b[0m\x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m 16%\x1b[0m \x1b[36m-:--:--\x1b[0m \negg \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m  0%\x1b[0m \x1b[36m-:--:--\x1b[0m \r\x1b[2A\x1b[2Kfoo  \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m  0%\x1b[0m \x1b[36m-:--:--\x1b[0m \nbar  \x1b[38;5;13m━━━━━━\x1b[0m\x1b[38;5;237m╺\x1b[0m\x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m 16%\x1b[0m \x1b[36m-:--:--\x1b[0m \nfoo2 \x1b[38;5;13m━━━━━━━━━━━━━━━━━━━━\x1b[0m\x1b[38;5;237m╺\x1b[0m\x1b[38;5;237m━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m 50%\x1b[0m \x1b[36m-:--:--\x1b[0m \r\x1b[2A\x1b[2Kfoo  \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m  0%\x1b[0m \x1b[36m-:--:--\x1b[0m \nbar  \x1b[38;5;13m━━━━━━\x1b[0m\x1b[38;5;237m╺\x1b[0m\x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m 16%\x1b[0m \x1b[36m-:--:--\x1b[0m \nfoo2 \x1b[38;5;10m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m100%\x1b[0m \x1b[36m0:00:00\x1b[0m "
    assert render_progress() == expected


def test_track() -> None:
    console = Console(file=io.StringIO(), force_terminal=True, width=40)
    test = ["foo", "bar", "baz"]
    expected_values = iter(test)
    for value in track(test, "test", console=console, auto_refresh=False):
        assert value == next(expected_values)
    result = console.file.getvalue()
    expected = "test \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m  0%\x1b[0m \x1b[36m-:--:--\x1b[0m \x1b[?25l\r\x1b[2Ktest \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m  0%\x1b[0m \x1b[36m-:--:--\x1b[0m \r\x1b[2Ktest \x1b[38;5;13m━━━━━━━\x1b[0m\x1b[38;5;237m╺\x1b[0m\x1b[38;5;237m━━━━━━━━━━━━━\x1b[0m \x1b[35m 33%\x1b[0m \x1b[36m-:--:--\x1b[0m \r\x1b[2Ktest \x1b[38;5;13m━━━━━━━━━━━━━━\x1b[0m\x1b[38;5;237m╺\x1b[0m\x1b[38;5;237m━━━━━━\x1b[0m \x1b[35m 67%\x1b[0m \x1b[36m0:00:01\x1b[0m \r\x1b[2Ktest \x1b[38;5;10m━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m100%\x1b[0m \x1b[36m0:00:00\x1b[0m \r\x1b[2Ktest \x1b[38;5;10m━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m100%\x1b[0m \x1b[36m0:00:00\x1b[0m \n\x1b[?25h"
    assert result == expected

    with pytest.raises(ValueError):
        for n in track(5):
            pass


def test_columns() -> None:
    time = 1.0

    def get_time():
        nonlocal time
        time += 1.0
        return time

    console = Console(
        file=io.StringIO(), force_terminal=True, width=80, log_time_format="[TIME]"
    )
    progress = Progress(
        "test",
        TextColumn("{task.description}"),
        BarColumn(bar_width=None),
        TimeRemainingColumn(),
        FileSizeColumn(),
        TotalFileSizeColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        console=console,
        auto_refresh=False,
        get_time=get_time,
    )
    task1 = progress.add_task("foo", total=10)
    task2 = progress.add_task("bar", total=7)
    with progress:
        for n in range(4):
            progress.advance(task1, 3)
            progress.advance(task2, 4)
        progress.log("hello")
        progress.print("world")
        progress.refresh()
    result = console.file.getvalue()
    expected = "test foo \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[36m-:--:--\x1b[0m \x1b[32m0 bytes\x1b[0m \x1b[32m10 bytes\x1b[0m \x1b[32m0/10 bytes\x1b[0m \x1b[31m?\x1b[0m \r\x1b[2Ktest foo \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[36m-:--:--\x1b[0m \x1b[32m0 bytes\x1b[0m \x1b[32m10 bytes\x1b[0m \x1b[32m0/10 bytes\x1b[0m \x1b[31m?\x1b[0m \ntest bar \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[36m-:--:--\x1b[0m \x1b[32m0 bytes\x1b[0m \x1b[32m7 bytes \x1b[0m \x1b[32m0/7 bytes \x1b[0m \x1b[31m?\x1b[0m \x1b[?25l\r\x1b[1A\x1b[2Ktest foo \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[36m-:--:--\x1b[0m \x1b[32m0 bytes\x1b[0m \x1b[32m10 bytes\x1b[0m \x1b[32m0/10 bytes\x1b[0m \x1b[31m?\x1b[0m \ntest bar \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[36m-:--:--\x1b[0m \x1b[32m0 bytes\x1b[0m \x1b[32m7 bytes \x1b[0m \x1b[32m0/7 bytes \x1b[0m \x1b[31m?\x1b[0m \r\x1b[1A\x1b[2K\x1b[2;36m[TIME]\x1b[0m\x1b[2;36m \x1b[0mhello                                               \x1b[2mtest_progress.py:151\x1b[0m\x1b[2m \x1b[0m\ntest foo \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[36m-:--:--\x1b[0m \x1b[32m0 bytes\x1b[0m \x1b[32m10 bytes\x1b[0m \x1b[32m0/10 bytes\x1b[0m \x1b[31m?\x1b[0m \ntest bar \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[36m-:--:--\x1b[0m \x1b[32m0 bytes\x1b[0m \x1b[32m7 bytes \x1b[0m \x1b[32m0/7 bytes \x1b[0m \x1b[31m?\x1b[0m \r\x1b[1A\x1b[2Kworld\ntest foo \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[36m-:--:--\x1b[0m \x1b[32m0 bytes\x1b[0m \x1b[32m10 bytes\x1b[0m \x1b[32m0/10 bytes\x1b[0m \x1b[31m?\x1b[0m \ntest bar \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[36m-:--:--\x1b[0m \x1b[32m0 bytes\x1b[0m \x1b[32m7 bytes \x1b[0m \x1b[32m0/7 bytes \x1b[0m \x1b[31m?\x1b[0m \r\x1b[1A\x1b[2Ktest foo \x1b[38;5;10m━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[36m0:00:00\x1b[0m \x1b[32m12 bytes\x1b[0m \x1b[32m10 bytes\x1b[0m \x1b[32m12/10 bytes\x1b[0m \x1b[31m1 byte/s \x1b[0m \ntest bar \x1b[38;5;10m━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[36m0:00:00\x1b[0m \x1b[32m16 bytes\x1b[0m \x1b[32m7 bytes \x1b[0m \x1b[32m16/7 bytes \x1b[0m \x1b[31m2 bytes/s\x1b[0m \r\x1b[1A\x1b[2Ktest foo \x1b[38;5;10m━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[36m0:00:00\x1b[0m \x1b[32m12 bytes\x1b[0m \x1b[32m10 bytes\x1b[0m \x1b[32m12/10 bytes\x1b[0m \x1b[31m1 byte/s \x1b[0m \ntest bar \x1b[38;5;10m━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[36m0:00:00\x1b[0m \x1b[32m16 bytes\x1b[0m \x1b[32m7 bytes \x1b[0m \x1b[32m16/7 bytes \x1b[0m \x1b[31m2 bytes/s\x1b[0m \n\x1b[?25h"
    assert result == expected


if __name__ == "__main__":
    _render = render_progress()
    print(_render)
    print(repr(_render))
