from io import StringIO
import pytest

from rich.console import Console
from rich.text import Span, Text
from rich.render_width import RenderWidth


def test_span():
    span = Span(1, 10, "foo")
    repr(span)
    assert bool(span)
    assert not Span(10, 10, "foo")


def test_span_split():
    assert Span(5, 10, "foo").split(2) == (Span(5, 10, "foo"), None)
    assert Span(5, 10, "foo").split(15) == (Span(5, 10, "foo"), None)
    assert Span(0, 10, "foo").split(5) == (Span(0, 5, "foo"), Span(5, 10, "foo"))


def test_span_move():
    assert Span(5, 10, "foo").move(2) == Span(7, 12, "foo")


def test_span_right_crop():
    assert Span(5, 10, "foo").right_crop(15) == Span(5, 10, "foo")
    assert Span(5, 10, "foo").right_crop(7) == Span(5, 7, "foo")


def test_len():
    assert len(Text("foo")) == 3


def test_bool():
    assert Text("foo")
    assert not Text("")


def test_str():
    assert str(Text("foo")) == "foo"


def test_repr():
    assert isinstance(repr(Text("foo")), str)


def test_add():
    text = Text("foo") + Text("bar")
    assert str(text) == "foobar"
    assert Text("foo").__add__(1) == NotImplemented


def test_eq():
    assert Text("foo") == Text("foo")
    assert Text("foo") != Text("bar")
    assert Text("foo").__eq__(1) == NotImplemented


def test_text_property():
    text = Text("foo")
    text.append("bar")
    text.append("baz")
    assert text.text == "foobarbaz"


def test_text_property_setter():
    test = Text("foo")
    test.text = "bar"
    assert str(test) == "bar"
    test = Text()
    test.append("Hello, World", "bold")
    test.text = "Hello"
    assert str(test) == "Hello"
    assert test._spans == [Span(0, 5, "bold")]


def test_from_markup():
    text = Text.from_markup("Hello, [bold]World![/bold]")
    assert str(text) == "Hello, World!"
    assert text._spans == [Span(7, 13, "bold")]


def test_copy():
    test = Text()
    test.append("Hello", "bold")
    test.append(" ")
    test.append("World", "italic")
    test_copy = test.copy()
    assert test == test_copy
    assert test is not test_copy


def test_rstrip():
    test = Text("Hello, World!    ")
    test.rstrip()
    assert str(test) == "Hello, World!"


def test_stylize():
    test = Text("Hello, World!")
    test.stylize(7, 11, "bold")
    assert test._spans == [Span(7, 11, "bold")]
    test.stylize(20, 25, "bold")
    assert test._spans == [Span(7, 11, "bold")]


def test_set_length():
    test = Text("Hello")
    test.set_length(5)
    assert test == Text("Hello")

    test = Text("Hello")
    test.set_length(10)
    assert test == Text("Hello     ")

    test = Text("Hello World")
    test.stylize(0, 5, "bold")
    test.stylize(7, 9, "italic")

    test.set_length(3)
    expected = Text()
    expected.append("Hel", "bold")
    assert test == expected


def test_console_width():
    test = Text("Hello World!\nfoobarbaz")
    assert test.__console_width__(80) == RenderWidth(9, 12)
    assert Text(" " * 4).__console_width__(80) == RenderWidth(4, 4)


def test_join():
    test = Text("bar").join([Text("foo", "red"), Text("baz", "blue")])
    assert str(test) == "foobarbaz"
    assert test._spans == [Span(0, 3, "red"), Span(3, 6, ""), Span(6, 9, "blue")]


def test_trim_spans():
    test = Text("Hello")
    test._spans[:] = [Span(0, 3, "red"), Span(3, 6, "green"), Span(6, 9, "blue")]
    test._trim_spans()
    assert test._spans == [Span(0, 3, "red"), Span(3, 5, "green")]


def test_pad_left():
    test = Text("foo")
    test.pad_left(3, "X")
    assert str(test) == "XXXfoo"


def test_pad_right():
    test = Text("foo")
    test.pad_right(3, "X")
    assert str(test) == "fooXXX"


def test_append():
    test = Text("foo")
    test.append("bar")
    assert str(test) == "foobar"
    test.append(Text("baz", "bold"))
    assert str(test) == "foobarbaz"
    assert test._spans == [Span(6, 9, "bold")]

    with pytest.raises(ValueError):
        test.append(Text("foo"), "bar")

    with pytest.raises(TypeError):
        test.append(1)


