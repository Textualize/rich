"""Tests for the higlighter classes."""
import pytest

from rich.highlighter import NullHighlighter, ReprHighlighter
from rich.text import Span, Text


def test_wrong_type():
    highlighter = NullHighlighter()
    with pytest.raises(TypeError):
        highlighter([])


@pytest.mark.parametrize(
    "style_name, test_str",
    [
        ("repr.eui48", "01-23-45-67-89-AB"),  # 6x2 hyphen
        ("repr.eui64", "01-23-45-FF-FE-67-89-AB"),  # 8x2 hyphen
        ("repr.eui48", "01:23:45:67:89:AB"),  # 6x2 colon
        ("repr.eui64", "01:23:45:FF:FE:67:89:AB"),  # 8x2 colon
        ("repr.eui48", "0123.4567.89AB"),  # 3x4 dot
        ("repr.eui64", "0123.45FF.FE67.89AB"),  # 4x4 dot
        ("repr.eui48", "ed-ed-ed-ed-ed-ed"),  # lowercase
        ("repr.eui48", "ED-ED-ED-ED-ED-ED"),  # uppercase
        ("repr.eui48", "Ed-Ed-Ed-Ed-Ed-Ed"),  # mixed case
        ("repr.eui48", "0-00-1-01-2-02"),  # dropped zero
    ],
)
def test_highlight_regex(style_name: str, test_str: str):
    """Tests for the regular expressions used in ReprHighlighter."""
    text = Text(test_str)
    highlighter = ReprHighlighter()
    highlighter.highlight(text)
    assert text._spans[-1] == Span(0, len(test_str), style_name)
