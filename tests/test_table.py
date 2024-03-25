# encoding=utf-8

import io

import pytest

from rich import box, errors
from rich.console import Console
from rich.measure import Measurement
from rich.style import Style
from rich.table import Column, Table
from rich.text import Text


def render_tables():
    console = Console(
        width=60,
        force_terminal=True,
        file=io.StringIO(),
        legacy_windows=False,
        color_system=None,
        _environ={},
    )

    table = Table(title="test table", caption="table caption", expand=False)
    table.add_column("foo", footer=Text("total"), no_wrap=True, overflow="ellipsis")
    table.add_column("bar", justify="center")
    table.add_column("baz", justify="right")

    table.add_row("Averlongwordgoeshere", "banana pancakes", None)

    assert Measurement.get(console, console.options, table) == Measurement(41, 48)
    table.expand = True
    assert Measurement.get(console, console.options, table) == Measurement(41, 48)

    for width in range(10, 60, 5):
        console.print(table, width=width)

    table.expand = False
    console.print(table, justify="left")
    console.print(table, justify="center")
    console.print(table, justify="right")

    assert table.row_count == 1

    table.row_styles = ["red", "yellow"]
    table.add_row("Coffee")
    table.add_row("Coffee", "Chocolate", None, "cinnamon")

    assert table.row_count == 3

    console.print(table)

    table.show_lines = True
    console.print(table)

    table.show_footer = True
    console.print(table)

    table.show_edge = False

    console.print(table)

    table.padding = 1
    console.print(table)

    table.width = 20
    assert Measurement.get(console, console.options, table) == Measurement(20, 20)
    table.expand = False
    assert Measurement.get(console, console.options, table) == Measurement(20, 20)
    table.expand = True
    console.print(table)

    table.columns[0].no_wrap = True
    table.columns[1].no_wrap = True
    table.columns[2].no_wrap = True

    console.print(table)

    table.padding = 0
    table.width = 60
    table.leading = 1
    console.print(table)

    return console.file.getvalue()


