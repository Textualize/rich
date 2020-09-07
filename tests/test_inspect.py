import io


from rich import inspect
from rich.console import Console


class Foo:
    """Foo test

    Second line
    """

    def __init__(self, foo: int) -> None:
        """constructor docs."""
        self.foo = foo

    @property
    def broken(self):
        1 / 0

    def method(self, a, b) -> str:
        """Multi line

        docs.
        """
        return "test"

    def __dir__(self):
        return ["__init__", "broken", "method"]


def test_render():
    console = Console(width=100, file=io.StringIO(), legacy_windows=False)

    foo = Foo("hello")
    inspect(foo, console=console, all=True)
    result = console.file.getvalue()
    print(repr(result))
    expected = "╭──────────── <class 'tests.test_inspect.Foo'> ────────────╮\n│ Foo test                                                 │\n│                                                          │\n│   broken = ZeroDivisionError('division by zero')         │\n│ __init__ = __init__(foo: int) -> None: constructor docs. │\n│   method = method(a, b) -> str: Multi line               │\n╰──────────────────────────────────────────────────────────╯\n"
    assert expected == result
