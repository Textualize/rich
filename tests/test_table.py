# encoding=utf-8

import io

import pytest

from rich import errors
from rich.console import Console
from rich.measure import Measurement
from rich.table import Table
from rich.text import Text


def render_tables():
    console = Console(
        width=60,
        force_terminal=True,
        file=io.StringIO(),
        legacy_windows=False,
        color_system=None,
    )

    table = Table(title="test table", caption="table caption", expand=True)
    table.add_column("foo", footer=Text("total"), no_wrap=True, overflow="ellipsis")
    table.add_column("bar", justify="center")
    table.add_column("baz", justify="right")

    table.add_row("Averlongwordgoeshere", "banana pancakes", None)

    assert Measurement.get(console, table, 80) == Measurement(41, 48)

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
    assert Measurement.get(console, table, 80) == Measurement(46, 52)
    console.print(table)

    return console.file.getvalue()


def test_render_table():
    expected = "test table\n┏━━┳━━┳━━┓\n┃  ┃  ┃  ┃\n┡━━╇━━╇━━┩\n│  │  │  │\n└──┴──┴──┘\n  table   \n caption  \n  test table   \n┏━━━━━┳━━━━┳━━┓\n┃ foo ┃ b… ┃  ┃\n┡━━━━━╇━━━━╇━━┩\n│ Av… │ b… │  │\n└─────┴────┴──┘\n table caption \n     test table     \n┏━━━━━━━━┳━━━━━┳━━━┓\n┃ foo    ┃ bar ┃ … ┃\n┡━━━━━━━━╇━━━━━╇━━━┩\n│ Averl… │ ba… │   │\n└────────┴─────┴───┘\n   table caption    \n       test table        \n┏━━━━━━━━━━━━┳━━━━━━┳━━━┓\n┃ foo        ┃ bar  ┃ … ┃\n┡━━━━━━━━━━━━╇━━━━━━╇━━━┩\n│ Averlongw… │ ban… │   │\n└────────────┴──────┴───┘\n      table caption      \n          test table          \n┏━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━┓\n┃ foo           ┃  bar  ┃ b… ┃\n┡━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━┩\n│ Averlongword… │ bana… │    │\n└───────────────┴───────┴────┘\n        table caption         \n            test table             \n┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━┓\n┃ foo              ┃   bar   ┃ b… ┃\n┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━┩\n│ Averlongwordgoe… │ banana… │    │\n└──────────────────┴─────────┴────┘\n           table caption           \n               test table               \n┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━┓\n┃ foo                 ┃   bar    ┃ baz ┃\n┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━┩\n│ Averlongwordgoeshe… │  banana  │     │\n│                     │ pancakes │     │\n└─────────────────────┴──────────┴─────┘\n             table caption              \n                 test table                  \n┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━┓\n┃ foo                  ┃     bar      ┃ baz ┃\n┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━┩\n│ Averlongwordgoeshere │    banana    │     │\n│                      │   pancakes   │     │\n└──────────────────────┴──────────────┴─────┘\n                table caption                \n                    test table                    \n┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━┓\n┃ foo                   ┃       bar        ┃ baz ┃\n┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━┩\n│ Averlongwordgoeshere  │ banana pancakes  │     │\n└───────────────────────┴──────────────────┴─────┘\n                  table caption                   \n                      test table                       \n┏━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━┓\n┃ foo                      ┃        bar         ┃ baz ┃\n┡━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━┩\n│ Averlongwordgoeshere     │  banana pancakes   │     │\n└──────────────────────────┴────────────────────┴─────┘\n                     table caption                     \n                   test table                   \n┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━┓\n┃ foo                  ┃       bar       ┃ baz ┃\n┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━┩\n│ Averlongwordgoeshere │ banana pancakes │     │\n└──────────────────────┴─────────────────┴─────┘\n                 table caption                  \n                         test table                   \n      ┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━┓\n      ┃ foo                  ┃       bar       ┃ baz ┃\n      ┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━┩\n      │ Averlongwordgoeshere │ banana pancakes │     │\n      └──────────────────────┴─────────────────┴─────┘\n                       table caption                  \n                               test table                   \n            ┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━┓\n            ┃ foo                  ┃       bar       ┃ baz ┃\n            ┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━┩\n            │ Averlongwordgoeshere │ banana pancakes │     │\n            └──────────────────────┴─────────────────┴─────┘\n                             table caption                  \n                        test table                         \n┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━┳━━━━━━━━━━┓\n┃ foo                  ┃       bar       ┃ baz ┃          ┃\n┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━╇━━━━━━━━━━┩\n│ Averlongwordgoeshere │ banana pancakes │     │          │\n│ Coffee               │                 │     │          │\n│ Coffee               │    Chocolate    │     │ cinnamon │\n└──────────────────────┴─────────────────┴─────┴──────────┘\n                       table caption                       \n                        test table                         \n┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━┳━━━━━━━━━━┓\n┃ foo                  ┃       bar       ┃ baz ┃          ┃\n┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━╇━━━━━━━━━━┩\n│ Averlongwordgoeshere │ banana pancakes │     │          │\n├──────────────────────┼─────────────────┼─────┼──────────┤\n│ Coffee               │                 │     │          │\n├──────────────────────┼─────────────────┼─────┼──────────┤\n│ Coffee               │    Chocolate    │     │ cinnamon │\n└──────────────────────┴─────────────────┴─────┴──────────┘\n                       table caption                       \n                        test table                         \n┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━┳━━━━━━━━━━┓\n┃ foo                  ┃       bar       ┃ baz ┃          ┃\n┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━╇━━━━━━━━━━┩\n│ Averlongwordgoeshere │ banana pancakes │     │          │\n├──────────────────────┼─────────────────┼─────┼──────────┤\n│ Coffee               │                 │     │          │\n├──────────────────────┼─────────────────┼─────┼──────────┤\n│ Coffee               │    Chocolate    │     │ cinnamon │\n├──────────────────────┼─────────────────┼─────┼──────────┤\n│ total                │                 │     │          │\n└──────────────────────┴─────────────────┴─────┴──────────┘\n                       table caption                       \n                       test table                        \n foo                  ┃       bar       ┃ baz ┃          \n━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━╇━━━━━━━━━━\n Averlongwordgoeshere │ banana pancakes │     │          \n──────────────────────┼─────────────────┼─────┼──────────\n Coffee               │                 │     │          \n──────────────────────┼─────────────────┼─────┼──────────\n Coffee               │    Chocolate    │     │ cinnamon \n──────────────────────┼─────────────────┼─────┼──────────\n total                │                 │     │          \n                      table caption                      \n                       test table                        \n                      ┃                 ┃     ┃          \n foo                  ┃       bar       ┃ baz ┃          \n                      ┃                 ┃     ┃          \n━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━╇━━━━━━━━━━\n                      │                 │     │          \n Averlongwordgoeshere │ banana pancakes │     │          \n                      │                 │     │          \n──────────────────────┼─────────────────┼─────┼──────────\n                      │                 │     │          \n Coffee               │                 │     │          \n                      │                 │     │          \n──────────────────────┼─────────────────┼─────┼──────────\n                      │                 │     │          \n Coffee               │    Chocolate    │     │ cinnamon \n                      │                 │     │          \n──────────────────────┼─────────────────┼─────┼──────────\n                      │                 │     │          \n total                │                 │     │          \n                      │                 │     │          \n                      table caption                      \n     test table     \n       ┃    ┃  ┃    \n foo   ┃ b… ┃  ┃    \n       ┃    ┃  ┃    \n━━━━━━━╇━━━━╇━━╇━━━━\n       │    │  │    \n Aver… │ b… │  │    \n       │    │  │    \n───────┼────┼──┼────\n       │    │  │    \n Coff… │    │  │    \n       │    │  │    \n───────┼────┼──┼────\n       │    │  │    \n Coff… │ C… │  │ c… \n       │    │  │    \n───────┼────┼──┼────\n       │    │  │    \n total │    │  │    \n       │    │  │    \n   table caption    \n"
    assert render_tables() == expected


def test_not_renderable():
    class Foo:
        pass

    table = Table()
    with pytest.raises(errors.NotRenderableError):
        table.add_row(Foo())


if __name__ == "__main__":
    render = render_tables()
    print(render)
    print(repr(render))
