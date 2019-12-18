from rich.segment import Segment
from rich.style import Style


def test_repr():
    assert repr(Segment("foo")) == "Segment('foo', None)"


def test_line():
    assert Segment.line() == Segment("\n")


def test_apply_style():
    segments = [Segment("foo"), Segment("bar", Style(bold=True))]
    assert Segment.apply_style(segments, None) is segments
    assert list(Segment.apply_style(segments, Style(italic=True))) == [
        Segment("foo", Style(italic=True)),
        Segment("bar", Style(italic=True, bold=True)),
    ]


def test_split_and_crop_lines():
    assert list(
        Segment.split_and_crop_lines([Segment("Hello\nWorld!\n"), Segment("foo")], 4)
    ) == [[Segment("Hell")], [Segment("Worl")], [Segment("foo"), Segment(" ")]]


def test_get_line_length():
    assert Segment.get_line_length([Segment("foo"), Segment("bar")]) == 6
