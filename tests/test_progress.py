import io
from time import time

from rich.console import Console
from rich.progress import BarColumn, Progress, Task, TimeRemainingColumn
from rich.bar import Bar


def test_bar_columns():
    bar_column = BarColumn(100)
    assert bar_column.bar_width == 100
    task = Task(1, "test", 100, 20)
    bar = bar_column(task)
    assert isinstance(bar, Bar)
    assert bar.completed == 20
    assert bar.total == 100


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


def test_render() -> None:
    expected = "foo \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m  0%\x1b[0m \x1b[36m-:--:--\x1b[0m \rfoo \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m  0%\x1b[0m \x1b[36m-:--:--\x1b[0m \nbar \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m  0%\x1b[0m \x1b[36m-:--:--\x1b[0m \r\x1b[1Afoo \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m  0%\x1b[0m \x1b[36m-:--:--\x1b[0m \nbar \x1b[38;5;13m━━━━━━\x1b[0m\x1b[38;5;237m╺\x1b[0m\x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m 16%\x1b[0m \x1b[36m-:--:--\x1b[0m \r\x1b[1Afoo \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m  0%\x1b[0m \x1b[36m-:--:--\x1b[0m \nbar \x1b[38;5;13m━━━━━━\x1b[0m\x1b[38;5;237m╺\x1b[0m\x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m 16%\x1b[0m \x1b[36m-:--:--\x1b[0m \negg \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m  0%\x1b[0m \x1b[36m-:--:--\x1b[0m \r\x1b[2Afoo  \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m  0%\x1b[0m \x1b[36m-:--:--\x1b[0m \nbar  \x1b[38;5;13m━━━━━━\x1b[0m\x1b[38;5;237m╺\x1b[0m\x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m 16%\x1b[0m \x1b[36m-:--:--\x1b[0m \nfoo2 \x1b[38;5;13m━━━━━━━━━━━━━━━━━━━━\x1b[0m\x1b[38;5;237m╺\x1b[0m\x1b[38;5;237m━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m 50%\x1b[0m \x1b[36m-:--:--\x1b[0m \r\x1b[2Afoo  \x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m  0%\x1b[0m \x1b[36m-:--:--\x1b[0m \nbar  \x1b[38;5;13m━━━━━━\x1b[0m\x1b[38;5;237m╺\x1b[0m\x1b[38;5;237m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m 16%\x1b[0m \x1b[36m-:--:--\x1b[0m \nfoo2 \x1b[38;5;10m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m \x1b[35m100%\x1b[0m \x1b[36m0:00:00\x1b[0m "
    assert render_progress() == expected


if __name__ == "__main__":
    _render = render_progress()
    print(_render)
    print(repr(_render))
