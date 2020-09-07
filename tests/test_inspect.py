import io
import sys

import pytest

from rich import inspect
from rich.console import Console


skip_py36 = pytest.mark.skipif(
    sys.version_info.minor == 6 and sys.version_info.major == 3,
    reason="rendered differently on py3.6",
)


class InspectError(Exception):
    def __str__(self) -> str:
        return "INSPECT ERROR"


class Foo:
    """Foo test

    Second line
    """

    def __init__(self, foo: int) -> None:
        """constructor docs."""
        self.foo = foo

    @property
    def broken(self):
        raise InspectError()

    def method(self, a, b) -> str:
        """Multi line

        docs.
        """
        return "test"

    def __dir__(self):
        return ["__init__", "broken", "method"]


@skip_py36
def test_render():
    console = Console(width=100, file=io.StringIO(), legacy_windows=False)

    foo = Foo("hello")
    inspect(foo, console=console, all=True)
    result = console.file.getvalue()
    print(repr(result))
    expected = "╭──────────── <class 'tests.test_inspect.Foo'> ────────────╮\n│ Foo test                                                 │\n│                                                          │\n│   broken = InspectError()                                │\n│ __init__ = __init__(foo: int) -> None: constructor docs. │\n│   method = method(a, b) -> str: Multi line               │\n╰──────────────────────────────────────────────────────────╯\n"
    assert expected == result
