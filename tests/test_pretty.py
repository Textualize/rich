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
        False: "foo",
        True: "",
        "text": ("Hello World", "foo bar baz egg"),
    }

    result = pretty_repr(test)
    expected = "{\n    'foo': [1, 2, 3, {(7, 8, 9), 4, 5, 6}, {}], \n    False: 'foo', \n    True: '', \n    'text': ('Hello World', 'foo bar baz egg')\n}"
    assert result.plain == expected


def test_small_width():
    test = ["Hello world! 12345"]
    result = pretty_repr(test, max_width=10)
    expected = "[\n    'Hello world! 12345'\n]"
    assert result.plain == expected


def test_broken_repr():
    class BrokenRepr:
        def __repr__(self):
            1 / 0

    test = [BrokenRepr()]
    result = pretty_repr(test)
    expected = "[<error in repr: division by zero>]"
    assert result.plain == expected


def test_recursive():
    test = []
    test.append(test)
    result = pretty_repr(test)
    expected = "[...]"
    assert result.plain == expected
