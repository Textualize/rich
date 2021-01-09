from rich.console import Console
from rich.tree import Tree


def test_render_single_node():
    tree = Tree("foo")
    console = Console(color_system=None, width=20)
    console.begin_capture()
    console.print(tree)
    assert console.end_capture() == "foo                 \n"


def test_render_single_branch():
    tree = Tree("foo")
    tree.add("bar")
    console = Console(color_system=None, width=20)
    console.begin_capture()
    console.print(tree)
    result = console.end_capture()
    print(repr(result))
    expected = "foo                 \n└── bar             \n"
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
    expected = "foo                 \n├── bar             \n└── baz             \n"
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
    expected = "foo                 \n+-- bar             \n`-- baz             \n"
    assert result == expected