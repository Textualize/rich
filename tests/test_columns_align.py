# encoding=utf-8

import io

from rich import box
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel


def render():
    console = Console(file=io.StringIO(), width=100, legacy_windows=False)
    panel = Panel.fit("foo", box=box.SQUARE, padding=0)
    columns = Columns([panel] * 4)
    columns.expand = True
    console.rule("no align")
    console.print(columns)

    columns.align = "left"
    console.rule("left align")
    console.print(columns)

    columns.align = "center"
    console.rule("center align")
    console.print(columns)

    columns.align = "right"
    console.rule("right align")
    console.print(columns)

    return console.file.getvalue()


def test_align():
    result = render()
    expected = "───────────────────────────────────────────── no align ─────────────────────────────────────────────\n┌───┐                      ┌───┐                     ┌───┐                     ┌───┐                \n│foo│                      │foo│                     │foo│                     │foo│                \n└───┘                      └───┘                     └───┘                     └───┘                \n──────────────────────────────────────────── left align ────────────────────────────────────────────\n┌───┐                      ┌───┐                     ┌───┐                     ┌───┐                \n│foo│                      │foo│                     │foo│                     │foo│                \n└───┘                      └───┘                     └───┘                     └───┘                \n─────────────────────────────────────────── center align ───────────────────────────────────────────\n          ┌───┐                      ┌───┐                     ┌───┐                   ┌───┐        \n          │foo│                      │foo│                     │foo│                   │foo│        \n          └───┘                      └───┘                     └───┘                   └───┘        \n─────────────────────────────────────────── right align ────────────────────────────────────────────\n                     ┌───┐                     ┌───┐                     ┌───┐                 ┌───┐\n                     │foo│                     │foo│                     │foo│                 │foo│\n                     └───┘                     └───┘                     └───┘                 └───┘\n"
    assert result == expected


if __name__ == "__main__":
    rendered = render()
    print(rendered)
    print(repr(rendered))
