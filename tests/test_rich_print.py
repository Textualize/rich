import io
import sys

import rich
from rich.console import Console


def test_rich_print():
    output = io.StringIO()

    assert rich._console is None
    backup_file = sys.stdout
    try:
        sys.stdout = output
        rich.print("foo")
        assert isinstance(rich._console, Console)
        assert output.getvalue() == "foo\n"
    finally:
        sys.stdout = backup_file
