import sys
from typing import Optional

import pytest

import rich.repr
from rich.console import Console

skip_py36 = pytest.mark.skipif(
    sys.version_info.minor == 6 and sys.version_info.major == 3,
    reason="rendered differently on py3.6",
)

skip_py37 = pytest.mark.skipif(
    sys.version_info.minor == 7 and sys.version_info.major == 3,
    reason="rendered differently on py3.7",
)


@rich.repr.auto
class Foo:
    def __init__(self, foo: str, bar: Optional[int] = None, egg: int = 1):
        self.foo = foo
        self.bar = bar
        self.egg = egg

    def __rich_repr__(self):
        yield self.foo
        yield None, self.foo,
        yield "bar", self.bar, None
        yield "egg", self.egg


@rich.repr.auto
class Egg:
    def __init__(self, foo: str, bar: Optional[int] = None, egg: int = 1):
        self.foo = foo
        self.bar = bar
        self.egg = egg


@rich.repr.auto
class BrokenEgg:
    def __init__(self, foo: str, *, bar: Optional[int] = None, egg: int = 1):
        self.foo = foo
        self.fubar = bar
        self.egg = egg


@rich.repr.auto(angular=True)
class AngularEgg:
    def __init__(self, foo: str, *, bar: Optional[int] = None, egg: int = 1):
        self.foo = foo
        self.bar = bar
        self.egg = egg


@rich.repr.auto
class Bar(Foo):
    def __rich_repr__(self):
        yield (self.foo,)
        yield None, self.foo,
        yield "bar", self.bar, None
        yield "egg", self.egg

    __rich_repr__.angular = True


def test_rich_repr() -> None:
    assert (repr(Foo("hello"))) == "Foo('hello', 'hello', egg=1)"
    assert (repr(Foo("hello", bar=3))) == "Foo('hello', 'hello', bar=3, egg=1)"


@skip_py36
@skip_py37
def test_rich_repr_positional_only() -> None:
    _locals = locals().copy()
    exec(
        """\
@rich.repr.auto
class PosOnly:
    def __init__(self, foo, /):
        self.foo = 1
    """,
        globals(),
        _locals,
    )
    p = _locals["PosOnly"](1)
    assert repr(p) == "PosOnly(1)"


def test_rich_angular() -> None:
    assert (repr(Bar("hello"))) == "<Bar 'hello' 'hello' egg=1>"
    assert (repr(Bar("hello", bar=3))) == "<Bar 'hello' 'hello' bar=3 egg=1>"


def test_rich_repr_auto() -> None:
    assert repr(Egg("hello", egg=2)) == "Egg('hello', egg=2)"


def test_rich_repr_auto_angular() -> None:
    assert repr(AngularEgg("hello", egg=2)) == "<AngularEgg 'hello' egg=2>"


def test_broken_egg() -> None:
    with pytest.raises(rich.repr.ReprError):
        repr(BrokenEgg("foo"))


def test_rich_pretty() -> None:
    console = Console()
    with console.capture() as capture:
        console.print(Foo("hello", bar=3))
    result = capture.get()
    expected = "Foo('hello', 'hello', bar=3, egg=1)\n"
    assert result == expected


def test_rich_pretty_angular() -> None:
    console = Console()
    with console.capture() as capture:
        console.print(Bar("hello", bar=3))
    result = capture.get()
    expected = "<Bar 'hello' 'hello' bar=3 egg=1>\n"
    assert result == expected
