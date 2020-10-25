import io
import os
import sys

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
    if os.getenv("CAPTURE") is not None:  # adjust the correct output check
        set_capture_text("live", output_file, output=output)

    correct_output = get_capture_text("live", output_file)

    assert output.replace("\r", "") == correct_output.replace(
        "\r", ""
    ), "Console output differs from the correct output"


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
    console = create_capture_console()
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
