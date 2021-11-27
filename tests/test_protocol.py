import io

from rich.abc import RichRenderable
from rich.console import Console
from rich.panel import Panel
from rich.text import Text


class Foo:
    def __rich__(self) -> Text:
        return Text("Foo")


def test_rich_cast():
    foo = Foo()
    console = Console(file=io.StringIO())
    console.print(foo)
    assert console.file.getvalue() == "Foo\n"


class Fake:
    def __getattr__(self, name):
        return 12

    def __repr__(self) -> str:
        return "Fake()"


def test_rich_cast_fake():
    fake = Fake()
    console = Console(file=io.StringIO())
    console.print(fake)
    assert console.file.getvalue() == "Fake()\n"


def test_rich_cast_container():
    foo = Foo()
    console = Console(file=io.StringIO(), legacy_windows=False)
    console.print(Panel.fit(foo, padding=0))
    assert console.file.getvalue() == "╭───╮\n│Foo│\n╰───╯\n"


def test_abc():
    foo = Foo()
    assert isinstance(foo, RichRenderable)
    assert isinstance(Text("hello"), RichRenderable)
    assert isinstance(Panel("hello"), RichRenderable)
    assert not isinstance(foo, str)
    assert not isinstance("foo", RichRenderable)
    assert not isinstance([], RichRenderable)


def test_cast_deep():
    class B:
        def __rich__(self) -> Foo:
            return Foo()

    class A:
        def __rich__(self) -> B:
            return B()

    console = Console(file=io.StringIO())
    console.print(A())
    assert console.file.getvalue() == "Foo\n"


def test_cast_recursive():
    class B:
        def __rich__(self) -> "A":
            return A()

        def __repr__(self) -> str:
            return "<B>"

    class A:
        def __rich__(self) -> B:
            return B()

        def __repr__(self) -> str:
            return "<A>"

    console = Console(file=io.StringIO())
    console.print(A())
    assert console.file.getvalue() == "<B>\n"
