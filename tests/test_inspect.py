import io
import sys

import pytest

from rich import inspect
from rich.console import Console


skip_py36 = pytest.mark.skipif(
    sys.version_info.minor == 6 and sys.version_info.major == 3,
    reason="rendered differently on py3.6",
)


skip_py37 = pytest.mark.skipif(
    sys.version_info.minor == 7 and sys.version_info.major == 3,
    reason="rendered differently on py3.7",
)


def render(obj, methods=False) -> str:
    console = Console(file=io.StringIO(), width=50, legacy_windows=False)
    inspect(obj, console=console, methods=methods)
    return console.file.getvalue()


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
    expected = "╭────────────── <class 'tests.test_inspect.Foo'> ──────────────╮\n│ Foo test                                                     │\n│                                                              │\n│   broken = InspectError()                                    │\n│ __init__ = def __init__(foo: int) -> None: constructor docs. │\n│   method = def method(a, b) -> str: Multi line               │\n╰──────────────────────────────────────────────────────────────╯\n"
    assert expected == result


def test_inspect_text():

    expected = (
        "╭──────────────── <class 'str'> ─────────────────╮\n"
        "│ str(object='') -> str                          │\n"
        "│ str(bytes_or_buffer[, encoding[, errors]]) ->  │\n"
        "│ str                                            │\n"
        "│                                                │\n"
        "│ 33 attribute(s) not shown. Use                 │\n"
        "│ inspect(<OBJECT>, all=True) to see all         │\n"
        "│ attributes.                                    │\n"
        "╰────────────────────────────────────────────────╯\n"
    )
    assert expected == render("Hello")


@skip_py36
@skip_py37
def test_inspect_empty_dict():

    expected = (
        "╭──────────────── <class 'dict'> ────────────────╮\n"
        "│ dict() -> new empty dictionary                 │\n"
        "│ dict(mapping) -> new dictionary initialized    │\n"
        "│ from a mapping object's                        │\n"
        "│     (key, value) pairs                         │\n"
        "│ dict(iterable) -> new dictionary initialized   │\n"
        "│ as if via:                                     │\n"
        "│     d = {}                                     │\n"
        "│     for k, v in iterable:                      │\n"
        "│         d[k] = v                               │\n"
        "│ dict(**kwargs) -> new dictionary initialized   │\n"
        "│ with the name=value pairs                      │\n"
        "│     in the keyword argument list.  For         │\n"
        "│ example:  dict(one=1, two=2)                   │\n"
        "│                                                │\n"
    )
    assert render({}).startswith(expected)


def test_inspect_builtin_function():

    expected = (
        "╭────────── <built-in function print> ───────────╮\n"
        "│ def print(...)                                 │\n"
        "│                                                │\n"
        "│ print(value, ..., sep=' ', end='\\n',           │\n"
        "│ file=sys.stdout, flush=False)                  │\n"
        "│                                                │\n"
        "│ 29 attribute(s) not shown. Use                 │\n"
        "│ inspect(<OBJECT>, all=True) to see all         │\n"
        "│ attributes.                                    │\n"
        "╰────────────────────────────────────────────────╯\n"
    )
    assert expected == render(print)


@skip_py36
def test_inspect_integer():

    expected = (
        "╭────── <class 'int'> ───────╮\n"
        "│ int([x]) -> integer        │\n"
        "│ int(x, base=10) -> integer │\n"
        "│                            │\n"
        "│ denominator = 1            │\n"
        "│        imag = 0            │\n"
        "│   numerator = 1            │\n"
        "│        real = 1            │\n"
        "╰────────────────────────────╯\n"
    )
    assert expected == render(1)


@skip_py36
@skip_py37
def test_inspect_integer_with_methods():

    expected = (
        "╭──────────────── <class 'int'> ─────────────────╮\n"
        "│ int([x]) -> integer                            │\n"
        "│ int(x, base=10) -> integer                     │\n"
        "│                                                │\n"
        "│      denominator = 1                           │\n"
        "│             imag = 0                           │\n"
        "│        numerator = 1                           │\n"
        "│             real = 1                           │\n"
        "│ as_integer_ratio = def as_integer_ratio():     │\n"
        "│                    Return integer ratio.       │\n"
        "│       bit_length = def bit_length(): Number of │\n"
        "│                    bits necessary to represent │\n"
        "│                    self in binary.             │\n"
        "│        conjugate = def conjugate(...) Returns  │\n"
        "│                    self, the complex conjugate │\n"
        "│                    of any int.                 │\n"
        "│       from_bytes = def from_bytes(bytes,       │\n"
        "│                    byteorder, *,               │\n"
        "│                    signed=False): Return the   │\n"
        "│                    integer represented by the  │\n"
        "│                    given array of bytes.       │\n"
        "│         to_bytes = def to_bytes(length,        │\n"
        "│                    byteorder, *,               │\n"
        "│                    signed=False): Return an    │\n"
        "│                    array of bytes representing │\n"
        "│                    an integer.                 │\n"
        "╰────────────────────────────────────────────────╯\n"
    )
    assert expected == render(1, methods=True)
