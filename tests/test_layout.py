import sys
import pytest

from rich.console import Console
from rich.layout import Layout, NoSplitter
from rich.panel import Panel


def test_rich_laylout():
    rich_repr = list(
        Layout(name="foo", size=2, minimum_size=10, ratio=2).__rich_repr__()
    )
    print(rich_repr)
    expected = [
        "Layout(",
        ("name", "foo"),
        ("size", 2),
        ("minimum_size", 2),
        ("ratio", 2),
        ")",
    ]
    assert rich_repr == expected


def test_no_layout():
    layout = Layout()
    with pytest.raises(NoSplitter):
        layout.split(Layout(), Layout(), splitter="nope")


def test_add_split():
    layout = Layout()
    layout.split(Layout(), Layout())
    assert len(layout.children) == 2
    layout.add_split(Layout(name="foo"))
    assert len(layout.children) == 3
    assert layout.children[2].name == "foo"


def test_unsplit():
    layout = Layout()
    layout.split(Layout(), Layout())
    assert len(layout.children) == 2

    layout.unsplit()
    assert len(layout.children) == 0


@pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")
def test_render():
    layout = Layout(name="root")
    repr(layout)

    layout.split_column(Layout(name="top"), Layout(name="bottom"))
    top = layout["top"]
    top.update(Panel("foo"))

    print(type(top._renderable))
    assert isinstance(top.renderable, Panel)
    layout["bottom"].split_row(Layout(name="left"), Layout(name="right"))

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
    print(repr(result))
    expected = "╭──────────────────────────────────────────────────────────╮\n│ foo                                                      │\n│                                                          │\n│                                                          │\n╰──────────────────────────────────────────────────────────╯\nfoobar                        ╭───── 'right' (30 x 5) ─────╮\n                              │                            │\n                              │    Layout(name='right')    │\n                              │                            │\n                              ╰────────────────────────────╯\n"
    assert result == expected


def test_tree():
    layout = Layout(name="root")
    layout.split(Layout("foo", size=2), Layout("bar", name="bar"))
    layout["bar"].split_row(Layout(), Layout())

    console = Console(width=60, color_system=None)

    with console.capture() as capture:
        console.print(layout.tree, height=10)
    result = capture.get()
    print(repr(result))
    expected = "⬍ Layout(name='root')                                       \n├── ⬍ Layout(size=2)                                        \n└── ⬌ Layout(name='bar')                                    \n    ├── ⬍ Layout()                                          \n    └── ⬍ Layout()                                          \n"

    assert result == expected
