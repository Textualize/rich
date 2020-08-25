import io

from rich.console import Console
from rich.panel import Panel
from rich.text import Text


class Foo:
    def __rich__(self):
        return Text("Foo")


def test_rich_cast():
    foo = Foo()
    console = Console(file=io.StringIO())
    console.print(foo)
    assert console.file.getvalue() == "Foo\n"


def test_rich_cast_container():
    foo = Foo()
    console = Console(file=io.StringIO(), legacy_windows=False)
    console.print(Panel.fit(foo))
    assert console.file.getvalue() == "╭───╮\n│Foo│\n╰───╯\n"
