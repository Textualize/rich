import io
import os
import random
import sys
import time
from typing import List

import pytest
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.text import Text

from tests.util import get_capture_text, set_capture_text


def create_capture_console(*, width: int = 60, height: int = 80) -> Console:
    return Console(
        width=width,
        height=height,
        file=io.StringIO(),
        force_terminal=True,
        legacy_windows=False,
        color_system=None,
    )


def create_base_table() -> Table:
    table = Table(title="test table", caption="table caption", expand=True)
    table.add_column("foo", footer=Text("total"), no_wrap=True, overflow="ellipsis")
    table.add_column("bar", justify="center")
    table.add_column("baz", justify="right")

    return table


def check_output(output_file: str, output: str) -> None:
    output = output.replace("\r", "")
    if os.getenv("CAPTURE") is not None:  # adjust the correct output check
        set_capture_text("live", output_file, output=output)

    correct_output = get_capture_text("live", output_file).replace("\r", "")

    if os.getenv("VERBOSE") is not None:
        print("Current Output\n", output)
        print("Correct Output\n", correct_output)

    assert output == correct_output, "Console output differs from the correct output"


def test_live_state() -> None:

    with Live("") as live:
        assert live.is_started
        live.start()

        assert live.item == ""

        assert live.is_started
        live.stop()
        assert not live.is_started

    assert not live.is_started


@pytest.mark.skipif(sys.version_info < (3, 7), reason="requires python3.7 or higher")
def test_growing_table() -> None:
    """Test generating a table and adding more rows of data. No auto-refresh"""
    console = create_capture_console()
    table = create_base_table()

    with console.capture() as capture, Live(
        table, console=console, auto_refresh=False
    ) as live:
        for step in range(20):
            table.add_row(f"{step}", f"{step}", f"{step}")
            live.refresh()
    output = capture.get()
    check_output("growing_table.txt", output=output)


@pytest.mark.skipif(sys.version_info < (3, 7), reason="requires python3.7 or higher")
def test_growing_table_transient() -> None:
    """Test generating a table and adding more rows of data. Delete data at then end. No auto-refresh."""
    console = create_capture_console()
    table = create_base_table()

    with console.capture() as capture, Live(
        table, console=console, auto_refresh=False, transient=True
    ) as live:
        for step in range(20):
            table.add_row(f"{step}", f"{step}", f"{step}")
            live.refresh()

    output = capture.get()
    check_output("growing_table_transient.txt", output=output)


@pytest.mark.skipif(sys.version_info < (3, 7), reason="requires python3.7 or higher")
def test_growing_table_overflow() -> None:
    """Test generating a table and adding more rows of data. No auto-refresh"""
    console = create_capture_console(height=20)
    table = create_base_table()

    with console.capture() as capture, Live(
        table, console=console, auto_refresh=False
    ) as live:
        for step in range(20):
            table.add_row(f"{step}", f"{step}", f"{step}")
            live.refresh()
    output = capture.get()
    check_output("growing_table_overflow.txt", output=output)


@pytest.mark.skipif(sys.version_info < (3, 7), reason="requires python3.7 or higher")
def test_growing_table_autorefresh() -> None:
    """Test generating a table but using auto-refresh from threading"""
    console = create_capture_console()
    table = create_base_table()

    with console.capture() as capture, Live(table, console=console):
        for step in range(20):
            table.add_row(f"{step}", f"{step}", f"{step}")
            time.sleep(0.2)
    output = capture.get()
    check_output("growing_table_autorefresh.txt", output=output)


@pytest.mark.skipif(sys.version_info < (3, 7), reason="requires python3.7 or higher")
def test_growing_table_logging() -> None:
    """Test generating a table but also add in console logging."""
    console = create_capture_console()
    table = create_base_table()

    with console.capture() as capture, Live(table, console=console):
        for step in range(20):
            console.print(f"Attempting Step #{step}")
            table.add_row(f"{step}", f"{step}", f"{step}")
    output = capture.get()
    check_output("growing_table_logging.txt", output=output)


@pytest.mark.skipif(sys.version_info < (3, 7), reason="requires python3.7 or higher")
def test_growing_table_large() -> None:
    """Test generating a table but also add in console logging."""
    console = create_capture_console(height=1_000)
    table = create_base_table()

    with console.capture() as capture, Live(
        table, console=console, auto_refresh=False
    ) as live:
        for step in range(100):
            console.print(f"Attempting Step #{step}")
            table.add_row(f"{step}", f"{step}", f"{step}")
            if step % 20 == 0:
                live.refresh()
    output = capture.get()
    check_output("growing_table_large.txt", output=output)


@pytest.mark.skipif(sys.version_info < (3, 7), reason="requires python3.7 or higher")
def test_growing_table_large_overflow() -> None:
    """Test generating a table but also add in console logging."""
    console = create_capture_console()
    table = create_base_table()

    with console.capture() as capture, Live(
        table, console=console, auto_refresh=False
    ) as live:
        for step in range(100):
            console.print(f"Attempting Step #{step}")
            table.add_row(f"{step}", f"{step}", f"{step}")
            if step % 20 == 0:
                live.refresh()
    output = capture.get()
    check_output("growing_table_large_overflow.txt", output=output)


def generate_random_data_table() -> Table:
    Data = List[List[int]]

    def generate_data() -> Data:
        rows = random.randint(0, 20)
        return [
            [random.randint(0, 20) for _ in range(rows)]
            for _ in range(random.randint(0, 20))
        ]

    table = Table()
    for data_row in generate_data():
        table.add_row(*[hex(data_cell) for data_cell in data_row])

    return table


@pytest.mark.skipif(sys.version_info < (3, 7), reason="requires python3.7 or higher")
def test_random_data_table() -> None:
    """Test generating a data table whose height fluctuates."""
    console = create_capture_console()
    random.seed(123)  # seed so that it always provides same values
    with console.capture() as capture, Live(
        console=console, auto_refresh=False
    ) as live:
        for _ in range(100):
            table = generate_random_data_table()
            live.update(table, refresh=True)

    output = capture.get()
    check_output("random_data_table.txt", output=output)


@pytest.mark.skipif(sys.version_info < (3, 7), reason="requires python3.7 or higher")
def test_random_data_table_overflow() -> None:
    """Test generating a data table whose height fluctuates."""
    console = create_capture_console(height=20)
    random.seed(123)  # seed so that it always provides same values
    with console.capture() as capture, Live(
        console=console, auto_refresh=False
    ) as live:
        for _ in range(100):
            table = generate_random_data_table()
            live.update(table, refresh=True)

    output = capture.get()
    check_output("random_data_table_overflow.txt", output=output)


@pytest.mark.skipif(sys.version_info < (3, 7), reason="requires python3.7 or higher")
def test_random_data_table_logging() -> None:
    """Test generating a data table whose height fluctuates."""
    console = create_capture_console()
    random.seed(123)  # seed so that it always provides same values
    with console.capture() as capture, Live(
        console=console, auto_refresh=False
    ) as live:
        for step in range(100):
            console.print(f"Step {step} start")
            table = generate_random_data_table()
            live.update(table, refresh=True)
            print(f"Step {step} end")  # test redirect of stdout

    output = capture.get()
    check_output("random_data_table_logging.txt", output=output)
