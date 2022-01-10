"""Tests for the highlighter classes."""
import pytest
from typing import List

from rich.highlighter import NullHighlighter, ReprHighlighter
from rich.text import Span, Text


def test_wrong_type():
    highlighter = NullHighlighter()
    with pytest.raises(TypeError):
        highlighter([])


highlight_tests = [
    ("", []),
    (" ", []),
    (
        "<foo>",
        [
            Span(0, 1, "repr.tag_start"),
            Span(1, 4, "repr.tag_name"),
            Span(4, 5, "repr.tag_end"),
        ],
    ),
    (
        "False True None",
        [
            Span(0, 5, "repr.bool_false"),
            Span(6, 10, "repr.bool_true"),
            Span(11, 15, "repr.none"),
        ],
    ),
    ("foo=bar", [Span(0, 3, "repr.attrib_name"), Span(4, 7, "repr.attrib_value")]),
    (
        'foo="bar"',
        [
            Span(0, 3, "repr.attrib_name"),
            Span(4, 9, "repr.attrib_value"),
            Span(4, 9, "repr.str"),
        ],
    ),
    ("( )", [Span(0, 1, "repr.brace"), Span(2, 3, "repr.brace")]),
    ("[ ]", [Span(0, 1, "repr.brace"), Span(2, 3, "repr.brace")]),
    ("{ }", [Span(0, 1, "repr.brace"), Span(2, 3, "repr.brace")]),
    (" 1 ", [Span(1, 2, "repr.number")]),
    (" 1.2 ", [Span(1, 4, "repr.number")]),
    (" 0xff ", [Span(1, 5, "repr.number")]),
    (" 1e10 ", [Span(1, 5, "repr.number")]),
    (" /foo ", [Span(1, 2, "repr.path"), Span(2, 5, "repr.filename")]),
    (" /foo/bar.html ", [Span(1, 6, "repr.path"), Span(6, 14, "repr.filename")]),
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
    (" https://example.org ", [Span(1, 20, "repr.url")]),
    (" http://example.org ", [Span(1, 19, "repr.url")]),
    (" http://example.org/index.html ", [Span(1, 30, "repr.url")]),
    ("No place like 127.0.0.1", [Span(14, 23, "repr.ipv4")]),
    ("''", [Span(0, 2, "repr.str")]),
    ("'hello'", [Span(0, 7, "repr.str")]),
    ("'''hello'''", [Span(0, 11, "repr.str")]),
    ('""', [Span(0, 2, "repr.str")]),
    ('"hello"', [Span(0, 7, "repr.str")]),
    ('"""hello"""', [Span(0, 11, "repr.str")]),
    ("\\'foo'", []),
    ("it's no 'string'", [Span(8, 16, "repr.str")]),
]


@pytest.mark.parametrize("test, spans", highlight_tests)
def test_highlight_regex(test: str, spans: List[Span]):
    """Tests for the regular expressions used in ReprHighlighter."""
    text = Text(test)
    highlighter = ReprHighlighter()
    highlighter.highlight(text)
    print(text.spans)
    assert text.spans == spans