def test_split():
    test = Text()
    test.append("foo", "red")
    test.append("\n")
    test.append("bar", "green")
    test.append("\n")

    line1 = Text()
    line1.append("foo", "red")
    line2 = Text()
    line2.append("bar", "green")
    split = test.split("\n")
    assert len(split) == 2
    assert split[0] == line1
    assert split[1] == line2

    assert list(Text("foo").split("\n")) == [Text("foo")]


def test_divide():
    lines = Text("foo").divide([])
    assert len(lines) == 1
    assert lines[0] == Text("foo")

    text = Text()
    text.append("foo", "bold")
    lines = text.divide([1, 2])
    assert len(lines) == 3
    assert str(lines[0]) == "f"
    assert str(lines[1]) == "o"
    assert str(lines[2]) == "o"
    assert lines[0]._spans == [Span(0, 1, "bold")]
    assert lines[1]._spans == [Span(0, 1, "bold")]
    assert lines[2]._spans == [Span(0, 1, "bold")]

    text = Text()
    text.append("foo", "red")
    text.append("bar", "green")
    text.append("baz", "blue")
    lines = text.divide([8])
    assert len(lines) == 2
    assert str(lines[0]) == "foobarba"
    assert str(lines[1]) == "z"
    assert lines[0]._spans == [
        Span(0, 3, "red"),
        Span(3, 6, "green"),
        Span(6, 8, "blue"),
    ]
    assert lines[1]._spans == [Span(0, 1, "blue")]

    lines = text.divide([1])
    assert len(lines) == 2
    assert str(lines[0]) == "f"
    assert str(lines[1]) == "oobarbaz"
    assert lines[0]._spans == [Span(0, 1, "red")]
    assert lines[1]._spans == [
        Span(0, 2, "red"),
        Span(2, 5, "green"),
        Span(5, 8, "blue"),
    ]


def test_right_crop():
    test = Text()
    test.append("foobar", "red")
    test.right_crop(3)
    assert str(test) == "foo"
    assert test._spans == [Span(0, 3, "red")]


def test_wrap():
    test = Text("foo bar baz")
    lines = test.wrap(4)
    print(list(lines))
    assert len(lines) == 3
    assert lines[0] == Text("foo ")
    assert lines[1] == Text("bar ")
    assert lines[2] == Text("baz ")

    lines = test.wrap(3)
    print(list(lines))
    assert len(lines) == 3
    assert lines[0] == Text("foo")
    assert lines[1] == Text("bar")
    assert lines[2] == Text("baz")


def test_fit():
    test = Text("Hello\nWorld")
    lines = test.fit(3)
    assert str(lines[0]) == "Hel"
    assert str(lines[1]) == "Wor"


def test_render():
    console = Console(width=15, record=True)
    test = Text.from_markup(
        "[u][b]Where[/b] there is a [i]Will[/i], there is a Way.[/u]"
    )
    console.print(test)
    output = console.export_text(styles=True)
    expected = "\x1b[1;4mWhere\x1b[0m\x1b[4m there is \x1b[0m\n\x1b[0m\x1b[4ma \x1b[0m\x1b[3;4mWill\x1b[0m\x1b[4m, there \x1b[0m\n\x1b[0m\x1b[4mis a Way.\x1b[0m\n\x1b[0m"
    assert output == expected


@pytest.mark.parametrize(
    "print_text,result",
    [
        (("."), ".\n"),
        ((".", "."), ". .\n"),
        (("Hello", "World", "!"), "Hello World !\n"),
    ],
)
def test_print(print_text, result):
    console = Console(record=True)
    console.print(*print_text)
    assert console.export_text(styles=False) == result


@pytest.mark.parametrize(
    "print_text,result",
    [(("."), ".X"), ((".", "."), "..X"), (("Hello", "World", "!"), "HelloWorld!X"),],
)
def test_print_sep_end(print_text, result):
    console = Console(record=True, file=StringIO())
    console.print(*print_text, sep="", end="X")
    assert console.file.getvalue() == result


def test_tabs_to_spaces():
    test = Text("\tHello\tWorld", tab_size=8)
    assert test.tabs_to_spaces().text == "        Hello   World"

    test = Text("\tHello\tWorld", tab_size=4)
    assert test.tabs_to_spaces().text == "    Hello   World"

    test = Text(".\t..\t...\t....\t", tab_size=4)
    assert test.tabs_to_spaces().text == ".   ..  ... ....    "