def test_render_table():
    expected = "test table\n┏━━━━━━┳┳┓\n┃ foo  ┃┃┃\n┡━━━━━━╇╇┩\n│ Ave… │││\n└──────┴┴┘\n  table   \n caption  \n  test table   \n┏━━━━━━━━━━━┳┳┓\n┃ foo       ┃┃┃\n┡━━━━━━━━━━━╇╇┩\n│ Averlong… │││\n└───────────┴┴┘\n table caption \n     test table     \n┏━━━━━━━━━━━━━━━━┳┳┓\n┃ foo            ┃┃┃\n┡━━━━━━━━━━━━━━━━╇╇┩\n│ Averlongwordg… │││\n└────────────────┴┴┘\n   table caption    \n       test table        \n┏━━━━━━━━━━━━━━━━━━━━━┳┳┓\n┃ foo                 ┃┃┃\n┡━━━━━━━━━━━━━━━━━━━━━╇╇┩\n│ Averlongwordgoeshe… │││\n└─────────────────────┴┴┘\n      table caption      \n          test table          \n┏━━━━━━━━━━━━━━━━━━━━━━┳━━┳━━┓\n┃ foo                  ┃  ┃  ┃\n┡━━━━━━━━━━━━━━━━━━━━━━╇━━╇━━┩\n│ Averlongwordgoeshere │  │  │\n└──────────────────────┴──┴──┘\n        table caption         \n            test table             \n┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━┳━━━━┓\n┃ foo                  ┃ bar ┃ b… ┃\n┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━╇━━━━┩\n│ Averlongwordgoeshere │ ba… │    │\n│                      │ pa… │    │\n└──────────────────────┴─────┴────┘\n           table caption           \n               test table               \n┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━┓\n┃ foo                  ┃   bar   ┃ baz ┃\n┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━┩\n│ Averlongwordgoeshere │ banana  │     │\n│                      │ pancak… │     │\n└──────────────────────┴─────────┴─────┘\n             table caption              \n                 test table                  \n┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━┓\n┃ foo                  ┃     bar      ┃ baz ┃\n┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━┩\n│ Averlongwordgoeshere │    banana    │     │\n│                      │   pancakes   │     │\n└──────────────────────┴──────────────┴─────┘\n                table caption                \n                    test table                    \n┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━┓\n┃ foo                   ┃       bar        ┃ baz ┃\n┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━┩\n│ Averlongwordgoeshere  │ banana pancakes  │     │\n└───────────────────────┴──────────────────┴─────┘\n                  table caption                   \n                      test table                       \n┏━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━┓\n┃ foo                      ┃        bar         ┃ baz ┃\n┡━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━┩\n│ Averlongwordgoeshere     │  banana pancakes   │     │\n└──────────────────────────┴────────────────────┴─────┘\n                     table caption                     \n                   test table                               \n┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━┓            \n┃ foo                  ┃       bar       ┃ baz ┃            \n┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━┩            \n│ Averlongwordgoeshere │ banana pancakes │     │            \n└──────────────────────┴─────────────────┴─────┘            \n                 table caption                              \n                         test table                         \n      ┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━┓      \n      ┃ foo                  ┃       bar       ┃ baz ┃      \n      ┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━┩      \n      │ Averlongwordgoeshere │ banana pancakes │     │      \n      └──────────────────────┴─────────────────┴─────┘      \n                       table caption                        \n                               test table                   \n            ┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━┓\n            ┃ foo                  ┃       bar       ┃ baz ┃\n            ┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━┩\n            │ Averlongwordgoeshere │ banana pancakes │     │\n            └──────────────────────┴─────────────────┴─────┘\n                             table caption                  \n                        test table                         \n┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━┳━━━━━━━━━━┓\n┃ foo                  ┃       bar       ┃ baz ┃          ┃\n┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━╇━━━━━━━━━━┩\n│ Averlongwordgoeshere │ banana pancakes │     │          │\n│ Coffee               │                 │     │          │\n│ Coffee               │    Chocolate    │     │ cinnamon │\n└──────────────────────┴─────────────────┴─────┴──────────┘\n                       table caption                       \n                        test table                         \n┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━┳━━━━━━━━━━┓\n┃ foo                  ┃       bar       ┃ baz ┃          ┃\n┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━╇━━━━━━━━━━┩\n│ Averlongwordgoeshere │ banana pancakes │     │          │\n├──────────────────────┼─────────────────┼─────┼──────────┤\n│ Coffee               │                 │     │          │\n├──────────────────────┼─────────────────┼─────┼──────────┤\n│ Coffee               │    Chocolate    │     │ cinnamon │\n└──────────────────────┴─────────────────┴─────┴──────────┘\n                       table caption                       \n                        test table                         \n┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━┳━━━━━━━━━━┓\n┃ foo                  ┃       bar       ┃ baz ┃          ┃\n┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━╇━━━━━━━━━━┩\n│ Averlongwordgoeshere │ banana pancakes │     │          │\n├──────────────────────┼─────────────────┼─────┼──────────┤\n│ Coffee               │                 │     │          │\n├──────────────────────┼─────────────────┼─────┼──────────┤\n│ Coffee               │    Chocolate    │     │ cinnamon │\n├──────────────────────┼─────────────────┼─────┼──────────┤\n│ total                │                 │     │          │\n└──────────────────────┴─────────────────┴─────┴──────────┘\n                       table caption                       \n                       test table                        \n foo                  ┃       bar       ┃ baz ┃          \n━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━╇━━━━━━━━━━\n Averlongwordgoeshere │ banana pancakes │     │          \n──────────────────────┼─────────────────┼─────┼──────────\n Coffee               │                 │     │          \n──────────────────────┼─────────────────┼─────┼──────────\n Coffee               │    Chocolate    │     │ cinnamon \n──────────────────────┼─────────────────┼─────┼──────────\n total                │                 │     │          \n                      table caption                      \n                       test table                        \n                      ┃                 ┃     ┃          \n foo                  ┃       bar       ┃ baz ┃          \n                      ┃                 ┃     ┃          \n━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━╇━━━━━━━━━━\n                      │                 │     │          \n Averlongwordgoeshere │ banana pancakes │     │          \n                      │                 │     │          \n──────────────────────┼─────────────────┼─────┼──────────\n                      │                 │     │          \n Coffee               │                 │     │          \n                      │                 │     │          \n──────────────────────┼─────────────────┼─────┼──────────\n                      │                 │     │          \n Coffee               │    Chocolate    │     │ cinnamon \n                      │                 │     │          \n──────────────────────┼─────────────────┼─────┼──────────\n                      │                 │     │          \n total                │                 │     │          \n                      │                 │     │          \n                      table caption                      \n     test table     \n                 ┃┃┃\n foo             ┃┃┃\n                 ┃┃┃\n━━━━━━━━━━━━━━━━━╇╇╇\n                 │││\n Averlongwordgo… │││\n                 │││\n─────────────────┼┼┼\n                 │││\n Coffee          │││\n                 │││\n─────────────────┼┼┼\n                 │││\n Coffee          │││\n                 │││\n─────────────────┼┼┼\n                 │││\n total           │││\n                 │││\n   table caption    \n      test table      \n          ┃         ┃┃\n foo      ┃   bar   ┃┃\n          ┃         ┃┃\n━━━━━━━━━━╇━━━━━━━━━╇╇\n          │         ││\n Averlon… │ banana… ││\n          │         ││\n──────────┼─────────┼┼\n          │         ││\n Coffee   │         ││\n          │         ││\n──────────┼─────────┼┼\n          │         ││\n Coffee   │ Chocol… ││\n          │         ││\n──────────┼─────────┼┼\n          │         ││\n total    │         ││\n          │         ││\n    table caption     \n                         test table                         \nfoo                      ┃        bar        ┃ baz┃         \n━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━╇━━━━━━━━━\nAverlongwordgoeshere     │  banana pancakes  │    │         \n                         │                   │    │         \nCoffee                   │                   │    │         \n                         │                   │    │         \nCoffee                   │     Chocolate     │    │cinnamon \n─────────────────────────┼───────────────────┼────┼─────────\ntotal                    │                   │    │         \n                       table caption                        \n"
    result = render_tables()
    print(repr(result))
    assert result == expected


