import io

from rich.console import Console
from rich.text import Text


class Foo:
    def __rich__(self):
        return Text("Foo")


def test_rich_case():
    foo = Foo()
    console = Console(file=io.StringIO())
    console.print(foo)
    assert console.file.getvalue() == "Foo\n"
