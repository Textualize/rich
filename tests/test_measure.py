import pytest

from rich.console import Console
from rich.errors import NotRenderableError
from rich.measure import Measurement, measure_renderables
from rich.text import Text


def test_span():
    measurement = Measurement(10, 100)
    assert measurement.span == 90


def test_no_renderable():
    console = Console()
    text = Text()

    with pytest.raises(NotRenderableError):
        Measurement.get(console, console.options, None)


def test_measure_renderables():
    console = Console()
    assert measure_renderables(console, console.options, "") == Measurement(0, 0)
    assert measure_renderables(
        console, console.options.update_width(0), "hello"
    ) == Measurement(0, 0)


def test_clamp():
    measurement = Measurement(20, 100)
    assert measurement.clamp(10, 50) == Measurement(20, 50)
    assert measurement.clamp(30, 50) == Measurement(30, 50)
    assert measurement.clamp(None, 50) == Measurement(20, 50)
    assert measurement.clamp(30, None) == Measurement(30, 100)
    assert measurement.clamp(None, None) == Measurement(20, 100)
