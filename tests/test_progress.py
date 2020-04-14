from time import time

from rich import progress
from rich.bar import Bar


def test_bar_columns():
    bar_column = progress.BarColumn(100)
    assert bar_column.bar_width == 100
    task = progress.Task(1, "test", 100, 20)
    bar = bar_column(task)
    assert isinstance(bar, Bar)
    assert bar.completed == 20
    assert bar.total == 100


def test_time_remaining_column():
    class FakeTask(progress.Task):
        time_remaining = 60

    column = progress.TimeRemainingColumn()
    task = progress.Task(1, "test", 100, 20)
    text = column(task)
    assert str(text) == "-:--:--"

    text = column(FakeTask(1, "test", 100, 20))
    assert str(text) == "0:01:00"
