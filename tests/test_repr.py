from rich.console import Console
from rich.repr import rich_repr


@rich_repr
class Foo:
    def __init__(self, foo: str, bar: int = None, egg: int = 1):
        self.foo = foo
        self.bar = bar
        self.egg = egg

    def __rich_repr__(self):
        yield self.foo
        yield self.foo,
        yield "bar", self.bar, None
        yield "egg", self.egg


def test_rich_repr() -> None:
    assert (repr(Foo("hello"))) == "Foo('hello', 'hello', egg=1)"
    assert (repr(Foo("hello", bar=3))) == "Foo('hello', 'hello', bar=3, egg=1)"


def test_rich_pretty() -> None:
    console = Console()
    with console.capture() as capture:
        console.print(Foo("hello", bar=3))
    result = capture.get()
    expected = "Foo('hello', 'hello', bar=3, egg=1)\n"
    assert result == expected
