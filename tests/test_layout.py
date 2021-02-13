import pytest

from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel


def test_render():
    layout = Layout(name="root")
    repr(layout)
    top = layout.split()
    top.update(Panel("foo"))
    print(type(top._renderable))
    assert isinstance(top.renderable, Panel)
    bottom = layout.split(direction="horizontal")
    bottom.split(name="left")
    bottom.split(name="right")

    assert layout["root"].name == "root"
    assert layout["left"].name == "left"
    with pytest.raises(KeyError):
        top["asdasd"]

    layout["left"].update("foobar")

    console = Console(width=60, color_system=None)

    with console.capture() as capture:
        console.print(layout, height=10)

    result = capture.get()
    expected = "╭──────────────────────────────────────────────────────────╮\n│ foo                                                      │\n│                                                          │\n│                                                          │\n╰──────────────────────────────────────────────────────────╯\nfoobar                        ╭───── 'right' (30 x 5) ─────╮\n                              │   {                        │\n                              │       'size': None,        │\n                              │       'minimum_size': 1,   │\n                              ╰────────────────────────────╯\n"
    assert result == expected


def test_tree():
    layout = Layout(name="root")
    layout.split("foo", size=2)
    layout.split("bar")

    console = Console(width=60, color_system=None)

    with console.capture() as capture:
        console.print(layout.tree, height=10)
    result = capture.get()
    print(repr(result))
    expected = "'root' (ratio=1)                                            \n├── (size=2)                                                \n└── (ratio=1)                                               \n"

    assert result == expected