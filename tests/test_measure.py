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
