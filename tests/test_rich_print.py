import io

import rich
from rich.console import Console


def test_get_console():
    console = rich.get_console()
    assert isinstance(console, Console)


def test_reconfigure_console():
    rich.reconfigure(width=100)
    assert rich.get_console().width == 100


def test_rich_print():
    console = rich.get_console()
    output = io.StringIO()
    backup_file = console.file
    try:
        console.file = output
        rich.print("foo", "bar")
        rich.print("foo\n")
        rich.print("foo\n\n")
        assert output.getvalue() == "foo bar\nfoo\n\nfoo\n\n\n"
    finally:
        console.file = backup_file


def test_rich_print_X():
    console = rich.get_console()
    output = io.StringIO()
    backup_file = console.file
    try:
        console.file = output
        rich.print("foo")
        rich.print("fooX")
        rich.print("fooXX")
        assert output.getvalue() == "foo\nfooX\nfooXX\n"
    finally:
        console.file = backup_file
