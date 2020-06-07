# encoding=utf-8

import io


from rich.console import Console
from rich.table import Table


def render_tables():
    console = Console(width=60, file=io.StringIO())

    table = Table(title="test table", caption="table footer", expand=True)
    table.add_column("foo", no_wrap=True, overflow="ellipsis")
    table.add_column("bar", justify="center")
    table.add_column("baz", justify="right")

    table.add_row("Averlongwordgoeshere", "banana pancakes", None)

    for width in range(10, 60, 5):
        console.print(table, width=width)

    return console.file.getvalue()


def test_render_table():
    expected = "test table\n┏━━┳━━┳━━┓\n┃  ┃  ┃  ┃\n┡━━╇━━╇━━┩\n│  │  │  │\n└──┴──┴──┘\n  table   \n  footer  \n  test table   \n┏━━━━━┳━━━━┳━━┓\n┃ foo ┃ b… ┃  ┃\n┡━━━━━╇━━━━╇━━┩\n│ Av… │ b… │  │\n└─────┴────┴──┘\n table footer  \n     test table     \n┏━━━━━━━━┳━━━━━┳━━━┓\n┃ foo    ┃ bar ┃ … ┃\n┡━━━━━━━━╇━━━━━╇━━━┩\n│ Averl… │ ba… │   │\n└────────┴─────┴───┘\n    table footer    \n       test table        \n┏━━━━━━━━━━━━┳━━━━━━┳━━━┓\n┃ foo        ┃ bar  ┃ … ┃\n┡━━━━━━━━━━━━╇━━━━━━╇━━━┩\n│ Averlongw… │ ban… │   │\n└────────────┴──────┴───┘\n      table footer       \n          test table          \n┏━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━┓\n┃ foo           ┃  bar  ┃ b… ┃\n┡━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━┩\n│ Averlongword… │ bana… │    │\n└───────────────┴───────┴────┘\n         table footer         \n            test table             \n┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━┓\n┃ foo              ┃   bar   ┃ b… ┃\n┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━┩\n│ Averlongwordgoe… │ banana… │    │\n└──────────────────┴─────────┴────┘\n           table footer            \n               test table               \n┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━┓\n┃ foo                 ┃   bar    ┃ baz ┃\n┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━┩\n│ Averlongwordgoeshe… │  banana  │     │\n│                     │ pancakes │     │\n└─────────────────────┴──────────┴─────┘\n              table footer              \n                 test table                  \n┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━┓\n┃ foo                  ┃     bar      ┃ baz ┃\n┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━┩\n│ Averlongwordgoeshere │    banana    │     │\n│                      │   pancakes   │     │\n└──────────────────────┴──────────────┴─────┘\n                table footer                 \n                    test table                    \n┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━┓\n┃ foo                   ┃       bar        ┃ baz ┃\n┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━┩\n│ Averlongwordgoeshere  │ banana pancakes  │     │\n└───────────────────────┴──────────────────┴─────┘\n                   table footer                   \n                      test table                       \n┏━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━┓\n┃ foo                      ┃        bar         ┃ baz ┃\n┡━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━┩\n│ Averlongwordgoeshere     │  banana pancakes   │     │\n└──────────────────────────┴────────────────────┴─────┘\n                     table footer                      \n"
    assert render_tables() == expected


if __name__ == "__main__":
    render = render_tables()
    print(render)
    print(repr(render))
