import io

import pytest

from rich.console import Console
from rich.align import Align, VerticalCenter
from rich.measure import Measurement


def test_bad_align_legal():

    # Legal
    Align("foo", "left")
    Align("foo", "center")
    Align("foo", "right")

    # illegal
    with pytest.raises(ValueError):
        Align("foo", None)
    with pytest.raises(ValueError):
        Align("foo", "middle")
    with pytest.raises(ValueError):
        Align("foo", "")
    with pytest.raises(ValueError):
        Align("foo", "LEFT")


def test_repr():
    repr(Align("foo", "left"))
    repr(Align("foo", "center"))
    repr(Align("foo", "right"))


def test_align_left():
    console = Console(file=io.StringIO(), width=10)
    console.print(Align("foo", "left"))
    assert console.file.getvalue() == "foo       \n"


def test_align_center():
    console = Console(file=io.StringIO(), width=10)
    console.print(Align("foo", "center"))
    assert console.file.getvalue() == "   foo    \n"


def test_align_right():
    console = Console(file=io.StringIO(), width=10)
    console.print(Align("foo", "right"))
    assert console.file.getvalue() == "       foo\n"


def test_align_fit():
    console = Console(file=io.StringIO(), width=10)
    console.print(Align("foobarbaze", "center"))
    assert console.file.getvalue() == "foobarbaze\n"


def test_align_right_style():
    console = Console(
        file=io.StringIO(), width=10, color_system="truecolor", force_terminal=True
    )
    console.print(Align("foo", "right", style="on blue"))
    assert console.file.getvalue() == "\x1b[44m       \x1b[0m\x1b[44mfoo\x1b[0m\n"


def test_measure():
    console = Console(file=io.StringIO(), width=20)
    _min, _max = Measurement.get(console, Align("foo bar", "left"), 20)
    assert _min == 3
    assert _max == 7


def test_align_no_pad():
    console = Console(file=io.StringIO(), width=10)
    console.print(Align("foo", "center", pad=False))
    console.print(Align("foo", "left", pad=False))
    assert console.file.getvalue() == "   foo\nfoo\n"


def test_align_width():
    console = Console(file=io.StringIO(), width=40)
    words = "Deep in the human unconscious is a pervasive need for a logical universe that makes sense. But the real universe is always one step beyond logic"
    console.print(Align(words, "center", width=30))
    result = console.file.getvalue()
    expected = "     Deep in the human unconscious      \n     is a pervasive need for a          \n     logical universe that makes        \n     sense. But the real universe       \n     is always one step beyond          \n     logic                              \n"
    assert result == expected


def test_shortcuts():
    assert Align.left("foo").align == "left"
    assert Align.left("foo").renderable == "foo"
    assert Align.right("foo").align == "right"
    assert Align.right("foo").renderable == "foo"
    assert Align.center("foo").align == "center"
    assert Align.center("foo").renderable == "foo"


def test_vertical_center():
    console = Console(color_system=None, height=6)
    console.begin_capture()
    vertical_center = VerticalCenter("foo")
    repr(vertical_center)
    console.print(vertical_center)
    result = console.end_capture()
    print(repr(result))
    expected = "   \n   \nfoo\n   \n   \n   \n"
    assert result == expected
    assert Measurement.get(console, vertical_center) == Measurement(3, 3)
