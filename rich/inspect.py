from collections.abc import Sequence, Mapping
from typing import Any, TYPE_CHECKING


from . import box
from .repr import console_repr
from .table import Column, Table
from .text import Text


if TYPE_CHECKING:
    from .console import ConsoleRenderable


def inspect(object: Any) -> ConsoleRenderable:
    if isinstance(object, str):
        return console_repr(object)
    if isinstance(object, Mapping):
        return inspect_mapping(object)
    if isinstance(object, Sequence):
        return inspect_sequence(object)
    return console_repr(object)


def inspect_sequence(sequence: Sequence) -> Table:
    table = Table(
        Column("key", style="inspect.key", justify="right"),
        Column("value", style="inspect.value"),
        show_header=False,
        box=None,
        padding=0,
    )
    for key, value in enumerate(sequence):
        table.add_row(console_repr(key) + Text(": ", "not italic"), console_repr(value))
    return table


def inspect_mapping(mapping: Mapping) -> Table:
    table = Table(
        Column("key", style="inspect.key"),
        Column("value", style="inspect.value"),
        show_header=False,
        box=None,
        padding=0,
    )
    for key, value in mapping.items():
        table.add_row(console_repr(key) + Text(": ", "not italic"), console_repr(value))
    return table


if __name__ == "__main__":
    from .console import Console

    console = Console()
    mapping = {
        "version": "1.1",
        "method": "confirmFruitPurchase",
        "params": [["apple", "orange", "mangoes"], 1.123],
        "id": "194521489",
    }
    console.print(inspect(mapping))
    console.print(inspect(["Hello", "World", "!", 5] * 6))

    from .syntax import Syntax

    syntax = Syntax(repr(mapping), "python", theme="monokai")
    console.print(syntax)
    console.print(Text("50", style="italic bold") + Text(":"))

    from pprint import pprint

    pprint(mapping)
