from rich.text import Text
import pytest

from rich.errors import NotRenderableError
from rich.console import Console
from rich.measure import Measurement


def test_span():
    measurement = Measurement(10, 100)
    assert measurement.span == 90


def test_no_renderable():
    console = Console()
    text = Text()

    with pytest.raises(NotRenderableError):
        Measurement.get(console, None, console.width)


def test_null_get():
    # Test negative console.width passed into get method
    assert Measurement.get(Console(width=-1), None) == Measurement(0, 0)
    # Test negative max_width passed into get method
    assert Measurement.get(Console(), None, -1) == Measurement(0, 0)


if __name__ == "__main__":
    test_null_get()