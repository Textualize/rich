# encoding=utf-8
from rich.measure import Measurement
from rich.console import Console
from rich.table import Table, Column
from rich.style import Style
from rich.rule import Rule
from rich import box, errors
from rich.text import Text
from textwrap import dedent

import pytest
import io


def render_tables_with_header_attrs():
    table = Table(
        title="Star Wars Movies", caption="Rich example table", caption_justify="right"
    )

    table.add_column("Released", header_style="bright_cyan", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Box Office", justify="right", style="green")

    table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")
    table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
    table.add_row("Dec 15, 2017", "Star Wars Ep. V111: The Last Jedi", "$1,332,539,889")
    table.add_row("Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889")

    console = Console(width=32, file=io.StringIO(), legacy_windows=False, _environ={})
    console.print(table, justify="center")
    return console.file.getvalue()


def test_table_from_dict_with_header_attrs():
    t = Table(
        title="Star Wars Movies", caption="Rich example table", caption_justify="right"
    )
    data = [
        {
            "Released": "Dec 20, 2019",
            "Title": "Star Wars: The Rise of Skywalker",
            "Box Office": "$952,110,690",
        },
        {
            "Released": "May 25, 2018",
            "Title": "Solo: A Star Wars Story",
            "Box Office": "$393,151,347",
        },
        {
            "Released": "Dec 15, 2017",
            "Title": "Star Wars Ep. V111: The Last Jedi",
            "Box Office": "$1,332,539,889",
        },
        {
            "Released": "Dec 16, 2016",
            "Title": "Rogue One: A Star Wars Story",
            "Box Office": "$1,332,439,889",
        },
    ]

    header_attrs = [
        {"header_style": "bright_cyan", "style": "cyan", "no_wrap": True},
        {"style": "magenta"},
        {"justify": "right", "style": "green"},
    ]

    t.from_dict(data, header_attrs=header_attrs)

    console = Console(width=32, file=io.StringIO(), legacy_windows=False, _environ={})
    console.print(t, justify="center")
    assert console.file.getvalue() == render_tables_with_header_attrs()


def test_rule_in_expanded_table_using_from_table():
    console = Console(width=32, file=io.StringIO(), legacy_windows=False, _environ={})
    table = Table(box=box.ASCII, expand=True, show_header=False)
    data = [
        {"HEADER 1": "COL1", "HEADER 2": "COL2"},
        {"HEADER 1": "COL1", "HEADER 2": Rule(style=None)},
        {"HEADER 1": "COL1", "HEADER 2": "COL2"},
    ]
    table.from_dict(data)
    # table.add_row("COL1", "COL2")
    # table.add_row("COL1", Rule(style=None))
    # table.add_row("COL1", "COL2")
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


def test_init_append_column():
    header_names = ["header1", "header2", "header3"]
    test_columns = [
        Column(_index=index, header=header) for index, header in enumerate(header_names)
    ]

    # Test by specifing headers as column instances with populated dictionary
    t = Table()
    t.from_dict([{"header1": "", "header2": "", "header3": ""}], headers=test_columns)
    assert Table(*test_columns).columns == t.columns

    # Test by specifing headers as list of strings
    t = Table()
    t.from_dict(
        [{"header1": None, "header2": None, "header3": None}],
        headers=header_names,
    )
    assert Table(*test_columns).columns == t.columns

    # Test with missing data values
    t = Table()
    t.from_dict([{"header1": ""}], headers=test_columns)
    assert Table(*test_columns).columns == t.columns

    # test with no data values
    t = Table()
    t.from_dict([{}], headers=test_columns, fillvalue="")
    assert Table(*test_columns).columns == t.columns


def data():
    return [
        {
            "Released": "Dec 20, 2019",
            "Title": "Star Wars: The Rise of Skywalker",
            "Box Office": "$952,110,690",
        },
        {
            "Released": "May 25, 2018",
            "Title": "Solo: A Star Wars Story",
            "Box Office": "$393,151,347",
        },
        {
            "Released": "Dec 15, 2017",
            "Title": "Star Wars Ep. V111: The Last Jedi",
            "Box Office": "$1,332,539,889",
        },
        {
            "Released": "Dec 16, 2016",
            "Title": "Rogue One: A Star Wars Story",
            "Box Office": "$1,332,439,889",
        },
    ]


def test_table_with_excess_header_attrs():
    d = data()
    t = Table(title="Star Wars Movies")
    header_attrs = [
        {"header_style": "bright_cyan", "style": "cyan", "no_wrap": True},
        {"style": "magenta"},
        {"justify": "right", "style": "green"},
        {"style": "red", "vertical": "top"},  # extra attribute
    ]

    # test exception for more header attrs than headers
    with pytest.raises(ValueError):
        t.from_dict(d, header_attrs=header_attrs)


def test_table_with_excess_row_attrs():
    d = data()
    t = Table(title="Star wars Movies")
    row_attrs = (None, None, None, {"style": "white on blue"}, None)
    with pytest.raises(ValueError):
        t.from_dict(d, row_attrs=row_attrs)
