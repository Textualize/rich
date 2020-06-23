# encoding=utf-8

import io


from rich.console import Console
from rich.table import Table
from rich.text import Text


def render_tables():
    console = Console(
        width=60,
        force_terminal=True,
        file=io.StringIO(),
        legacy_windows=False,
        color_system="truecolor",
    )

    table = Table(title="test table", caption="table caption", expand=True)
    table.add_column("foo", footer=Text("total"), no_wrap=True, overflow="ellipsis")
    table.add_column("bar", justify="center")
    table.add_column("baz", justify="right")

    table.add_row("Averlongwordgoeshere", "banana pancakes", None)
    for width in range(10, 60, 5):
        console.print(table, width=width)

    table.expand = False
    console.print(table, justify="left")
    console.print(table, justify="center")
    console.print(table, justify="right")

    assert table.row_count == 1

    table.row_styles = ["red", "yellow"]
    table.add_row("Coffee", "Chocolate")

    assert table.row_count == 2

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
    console.print(table)

    return console.file.getvalue()


def test_render_table():
    expected = "\x1b[3mtest table\x1b[0m\n┏━━┳━━┳━━┓\n┃\x1b[1m \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1m \x1b[0m┃\n┡━━╇━━╇━━┩\n│  │  │  │\n└──┴──┴──┘\n\x1b[2;3m  table   \x1b[0m\n\x1b[2;3m caption  \x1b[0m\n\x1b[3m  test table   \x1b[0m\n┏━━━━━┳━━━━┳━━┓\n┃\x1b[1m \x1b[0m\x1b[1mfoo\x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1mb…\x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1m \x1b[0m┃\n┡━━━━━╇━━━━╇━━┩\n│ Av… │ b… │  │\n└─────┴────┴──┘\n\x1b[2;3m table caption \x1b[0m\n\x1b[3m     test table     \x1b[0m\n┏━━━━━━━━┳━━━━━┳━━━┓\n┃\x1b[1m \x1b[0m\x1b[1mfoo   \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1mbar\x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1m…\x1b[0m\x1b[1m \x1b[0m┃\n┡━━━━━━━━╇━━━━━╇━━━┩\n│ Averl… │ ba… │   │\n└────────┴─────┴───┘\n\x1b[2;3m   table caption    \x1b[0m\n\x1b[3m       test table        \x1b[0m\n┏━━━━━━━━━━━━┳━━━━━━┳━━━┓\n┃\x1b[1m \x1b[0m\x1b[1mfoo       \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1mbar \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1m…\x1b[0m\x1b[1m \x1b[0m┃\n┡━━━━━━━━━━━━╇━━━━━━╇━━━┩\n│ Averlongw… │ ban… │   │\n└────────────┴──────┴───┘\n\x1b[2;3m      table caption      \x1b[0m\n\x1b[3m          test table          \x1b[0m\n┏━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━┓\n┃\x1b[1m \x1b[0m\x1b[1mfoo          \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1m bar \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1mb…\x1b[0m\x1b[1m \x1b[0m┃\n┡━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━┩\n│ Averlongword… │ bana… │    │\n└───────────────┴───────┴────┘\n\x1b[2;3m        table caption         \x1b[0m\n\x1b[3m            test table             \x1b[0m\n┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━┓\n┃\x1b[1m \x1b[0m\x1b[1mfoo             \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1m  bar  \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1mb…\x1b[0m\x1b[1m \x1b[0m┃\n┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━┩\n│ Averlongwordgoe… │ banana… │    │\n└──────────────────┴─────────┴────┘\n\x1b[2;3m           table caption           \x1b[0m\n\x1b[3m               test table               \x1b[0m\n┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━┓\n┃\x1b[1m \x1b[0m\x1b[1mfoo                \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1m  bar   \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1mbaz\x1b[0m\x1b[1m \x1b[0m┃\n┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━┩\n│ Averlongwordgoeshe… │  banana  │     │\n│                     │ pancakes │     │\n└─────────────────────┴──────────┴─────┘\n\x1b[2;3m             table caption              \x1b[0m\n\x1b[3m                 test table                  \x1b[0m\n┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━┓\n┃\x1b[1m \x1b[0m\x1b[1mfoo                 \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1m    bar     \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1mbaz\x1b[0m\x1b[1m \x1b[0m┃\n┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━┩\n│ Averlongwordgoeshere │    banana    │     │\n│                      │   pancakes   │     │\n└──────────────────────┴──────────────┴─────┘\n\x1b[2;3m                table caption                \x1b[0m\n\x1b[3m                    test table                    \x1b[0m\n┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━┓\n┃\x1b[1m \x1b[0m\x1b[1mfoo                  \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1m      bar       \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1mbaz\x1b[0m\x1b[1m \x1b[0m┃\n┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━┩\n│ Averlongwordgoeshere  │ banana pancakes  │     │\n└───────────────────────┴──────────────────┴─────┘\n\x1b[2;3m                  table caption                   \x1b[0m\n\x1b[3m                      test table                       \x1b[0m\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━┓\n┃\x1b[1m \x1b[0m\x1b[1mfoo                     \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1m       bar        \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1mbaz\x1b[0m\x1b[1m \x1b[0m┃\n┡━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━┩\n│ Averlongwordgoeshere     │  banana pancakes   │     │\n└──────────────────────────┴────────────────────┴─────┘\n\x1b[2;3m                     table caption                     \x1b[0m\n\x1b[3m                   test table                   \x1b[0m\n┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━┓\n┃\x1b[1m \x1b[0m\x1b[1mfoo                 \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1m      bar      \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1mbaz\x1b[0m\x1b[1m \x1b[0m┃\n┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━┩\n│ Averlongwordgoeshere │ banana pancakes │     │\n└──────────────────────┴─────────────────┴─────┘\n\x1b[2;3m                 table caption                  \x1b[0m\n      \x1b[3m                   test table                   \x1b[0m\n      ┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━┓\n      ┃\x1b[1m \x1b[0m\x1b[1mfoo                 \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1m      bar      \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1mbaz\x1b[0m\x1b[1m \x1b[0m┃\n      ┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━┩\n      │ Averlongwordgoeshere │ banana pancakes │     │\n      └──────────────────────┴─────────────────┴─────┘\n      \x1b[2;3m                 table caption                  \x1b[0m\n            \x1b[3m                   test table                   \x1b[0m\n            ┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━┓\n            ┃\x1b[1m \x1b[0m\x1b[1mfoo                 \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1m      bar      \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1mbaz\x1b[0m\x1b[1m \x1b[0m┃\n            ┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━┩\n            │ Averlongwordgoeshere │ banana pancakes │     │\n            └──────────────────────┴─────────────────┴─────┘\n            \x1b[2;3m                 table caption                  \x1b[0m\n\x1b[3m                   test table                   \x1b[0m\n┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━┓\n┃\x1b[1m \x1b[0m\x1b[1mfoo                 \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1m      bar      \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1mbaz\x1b[0m\x1b[1m \x1b[0m┃\n┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━┩\n│\x1b[31m \x1b[0m\x1b[31mAverlongwordgoeshere\x1b[0m\x1b[31m \x1b[0m│\x1b[31m \x1b[0m\x1b[31mbanana pancakes\x1b[0m\x1b[31m \x1b[0m│\x1b[31m \x1b[0m\x1b[31m   \x1b[0m\x1b[31m \x1b[0m│\n│\x1b[33m \x1b[0m\x1b[33mCoffee              \x1b[0m\x1b[33m \x1b[0m│\x1b[33m \x1b[0m\x1b[33m   Chocolate   \x1b[0m\x1b[33m \x1b[0m│\x1b[33m \x1b[0m\x1b[33m   \x1b[0m\x1b[33m \x1b[0m│\n└──────────────────────┴─────────────────┴─────┘\n\x1b[2;3m                 table caption                  \x1b[0m\n\x1b[3m                   test table                   \x1b[0m\n┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━┓\n┃\x1b[1m \x1b[0m\x1b[1mfoo                 \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1m      bar      \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1mbaz\x1b[0m\x1b[1m \x1b[0m┃\n┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━┩\n│\x1b[31m \x1b[0m\x1b[31mAverlongwordgoeshere\x1b[0m\x1b[31m \x1b[0m│\x1b[31m \x1b[0m\x1b[31mbanana pancakes\x1b[0m\x1b[31m \x1b[0m│\x1b[31m \x1b[0m\x1b[31m   \x1b[0m\x1b[31m \x1b[0m│\n├──────────────────────┼─────────────────┼─────┤\n│\x1b[33m \x1b[0m\x1b[33mCoffee              \x1b[0m\x1b[33m \x1b[0m│\x1b[33m \x1b[0m\x1b[33m   Chocolate   \x1b[0m\x1b[33m \x1b[0m│\x1b[33m \x1b[0m\x1b[33m   \x1b[0m\x1b[33m \x1b[0m│\n└──────────────────────┴─────────────────┴─────┘\n\x1b[2;3m                 table caption                  \x1b[0m\n\x1b[3m                   test table                   \x1b[0m\n┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━┓\n┃\x1b[1m \x1b[0m\x1b[1mfoo                 \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1m      bar      \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1mbaz\x1b[0m\x1b[1m \x1b[0m┃\n┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━┩\n│\x1b[31m \x1b[0m\x1b[31mAverlongwordgoeshere\x1b[0m\x1b[31m \x1b[0m│\x1b[31m \x1b[0m\x1b[31mbanana pancakes\x1b[0m\x1b[31m \x1b[0m│\x1b[31m \x1b[0m\x1b[31m   \x1b[0m\x1b[31m \x1b[0m│\n├──────────────────────┼─────────────────┼─────┤\n│\x1b[33m \x1b[0m\x1b[33mCoffee              \x1b[0m\x1b[33m \x1b[0m│\x1b[33m \x1b[0m\x1b[33m   Chocolate   \x1b[0m\x1b[33m \x1b[0m│\x1b[33m \x1b[0m\x1b[33m   \x1b[0m\x1b[33m \x1b[0m│\n├──────────────────────┼─────────────────┼─────┤\n│\x1b[1m \x1b[0m\x1b[1mtotal               \x1b[0m\x1b[1m \x1b[0m│\x1b[1m \x1b[0m\x1b[1m               \x1b[0m\x1b[1m \x1b[0m│\x1b[1m \x1b[0m\x1b[1m   \x1b[0m\x1b[1m \x1b[0m│\n└──────────────────────┴─────────────────┴─────┘\n\x1b[2;3m                 table caption                  \x1b[0m\n\x1b[3m                  test table                  \x1b[0m\n\x1b[1m \x1b[0m\x1b[1mfoo                 \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1m      bar      \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1mbaz\x1b[0m\x1b[1m \x1b[0m\n━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━\n\x1b[31m \x1b[0m\x1b[31mAverlongwordgoeshere\x1b[0m\x1b[31m \x1b[0m│\x1b[31m \x1b[0m\x1b[31mbanana pancakes\x1b[0m\x1b[31m \x1b[0m│\x1b[31m \x1b[0m\x1b[31m   \x1b[0m\x1b[31m \x1b[0m\n──────────────────────┼─────────────────┼─────\n\x1b[33m \x1b[0m\x1b[33mCoffee              \x1b[0m\x1b[33m \x1b[0m│\x1b[33m \x1b[0m\x1b[33m   Chocolate   \x1b[0m\x1b[33m \x1b[0m│\x1b[33m \x1b[0m\x1b[33m   \x1b[0m\x1b[33m \x1b[0m\n──────────────────────┼─────────────────┼─────\n\x1b[1m \x1b[0m\x1b[1mtotal               \x1b[0m\x1b[1m \x1b[0m│\x1b[1m \x1b[0m\x1b[1m               \x1b[0m\x1b[1m \x1b[0m│\x1b[1m \x1b[0m\x1b[1m   \x1b[0m\x1b[1m \x1b[0m\n\x1b[2;3m                table caption                 \x1b[0m\n\x1b[3m                  test table                  \x1b[0m\n\x1b[1m                      \x1b[0m┃\x1b[1m                 \x1b[0m┃\x1b[1m     \x1b[0m\n\x1b[1m \x1b[0m\x1b[1mfoo                 \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1m      bar      \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1mbaz\x1b[0m\x1b[1m \x1b[0m\n\x1b[1m                      \x1b[0m┃\x1b[1m                 \x1b[0m┃\x1b[1m     \x1b[0m\n━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━\n\x1b[31m                      \x1b[0m│\x1b[31m                 \x1b[0m│\x1b[31m     \x1b[0m\n\x1b[31m \x1b[0m\x1b[31mAverlongwordgoeshere\x1b[0m\x1b[31m \x1b[0m│\x1b[31m \x1b[0m\x1b[31mbanana pancakes\x1b[0m\x1b[31m \x1b[0m│\x1b[31m \x1b[0m\x1b[31m   \x1b[0m\x1b[31m \x1b[0m\n\x1b[31m                      \x1b[0m│\x1b[31m                 \x1b[0m│\x1b[31m     \x1b[0m\n──────────────────────┼─────────────────┼─────\n\x1b[33m                      \x1b[0m│\x1b[33m                 \x1b[0m│\x1b[33m     \x1b[0m\n\x1b[33m \x1b[0m\x1b[33mCoffee              \x1b[0m\x1b[33m \x1b[0m│\x1b[33m \x1b[0m\x1b[33m   Chocolate   \x1b[0m\x1b[33m \x1b[0m│\x1b[33m \x1b[0m\x1b[33m   \x1b[0m\x1b[33m \x1b[0m\n\x1b[33m                      \x1b[0m│\x1b[33m                 \x1b[0m│\x1b[33m     \x1b[0m\n──────────────────────┼─────────────────┼─────\n\x1b[1m                      \x1b[0m│\x1b[1m                 \x1b[0m│\x1b[1m     \x1b[0m\n\x1b[1m \x1b[0m\x1b[1mtotal               \x1b[0m\x1b[1m \x1b[0m│\x1b[1m \x1b[0m\x1b[1m               \x1b[0m\x1b[1m \x1b[0m│\x1b[1m \x1b[0m\x1b[1m   \x1b[0m\x1b[1m \x1b[0m\n\x1b[1m                      \x1b[0m│\x1b[1m                 \x1b[0m│\x1b[1m     \x1b[0m\n\x1b[2;3m                table caption                 \x1b[0m\n\x1b[3m     test table     \x1b[0m\n\x1b[1m          \x1b[0m┃\x1b[1m     \x1b[0m┃\x1b[1m   \x1b[0m\n\x1b[1m \x1b[0m\x1b[1mfoo     \x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1mbar\x1b[0m\x1b[1m \x1b[0m┃\x1b[1m \x1b[0m\x1b[1m…\x1b[0m\x1b[1m \x1b[0m\n\x1b[1m          \x1b[0m┃\x1b[1m     \x1b[0m┃\x1b[1m   \x1b[0m\n━━━━━━━━━━╇━━━━━╇━━━\n\x1b[31m          \x1b[0m│\x1b[31m     \x1b[0m│\x1b[31m   \x1b[0m\n\x1b[31m \x1b[0m\x1b[31mAverlon…\x1b[0m\x1b[31m \x1b[0m│\x1b[31m \x1b[0m\x1b[31mba…\x1b[0m\x1b[31m \x1b[0m│\x1b[31m \x1b[0m\x1b[31m \x1b[0m\x1b[31m \x1b[0m\n\x1b[31m          \x1b[0m│\x1b[31m     \x1b[0m│\x1b[31m   \x1b[0m\n──────────┼─────┼───\n\x1b[33m          \x1b[0m│\x1b[33m     \x1b[0m│\x1b[33m   \x1b[0m\n\x1b[33m \x1b[0m\x1b[33mCoffee  \x1b[0m\x1b[33m \x1b[0m│\x1b[33m \x1b[0m\x1b[33mCh…\x1b[0m\x1b[33m \x1b[0m│\x1b[33m \x1b[0m\x1b[33m \x1b[0m\x1b[33m \x1b[0m\n\x1b[33m          \x1b[0m│\x1b[33m     \x1b[0m│\x1b[33m   \x1b[0m\n──────────┼─────┼───\n\x1b[1m          \x1b[0m│\x1b[1m     \x1b[0m│\x1b[1m   \x1b[0m\n\x1b[1m \x1b[0m\x1b[1mtotal   \x1b[0m\x1b[1m \x1b[0m│\x1b[1m \x1b[0m\x1b[1m   \x1b[0m\x1b[1m \x1b[0m│\x1b[1m \x1b[0m\x1b[1m \x1b[0m\x1b[1m \x1b[0m\n\x1b[1m          \x1b[0m│\x1b[1m     \x1b[0m│\x1b[1m   \x1b[0m\n\x1b[2;3m   table caption    \x1b[0m\n"
    assert render_tables() == expected


if __name__ == "__main__":
    render = render_tables()
    print(render)
    print(repr(render))
