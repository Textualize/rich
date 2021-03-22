from rich.console import Console
from rich.repr import rich_repr


@rich_repr
class Foo:
    def __init__(self, foo: str, bar: int = None):
        self.foo = foo
        self.bar = bar

    def __rich_repr__(self):
        yield self.foo
        yield "bar", self.bar, None


def test_rich_repr() -> None:
    assert (repr(Foo("hello"))) == "Foo('hello')"
    assert (repr(Foo("hello", bar=3))) == "Foo('hello', bar=3)"


def test_rich_pretty() -> None:
    console = Console()
    with console.capture() as capture:
        console.print(Foo("hello", bar=3))
    result = capture.get()
    expected = "Foo('hello', bar=3)\n"
    assert result == expected
