import io
import sys
from array import array
from collections import defaultdict, UserDict
from typing import List

import attr
import pytest
from dataclasses import dataclass, field

from rich.console import Console
from rich.pretty import install, Pretty, pprint, pretty_repr, Node, _ipy_display_hook
from rich.text import Text

skip_py36 = pytest.mark.skipif(
    sys.version_info.minor == 6 and sys.version_info.major == 3,
    reason="rendered differently on py3.6",
)

skip_py37 = pytest.mark.skipif(
    sys.version_info.minor == 7 and sys.version_info.major == 3,
    reason="rendered differently on py3.7",
)
skip_py38 = pytest.mark.skipif(
    sys.version_info.minor == 8 and sys.version_info.major == 3,
    reason="rendered differently on py3.8",
)
skip_py39 = pytest.mark.skipif(
    sys.version_info.minor == 9 and sys.version_info.major == 3,
    reason="rendered differently on py3.9",
)
skip_py310 = pytest.mark.skipif(
    sys.version_info.minor == 10 and sys.version_info.major == 3,
    reason="rendered differently on py3.10",
)


def test_install():
    console = Console(file=io.StringIO())
    dh = sys.displayhook
    install(console)
    sys.displayhook("foo")
    assert console.file.getvalue() == "'foo'\n"
    assert sys.displayhook is not dh


def test_ipy_display_hook__repr_html():
    console = Console(file=io.StringIO(), force_jupyter=True)

    class Thing:
        def _repr_html_(self):
            return "hello"

    console.begin_capture()
    _ipy_display_hook(Thing(), console=console)

    # Rendering delegated to notebook because _repr_html_ method exists
    assert console.end_capture() == ""


def test_ipy_display_hook__multiple_special_reprs():
    """
    The case where there are multiple IPython special _repr_*_
    methods on the object, and one of them returns None but another
    one does not.
    """
    console = Console(file=io.StringIO(), force_jupyter=True)

    class Thing:
        def _repr_latex_(self):
            return None

        def _repr_html_(self):
            return "hello"

    console.begin_capture()
    _ipy_display_hook(Thing(), console=console)

    assert console.end_capture() == ""


def test_ipy_display_hook__no_special_repr_methods():
    console = Console(file=io.StringIO(), force_jupyter=True)

    class Thing:
        def __repr__(self) -> str:
            return "hello"

    console.begin_capture()
    _ipy_display_hook(Thing(), console=console)

    # No IPython special repr methods, so printed by Rich
    assert console.end_capture() == "hello\n"


def test_ipy_display_hook__special_repr_raises_exception():
    """
    When an IPython special repr method raises an exception,
    we treat it as if it doesn't exist and look for the next.
    """
    console = Console(file=io.StringIO(), force_jupyter=True)

    class Thing:
        def _repr_markdown_(self):
            raise Exception()

        def _repr_latex_(self):
            return None

        def _repr_html_(self):
            return "hello"

    console.begin_capture()
    _ipy_display_hook(Thing(), console=console)

    assert console.end_capture() == ""


def test_ipy_display_hook__console_renderables_on_newline():
    console = Console(file=io.StringIO(), force_jupyter=True)
    console.begin_capture()
    _ipy_display_hook(Text("hello"), console=console)
    assert console.end_capture() == "\nhello\n"


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
    expected = "{\n    'foo': [1, 2, 3, (4, 5, {6}, 7, 8, {9}), {}],\n    'bar': {\n        'egg': 'baz',\n        'words': [\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World',\n            'Hello World'\n        ]\n    },\n    False: 'foo',\n    True: '',\n    'text': ('Hello World', 'foo bar baz egg')\n}"
    print(expected)
    assert result == expected


@dataclass
class ExampleDataclass:
    foo: int
    bar: str
    ignore: int = field(repr=False)
    baz: List[str] = field(default_factory=list)
    last: int = field(default=1, repr=False)


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


@skip_py36
def test_broken_repr():
    class BrokenRepr:
        def __repr__(self):
            1 / 0

    test = [BrokenRepr()]
    result = pretty_repr(test)
    expected = "[<repr-error 'division by zero'>]"
    assert result == expected


@skip_py36
def test_broken_getattr():
    class BrokenAttr:
        def __getattr__(self, name):
            1 / 0

        def __repr__(self):
            return "BrokenAttr()"

    test = BrokenAttr()
    result = pretty_repr(test)
    assert result == "BrokenAttr()"


def test_recursive():
    test = []
    test.append(test)
    result = pretty_repr(test)
    expected = "[...]"
    assert result == expected


def test_max_depth():
    d = {}
    d["foo"] = {"fob": {"a": [1, 2, 3], "b": {"z": "x", "y": ["a", "b", "c"]}}}

    assert pretty_repr(d, max_depth=0) == "..."
    assert pretty_repr(d, max_depth=1) == "{'foo': ...}"
    assert pretty_repr(d, max_depth=2) == "{'foo': {'fob': ...}}"
    assert pretty_repr(d, max_depth=3) == "{'foo': {'fob': {'a': ..., 'b': ...}}}"
    assert (
        pretty_repr(d, max_width=100, max_depth=4)
        == "{'foo': {'fob': {'a': [1, 2, 3], 'b': {'z': 'x', 'y': ...}}}}"
    )
    assert (
        pretty_repr(d, max_width=100, max_depth=5)
        == "{'foo': {'fob': {'a': [1, 2, 3], 'b': {'z': 'x', 'y': ['a', 'b', 'c']}}}}"
    )
    assert (
        pretty_repr(d, max_width=100, max_depth=None)
        == "{'foo': {'fob': {'a': [1, 2, 3], 'b': {'z': 'x', 'y': ['a', 'b', 'c']}}}}"
    )


def test_max_depth_rich_repr():
    class Foo:
        def __init__(self, foo):
            self.foo = foo

        def __rich_repr__(self):
            yield "foo", self.foo

    class Bar:
        def __init__(self, bar):
            self.bar = bar

        def __rich_repr__(self):
            yield "bar", self.bar

    assert (
        pretty_repr(Foo(foo=Bar(bar=Foo(foo=[]))), max_depth=2)
        == "Foo(foo=Bar(bar=...))"
    )


def test_max_depth_attrs():
    @attr.define
    class Foo:
        foo = attr.field()

    @attr.define
    class Bar:
        bar = attr.field()

    assert (
        pretty_repr(Foo(foo=Bar(bar=Foo(foo=[]))), max_depth=2)
        == "Foo(foo=Bar(bar=...))"
    )


def test_max_depth_dataclass():
    @dataclass
    class Foo:
        foo: object

    @dataclass
    class Bar:
        bar: object

    assert (
        pretty_repr(Foo(foo=Bar(bar=Foo(foo=[]))), max_depth=2)
        == "Foo(foo=Bar(bar=...))"
    )


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
@skip_py310
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


@skip_py36
@skip_py37
@skip_py38
@skip_py39
def test_attrs_broken_310():
    @attr.define
    class Foo:
        bar: int

    foo = Foo(1)
    del foo.bar
    result = pretty_repr(foo)
    print(repr(result))
    expected = "Foo(bar=AttributeError(\"'Foo' object has no attribute 'bar'\"))"
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


def test_lying_attribute():
    """Test getattr doesn't break rich repr protocol"""

    class Foo:
        def __getattr__(self, attr):
            return "foo"

    foo = Foo()
    result = pretty_repr(foo)
    assert "Foo" in result
