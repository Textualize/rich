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
        # Braces
        ("repr.brace", "["),
        ("repr.brace", "]"),
        ("repr.brace", "("),
        ("repr.brace", ")"),
        ("repr.brace", "{"),
        ("repr.brace", "}"),
        # Tags
        ("repr.tag_start", "<tag>"),
        ("repr.tag_end", "<tag>"),
        ("repr.tag_content", "</tag>"),  # closing tag
        ("repr.tag_content", "<some-tag>"),  # hyphen
        ("repr.tag_content", "<some.tag>"),  # dot
        ("repr.tag_content", "<some:tag>"),  # colon
        # Attributes
        ("repr.attrib_name", "attrib="),  # no value
        ("repr.attrib_value", "attrib=value"),  # some value
        ("repr.attrib_value", 'attrib="value"'),  # value with double quotes
        ("repr.attrib_value", "attrib='value'"),  # value with single quotes
        # Boolean values
        ("repr.bool_true", "True"),
        ("repr.bool_false", "False"),
        ("repr.none", "None"),
        # Numbers
        ("repr.number", "123456789"),  # positive
        ("repr.number", "-123456789"),  # negative
        ("repr.number", "123.456789"),  # decimal
        ("repr.number", "0x0123af"),  # hexadecimal
        # Paths
        ("repr.path", "/path/to/dir/"),
        ("repr.filename", "/path/to/filename"),
        ("repr.filename", "/path/to/filename.txt"),
        # IPV4 addresses
        ("repr.ipv4", "0.0.0.0"),  # first ip
        ("repr.ipv4", "192.168.1.1"),  # some ip in between
        ("repr.ipv4", "255.255.255.255"),  # last ip
        # IPV6 addresses
        ("repr.ipv6", "0:0:0:0:0:0:0:0"),  # first ip
        ("repr.ipv6", "fde2:1234:abcd:0:aaaa:ffff:56:789"),  # some ip in between
        ("repr.ipv6", "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"),  # last ip
        # MAC addresses
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
        # Strings
        ("repr.str", "'string'"),  # single quotes
        ("repr.str", '"string"'),  # double quotes
        ("repr.str", "'''string'''"),  # triple-single quotes
        ("repr.str", '"""string"""'),  # triple-double quotes
        # URLs
        ("repr.url", "http://example.com/some/path"),  # http url
        ("repr.url", "https://example.com/some/path"),  # https url
        # UUIDs
        ("repr.uuid", "00000000-0000-0000-0000-000000000000"),  # lowest uuid
        ("repr.uuid", "12345678-90ab-cdef-1234-567890abcdef"),  # some uuid in between
        ("repr.uuid", "ffffffff-ffff-ffff-ffff-ffffffffffff"),  # highest uuid
    ],
)
def test_highlight_regex(style_name: str, test_str: str):
    """Tests for the regular expressions used in ReprHighlighter."""
    text = Text(test_str)
    highlighter = ReprHighlighter()
    highlighter.highlight(text)
    assert style_name in repr(text)
