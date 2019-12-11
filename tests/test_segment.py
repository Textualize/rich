from rich.segment import Segment


def test_repr():
    assert repr(Segment("foo")) == "Segment('foo', None)"


def test_line():
    assert Segment.line() == Segment("\n")
