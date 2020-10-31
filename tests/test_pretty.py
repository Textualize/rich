from array import array
from collections import defaultdict
import io
import sys

from rich.console import Console
from rich.pretty import install, Pretty, pprint, pretty_repr, Node


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
    print(repr(result))
    expected = "{\n    'foo': [1, 2, 3, (4, 5, {6}, 7, 8, {9}), {}],\n    'bar': {\n        'egg': 'baz',\n        'words': [\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World'\n        ]\n    },\n    False: 'foo',\n    True: '',\n    'text': ('Hello World', 'foo bar baz egg')\n}"
    assert result == expected


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
