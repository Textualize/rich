from rich.text import Span, Text


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
