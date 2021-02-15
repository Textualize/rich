import sys
import pytest

from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel


@pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")
def test_render():
    layout = Layout(name="root")
    repr(layout)

    layout.split(Layout(name="top"), Layout(name="bottom"))
    top = layout["top"]
    top.update(Panel("foo"))

    print(type(top._renderable))
    assert isinstance(top.renderable, Panel)
    layout["bottom"].split(
        Layout(name="left"), Layout(name="right"), direction="horizontal"
    )

    assert layout["root"].name == "root"
    assert layout["left"].name == "left"
    with pytest.raises(KeyError):
        top["asdasd"]

    layout["left"].update("foobar")
    print(layout["left"].children)

    console = Console(width=60, color_system=None)

    with console.capture() as capture:
        console.print(layout, height=10)

    result = capture.get()
    expected = "╭──────────────────────────────────────────────────────────╮\n│ foo                                                      │\n│                                                          │\n│                                                          │\n╰──────────────────────────────────────────────────────────╯\nfoobar                        ╭───── 'right' (30 x 5) ─────╮\n                              │   {                        │\n                              │       'size': None,        │\n                              │       'minimum_size': 1,   │\n                              ╰────────────────────────────╯\n"
    assert result == expected


def test_tree():
    layout = Layout(name="root")
    layout.split(Layout("foo", size=2), Layout("bar"))

    console = Console(width=60, color_system=None)

    with console.capture() as capture:
        console.print(layout.tree, height=10)
    result = capture.get()
    print(repr(result))
    expected = "⬇ 'root' (ratio=1)                                          \n├── ■ (size=2)                                              \n└── ■ (ratio=1)                                             \n"

    assert result == expected
