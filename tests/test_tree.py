import sys

import pytest

from rich.console import Console
from rich.measure import Measurement
from rich.tree import Tree


def test_render_single_node():
    tree = Tree("foo")
    console = Console(color_system=None, width=20)
    console.begin_capture()
    console.print(tree)
    assert console.end_capture() == "foo\n"


def test_render_single_branch():
    tree = Tree("foo")
    tree.add("bar")
    console = Console(color_system=None, width=20)
    console.begin_capture()
    console.print(tree)
    result = console.end_capture()
    print(repr(result))
    expected = "foo\n└── bar\n"
    assert result == expected


def test_render_double_branch():
    tree = Tree("foo")
    tree.add("bar")
    tree.add("baz")
    console = Console(color_system=None, width=20)
    console.begin_capture()
    console.print(tree)
    result = console.end_capture()
    print(repr(result))
    expected = "foo\n├── bar\n└── baz\n"
    assert result == expected


def test_render_ascii():
    tree = Tree("foo")
    tree.add("bar")
    tree.add("baz")

    class AsciiConsole(Console):
        @property
        def encoding(self):
            return "ascii"

    console = AsciiConsole(color_system=None, width=20)
    console.begin_capture()
    console.print(tree)
    result = console.end_capture()
    expected = "foo\n+-- bar\n`-- baz\n"
    assert result == expected


@pytest.mark.skipif(sys.platform == "win32", reason="different on Windows")
def test_render_tree_non_win32():
    tree = Tree("foo")
    tree.add("bar", style="italic")
    baz_tree = tree.add("baz", guide_style="bold red", style="on blue")
    baz_tree.add("1")
    baz_tree.add("2")
    tree.add("egg")

    console = Console(
        width=20, force_terminal=True, color_system="standard", _environ={}
    )
    console.begin_capture()
    console.print(tree)
    result = console.end_capture()
    print(repr(result))
    expected = "foo\n├── \x1b[3mbar\x1b[0m\n\x1b[44m├── \x1b[0m\x1b[44mbaz\x1b[0m\n\x1b[44m│   \x1b[0m\x1b[31;44m┣━━ \x1b[0m\x1b[44m1\x1b[0m\n\x1b[44m│   \x1b[0m\x1b[31;44m┗━━ \x1b[0m\x1b[44m2\x1b[0m\n└── egg\n"
    assert result == expected


@pytest.mark.skipif(sys.platform != "win32", reason="Windows specific")
def test_render_tree_win32():
    tree = Tree("foo")
    tree.add("bar", style="italic")
    baz_tree = tree.add("baz", guide_style="bold red", style="on blue")
    baz_tree.add("1")
    baz_tree.add("2")
    tree.add("egg")

    console = Console(
        width=20, force_terminal=True, color_system="standard", legacy_windows=True
    )
    console.begin_capture()
    console.print(tree)
    result = console.end_capture()
    print(repr(result))
    expected = "foo\n├── \x1b[3mbar\x1b[0m\n\x1b[44m├── \x1b[0m\x1b[44mbaz\x1b[0m\n\x1b[44m│   \x1b[0m\x1b[31;44m├── \x1b[0m\x1b[44m1\x1b[0m\n\x1b[44m│   \x1b[0m\x1b[31;44m└── \x1b[0m\x1b[44m2\x1b[0m\n└── egg\n"
    assert result == expected


@pytest.mark.skipif(sys.platform == "win32", reason="different on Windows")
def test_render_tree_hide_root_non_win32():
    tree = Tree("foo", hide_root=True)
    tree.add("bar", style="italic")
    baz_tree = tree.add("baz", guide_style="bold red", style="on blue")
    baz_tree.add("1")
    baz_tree.add("2")
    tree.add("egg")

    console = Console(
        width=20, force_terminal=True, color_system="standard", _environ={}
    )
    console.begin_capture()
    console.print(tree)
    result = console.end_capture()
    print(repr(result))
    expected = "\x1b[3mbar\x1b[0m\n\x1b[44mbaz\x1b[0m\n\x1b[31;44m┣━━ \x1b[0m\x1b[44m1\x1b[0m\n\x1b[31;44m┗━━ \x1b[0m\x1b[44m2\x1b[0m\negg\n"
    assert result == expected


@pytest.mark.skipif(sys.platform != "win32", reason="Windows specific")
def test_render_tree_hide_root_win32():
    tree = Tree("foo", hide_root=True)
    tree.add("bar", style="italic")
    baz_tree = tree.add("baz", guide_style="bold red", style="on blue")
    baz_tree.add("1")
    baz_tree.add("2")
    tree.add("egg")

    console = Console(width=20, force_terminal=True, color_system="standard")
    console.begin_capture()
    console.print(tree)
    result = console.end_capture()
    print(repr(result))
    expected = "\x1b[3mbar\x1b[0m\n\x1b[44mbaz\x1b[0m\n\x1b[31;44m├── \x1b[0m\x1b[44m1\x1b[0m\n\x1b[31;44m└── \x1b[0m\x1b[44m2\x1b[0m\negg\n"
    assert result == expected


def test_tree_measure():
    tree = Tree("foo")
    tree.add("bar")
    tree.add("mushroom risotto")
    console = Console()
    measurement = Measurement.get(console, console.options, tree)
    assert measurement == Measurement(12, 20)
