from array import array
from collections import defaultdict, UserDict, UserList
from dataclasses import dataclass, field
import io
import sys
from typing import List

import attr
import pytest

from rich.console import Console
from rich.pretty import install, Pretty, pprint, pretty_repr, Node


skip_py36 = pytest.mark.skipif(
    sys.version_info.minor == 6 and sys.version_info.major == 3,
    reason="rendered differently on py3.6",
)


def test_install():
    console = Console(file=io.StringIO())
    dh = sys.displayhook
    install(console)
    sys.displayhook("foo")
    assert console.file.getvalue() == "'foo'\n"
    assert sys.displayhook is not dh


def test_pretty():
    test = {
        "foo": [1, 2, 3, (4, 5, {6}, 7, 8, {9}), {}],
        "bar": {"egg": "baz", "words": ["Hello World"] * 10},
        False: "foo",
        True: "",
        "text": ("Hello World", "foo bar baz egg"),
    }

    result = pretty_repr(test, max_width=80)
    print(result)
    # print(repr(result))
    expected = "{\n    'foo': [1, 2, 3, (4, 5, {6}, 7, 8, {9}), {}],\n    'bar': {\n        'egg': 'baz',\n        'words': [\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World'\n        ]\n    },\n    False: 'foo',\n    True: '',\n    'text': ('Hello World', 'foo bar baz egg')\n}"
    print(expected)
    assert result == expected


@dataclass
class ExampleDataclass:
    foo: int
    bar: str
    ignore: int = field(repr=False)
    baz: List[str] = field(default_factory=list)


def test_pretty_dataclass():
    dc = ExampleDataclass(1000, "Hello, World", 999, ["foo", "bar", "baz"])
    result = pretty_repr(dc, max_width=80)
    print(repr(result))
    assert (
        result
        == "ExampleDataclass(foo=1000, bar='Hello, World', baz=['foo', 'bar', 'baz'])"
    )
    result = pretty_repr(dc, max_width=16)
    print(repr(result))
    assert (
        result
        == "ExampleDataclass(\n    foo=1000,\n    bar='Hello, World',\n    baz=[\n        'foo',\n        'bar',\n        'baz'\n    ]\n)"
    )
    dc.bar = dc
    result = pretty_repr(dc, max_width=80)
    print(repr(result))
    assert result == "ExampleDataclass(foo=1000, bar=..., baz=['foo', 'bar', 'baz'])"


def test_small_width():
    test = ["Hello world! 12345"]
    result = pretty_repr(test, max_width=10)
    expected = "[\n    'Hello world! 12345'\n]"
    assert result == expected


def test_broken_repr():
    class BrokenRepr:
        def __repr__(self):
            1 / 0

    test = [BrokenRepr()]
    result = pretty_repr(test)
    expected = "[<repr-error 'division by zero'>]"
    assert result == expected


def test_recursive():
    test = []
    test.append(test)
    result = pretty_repr(test)
    expected = "[...]"
    assert result == expected


def test_defaultdict():
    test_dict = defaultdict(int, {"foo": 2})
    result = pretty_repr(test_dict)
    assert result == "defaultdict(<class 'int'>, {'foo': 2})"


def test_array():
    test_array = array("I", [1, 2, 3])
    result = pretty_repr(test_array)
    assert result == "array('I', [1, 2, 3])"


def test_tuple_of_one():
    assert pretty_repr((1,)) == "(1,)"


def test_node():
    node = Node("abc")
    assert pretty_repr(node) == "abc: "


def test_indent_lines():
    console = Console(width=100, color_system=None)
    console.begin_capture()
    console.print(Pretty([100, 200], indent_guides=True), width=8)
    expected = """\
[
│   100,
│   200
]
"""
    result = console.end_capture()
    print(repr(result))
    print(result)
    assert result == expected


def test_pprint():
    console = Console(color_system=None)
    console.begin_capture()
    pprint(1, console=console)
    assert console.end_capture() == "1\n"


def test_pprint_max_values():
    console = Console(color_system=None)
    console.begin_capture()
    pprint([1, 2, 3, 4, 5, 6, 7, 8, 9, 0], console=console, max_length=2)
    assert console.end_capture() == "[1, 2, ... +8]\n"


def test_pprint_max_items():
    console = Console(color_system=None)
    console.begin_capture()
    pprint({"foo": 1, "bar": 2, "egg": 3}, console=console, max_length=2)
    assert console.end_capture() == """{'foo': 1, 'bar': 2, ... +1}\n"""


def test_pprint_max_string():
    console = Console(color_system=None)
    console.begin_capture()
    pprint(["Hello" * 20], console=console, max_string=8)
    assert console.end_capture() == """['HelloHel'+92]\n"""


def test_tuples():
    console = Console(color_system=None)
    console.begin_capture()
    pprint((1,), console=console)
    pprint((1,), expand_all=True, console=console)
    pprint(((1,),), expand_all=True, console=console)
    result = console.end_capture()
    print(repr(result))
    expected = "(1,)\n(\n│   1,\n)\n(\n│   (\n│   │   1,\n│   ),\n)\n"
    print(result)
    print("--")
    print(expected)
    assert result == expected


def test_newline():
    console = Console(color_system=None)
    console.begin_capture()
    console.print(Pretty((1,), insert_line=True, expand_all=True))
    result = console.end_capture()
    expected = "\n(\n    1,\n)\n"
    assert result == expected


def test_empty_repr():
    class Foo:
        def __repr__(self):
            return ""

    assert pretty_repr(Foo()) == ""


def test_attrs():
    @attr.define
    class Point:
        x: int
        y: int
        foo: str = attr.field(repr=str.upper)
        z: int = 0

    result = pretty_repr(Point(1, 2, foo="bar"))
    print(repr(result))
    expected = "Point(x=1, y=2, foo=BAR, z=0)"
    assert result == expected


def test_attrs_empty():
    @attr.define
    class Nada:
        pass

    result = pretty_repr(Nada())
    print(repr(result))
    expected = "Nada()"
    assert result == expected


@skip_py36
def test_attrs_broken():
    @attr.define
    class Foo:
        bar: int

    foo = Foo(1)
    del foo.bar
    result = pretty_repr(foo)
    print(repr(result))
    expected = "Foo(bar=AttributeError('bar'))"
    assert result == expected


def test_user_dict():
    class D1(UserDict):
        pass

    class D2(UserDict):
        def __repr__(self):
            return "FOO"

    d1 = D1({"foo": "bar"})
    d2 = D2({"foo": "bar"})
    result = pretty_repr(d1, expand_all=True)
    print(repr(result))
    assert result == "{\n    'foo': 'bar'\n}"
    result = pretty_repr(d2, expand_all=True)
    print(repr(result))
    assert result == "FOO"
