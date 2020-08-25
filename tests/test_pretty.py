from array import array
from collections import defaultdict
import io
import sys

from rich.console import Console
from rich.pretty import install, pretty_repr


def test_install():
    console = Console(file=io.StringIO())
    dh = sys.displayhook
    install(console)
    sys.displayhook("foo")
    assert console.file.getvalue() == "'foo'\n"
    assert sys.displayhook is not dh


def test_pretty():
    test = {
        "foo": [1, 2, 3, {4, 5, 6, (7, 8, 9)}, {}],
        "bar": {"egg": "baz", "words": ["Hello World"] * 10},
        False: "foo",
        True: "",
        "text": ("Hello World", "foo bar baz egg"),
    }

    result = pretty_repr(test, max_width=80)
    print(result)
    print(repr(result))
    expected = "{\n    'foo': [1, 2, 3, {(7, 8, 9), 4, 5, 6}, {}],\n    'bar': {\n        'egg': 'baz',\n        'words': [\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World'\n        ]\n    },\n    False: 'foo',\n    True: '',\n    'text': ('Hello World', 'foo bar baz egg')\n}"
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
