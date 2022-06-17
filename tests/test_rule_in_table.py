import io
from textwrap import dedent

import pytest

from rich import box
from rich.console import Console
from rich.rule import Rule
from rich.table import Table


@pytest.mark.parametrize("expand_kwarg", ({}, {"expand": False}))
def test_rule_in_unexpanded_table(expand_kwarg):
    console = Console(width=32, file=io.StringIO(), legacy_windows=False, _environ={})
    table = Table(box=box.ASCII, show_header=False, **expand_kwarg)
    table.add_column()
    table.add_column()
    table.add_row("COL1", "COL2")
    table.add_row("COL1", Rule())
    table.add_row("COL1", "COL2")
    console.print(table)
    expected = dedent(
        """\
        +-------------+
        | COL1 | COL2 |
        | COL1 | ──── |
        | COL1 | COL2 |
        +-------------+
        """
    )
    result = console.file.getvalue()
    assert result == expected


def test_rule_in_expanded_table():
    console = Console(width=32, file=io.StringIO(), legacy_windows=False, _environ={})
    table = Table(box=box.ASCII, expand=True, show_header=False)
    table.add_column()
    table.add_column()
    table.add_row("COL1", "COL2")
    table.add_row("COL1", Rule(style=None))
    table.add_row("COL1", "COL2")
    console.print(table)
    expected = dedent(
        """\
        +------------------------------+
        | COL1          | COL2         |
        | COL1          | ──────────── |
        | COL1          | COL2         |
        +------------------------------+
        """
    )
    result = console.file.getvalue()
    assert result == expected


def test_rule_in_ratio_table():
    console = Console(width=32, file=io.StringIO(), legacy_windows=False, _environ={})
    table = Table(box=box.ASCII, expand=True, show_header=False)
    table.add_column(ratio=1)
    table.add_column()
    table.add_row("COL1", "COL2")
    table.add_row("COL1", Rule(style=None))
    table.add_row("COL1", "COL2")
    console.print(table)
    expected = dedent(
        """\
        +------------------------------+
        | COL1                  | COL2 |
        | COL1                  | ──── |
        | COL1                  | COL2 |
        +------------------------------+
        """
    )
    result = console.file.getvalue()
    assert result == expected
