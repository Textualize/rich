from rich.text import Text
import pytest

from rich.errors import NotRenderableError
from rich.console import Console
from rich.measure import Measurement, measure_renderables


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


def test_measure_renderables():
    # Test measure_renderables returning a null Measurement object
    assert measure_renderables(Console(), None, None) == Measurement(0, 0)
    # Test measure_renderables returning a valid Measurement object
    assert measure_renderables(Console(width=1), ["test"], 1) == Measurement(1, 1)


def test_clamp():
    measurement = Measurement(20, 100)
    assert measurement.clamp(10, 50) == Measurement(20, 50)
    assert measurement.clamp(30, 50) == Measurement(30, 50)
    assert measurement.clamp(None, 50) == Measurement(20, 50)
    assert measurement.clamp(30, None) == Measurement(30, 100)
    assert measurement.clamp(None, None) == Measurement(20, 100)
