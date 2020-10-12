"""Tests for the higlighter classes."""
import pytest
from typing import List

from rich.highlighter import NullHighlighter, ReprHighlighter
from rich.text import Span, Text


def test_wrong_type():
    highlighter = NullHighlighter()
    with pytest.raises(TypeError):
        highlighter([])


highlight_tests = [
    ("( ) { } [ ]", [Span(0, 1, "repr.brace")]),
    ("01-23-45-67-89-AB", [Span(0, 17, "repr.eui48")]),  # 6x2 hyphen
    ("01-23-45-FF-FE-67-89-AB", [Span(0, 23, "repr.eui64")]),  # 8x2 hyphen
    ("01:23:45:67:89:AB", [Span(0, 17, "repr.ipv6")]),  # 6x2 colon
    ("01:23:45:FF:FE:67:89:AB", [Span(0, 23, "repr.ipv6")]),  # 8x2 colon
    ("0123.4567.89AB", [Span(0, 14, "repr.eui48")]),  # 3x4 dot
    ("0123.45FF.FE67.89AB", [Span(0, 19, "repr.eui64")]),  # 4x4 dot
    ("ed-ed-ed-ed-ed-ed", [Span(0, 17, "repr.eui48")]),  # lowercase
    ("ED-ED-ED-ED-ED-ED", [Span(0, 17, "repr.eui48")]),  # uppercase
    ("Ed-Ed-Ed-Ed-Ed-Ed", [Span(0, 17, "repr.eui48")]),  # mixed case
    ("0-00-1-01-2-02", [Span(0, 14, "repr.eui48")]),  # dropped zero
]


@pytest.mark.parametrize("test, spans", highlight_tests)
def test_highlight_regex(test: str, spans: List[Span]):
    """Tests for the regular expressions used in ReprHighlighter."""
    text = Text(test)
    highlighter = ReprHighlighter()
    highlighter.highlight(text)
    assert text.spans == spans