def test_not_renderable():
    class Foo:
        pass

    table = Table()
    with pytest.raises(errors.NotRenderableError):
        table.add_row(Foo())


def test_init_append_column():
    header_names = ["header1", "header2", "header3"]
    test_columns = [
        Column(_index=index, header=header) for index, header in enumerate(header_names)
    ]

    # Test appending of strings for header names
    assert Table(*header_names).columns == test_columns
    # Test directly passing a Table Column objects
    assert Table(*test_columns).columns == test_columns


def test_rich_measure():
    console = Console()
    assert Table("test_header", width=-1).__rich_measure__(
        console, console.options
    ) == Measurement(0, 0)
    # Check __rich_measure__() for a positive width passed as an argument
    assert Table("test_header", width=None).__rich_measure__(
        console, console.options.update_width(10)
    ) == Measurement(10, 10)


def test_min_width():
    table = Table("foo", min_width=30)
    table.add_row("bar")
    console = Console()
    assert table.__rich_measure__(
        console, console.options.update_width(100)
    ) == Measurement(30, 30)
    console = Console(color_system=None)
    console.begin_capture()
    console.print(table)
    output = console.end_capture()
    print(output)
    assert all(len(line) == 30 for line in output.splitlines())


def test_no_columns():
    console = Console(color_system=None)
    console.begin_capture()
    console.print(Table())
    output = console.end_capture()
    print(repr(output))
    assert output == "\n"


def test_get_row_style():
    console = Console()
    table = Table()
    table.add_row("foo")
    table.add_row("bar", style="on red")
    assert table.get_row_style(console, 0) == Style.parse("")
    assert table.get_row_style(console, 1) == Style.parse("on red")


def test_vertical_align_top():
    console = Console(_environ={})

    def make_table(vertical_align):
        table = Table(show_header=False, box=box.SQUARE)
        table.add_column(vertical=vertical_align)
        table.add_row("foo", "\n".join(["bar"] * 5))

        return table

    with console.capture() as capture:
        console.print(make_table("top"))
        console.print()
        console.print(make_table("middle"))
        console.print()
        console.print(make_table("bottom"))
        console.print()
    result = capture.get()
    print(repr(result))
    expected = "┌─────┬─────┐\n│ foo │ bar │\n│     │ bar │\n│     │ bar │\n│     │ bar │\n│     │ bar │\n└─────┴─────┘\n\n┌─────┬─────┐\n│     │ bar │\n│     │ bar │\n│ foo │ bar │\n│     │ bar │\n│     │ bar │\n└─────┴─────┘\n\n┌─────┬─────┐\n│     │ bar │\n│     │ bar │\n│     │ bar │\n│     │ bar │\n│ foo │ bar │\n└─────┴─────┘\n\n"
    assert result == expected


@pytest.mark.parametrize(
    "box,result",
    [
        (None, " 1  2 \n 3  4 \n"),
        (box.HEAVY_HEAD, "┌───┬───┐\n│ 1 │ 2 │\n│ 3 │ 4 │\n└───┴───┘\n"),
        (box.SQUARE_DOUBLE_HEAD, "┌───┬───┐\n│ 1 │ 2 │\n│ 3 │ 4 │\n└───┴───┘\n"),
        (box.MINIMAL_DOUBLE_HEAD, "    ╷    \n  1 │ 2  \n  3 │ 4  \n    ╵    \n"),
        (box.MINIMAL_HEAVY_HEAD, "    ╷    \n  1 │ 2  \n  3 │ 4  \n    ╵    \n"),
        (box.ASCII_DOUBLE_HEAD, "+---+---+\n| 1 | 2 |\n| 3 | 4 |\n+---+---+\n"),
    ],
)
def test_table_show_header_false_substitution(box, result):
    """When the box style is one with a custom header edge, it should be substituted for
    the equivalent box that does not have a custom header when show_header=False"""
    table = Table(show_header=False, box=box)
    table.add_column()
    table.add_column()

    table.add_row("1", "2")
    table.add_row("3", "4")

    console = Console(record=True)
    console.print(table)
    output = console.export_text()

    assert output == result


def test_section():
    table = Table("foo")
    table.add_section()  # Null-op
    table.add_row("row1")
    table.add_row("row2", end_section=True)
    table.add_row("row3")
    table.add_row("row4")
    table.add_section()
    table.add_row("row5")
    table.add_section()  # Null-op

    console = Console(
        width=80,
        force_terminal=True,
        color_system="truecolor",
        legacy_windows=False,
        record=True,
    )
    console.print(table)
    output = console.export_text()
    print(repr(output))
    expected = "┏━━━━━━┓\n┃ foo  ┃\n┡━━━━━━┩\n│ row1 │\n│ row2 │\n├──────┤\n│ row3 │\n│ row4 │\n├──────┤\n│ row5 │\n└──────┘\n"

    assert output == expected


if __name__ == "__main__":
    render = render_tables()
    print(render)
    print(repr(render))
