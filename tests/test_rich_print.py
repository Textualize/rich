import io
import sys

import rich
from rich.console import Console


def test_get_console():
    console = rich.get_console()
    assert isinstance(console, Console)


def test_rich_print():
    console = rich.get_console()
    output = io.StringIO()
    backup_file = console.file
    try:
        console.file = output
        rich.print("foo")
        assert output.getvalue() == "foo\n"
    finally:
        console.file = backup_file
