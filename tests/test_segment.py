from io import StringIO

import pytest

from rich.segment import ControlType, Segment, SegmentLines, Segments
from rich.style import Style


def test_repr():
    assert repr(Segment("foo")) == "Segment('foo')"
    home = (ControlType.HOME, 0)
    assert (
        repr(Segment("foo", None, [home]))
        == "Segment('foo', None, [(<ControlType.HOME: 3>, 0)])"
    )


def test_line():
    assert Segment.line() == Segment("\n")


def test_apply_style():
    segments = [Segment("foo"), Segment("bar", Style(bold=True))]
    assert Segment.apply_style(segments, None) is segments
    assert list(Segment.apply_style(segments, Style(italic=True))) == [
        Segment("foo", Style(italic=True)),
        Segment("bar", Style(italic=True, bold=True)),
    ]


def test_split_lines():
    lines = [Segment("Hello\nWorld")]
    assert list(Segment.split_lines(lines)) == [[Segment("Hello")], [Segment("World")]]


def test_split_and_crop_lines():
    assert list(
        Segment.split_and_crop_lines([Segment("Hello\nWorld!\n"), Segment("foo")], 4)
    ) == [
        [Segment("Hell"), Segment("\n", None)],
        [Segment("Worl"), Segment("\n", None)],
        [Segment("foo"), Segment(" ")],
    ]


def test_adjust_line_length():
    line = [Segment("Hello", "foo")]
    assert Segment.adjust_line_length(line, 10, style="bar") == [
        Segment("Hello", "foo"),
        Segment("     ", "bar"),
    ]

    line = [Segment("H"), Segment("ello, World!")]
    assert Segment.adjust_line_length(line, 5) == [Segment("H"), Segment("ello")]

    line = [Segment("Hello")]
    assert Segment.adjust_line_length(line, 5) == line


def test_get_line_length():
    assert Segment.get_line_length([Segment("foo"), Segment("bar")]) == 6


def test_get_shape():
    assert Segment.get_shape([[Segment("Hello")]]) == (5, 1)
    assert Segment.get_shape([[Segment("Hello")], [Segment("World!")]]) == (6, 2)


def test_set_shape():
    assert Segment.set_shape([[Segment("Hello")]], 10) == [
        [Segment("Hello"), Segment("     ")]
    ]
    assert Segment.set_shape([[Segment("Hello")]], 10, 2) == [
        [Segment("Hello"), Segment("     ")],
        [Segment(" " * 10)],
    ]


def test_simplify():
    assert list(
        Segment.simplify([Segment("Hello"), Segment(" "), Segment("World!")])
    ) == [Segment("Hello World!")]
    assert list(
        Segment.simplify(
            [Segment("Hello", "red"), Segment(" ", "red"), Segment("World!", "blue")]
        )
    ) == [Segment("Hello ", "red"), Segment("World!", "blue")]
    assert list(Segment.simplify([])) == []


def test_filter_control():
    control_code = (ControlType.HOME, 0)
    segments = [Segment("foo"), Segment("bar", None, (control_code,))]
    assert list(Segment.filter_control(segments)) == [Segment("foo")]
    assert list(Segment.filter_control(segments, is_control=True)) == [
        Segment("bar", None, (control_code,))
    ]


def test_strip_styles():
    segments = [Segment("foo", Style(bold=True))]
    assert list(Segment.strip_styles(segments)) == [Segment("foo", None)]


def test_strip_links():
    segments = [Segment("foo", Style(bold=True, link="https://www.example.org"))]
    assert list(Segment.strip_links(segments)) == [Segment("foo", Style(bold=True))]


def test_remove_color():
    segments = [
        Segment("foo", Style(bold=True, color="red")),
        Segment("bar", None),
    ]
    assert list(Segment.remove_color(segments)) == [
        Segment("foo", Style(bold=True)),
        Segment("bar", None),
    ]


def test_is_control():
    assert Segment("foo", Style(bold=True)).is_control == False
    assert Segment("foo", Style(bold=True), []).is_control == True
    assert Segment("foo", Style(bold=True), [(ControlType.HOME, 0)]).is_control == True


def test_segments_renderable():
    segments = Segments([Segment("foo")])
    assert list(segments.__rich_console__(None, None)) == [Segment("foo")]

    segments = Segments([Segment("foo")], new_lines=True)
    assert list(segments.__rich_console__(None, None)) == [
        Segment("foo"),
        Segment.line(),
    ]


def test_divide():
    bold = Style(bold=True)
    italic = Style(italic=True)
    segments = [
        Segment("Hello", bold),
        Segment(" World!", italic),
    ]

    assert list(Segment.divide(segments, [])) == []
    assert list(Segment.divide([], [1])) == [[]]

    assert list(Segment.divide(segments, [1])) == [[Segment("H", bold)]]

    assert list(Segment.divide(segments, [1, 2])) == [
        [Segment("H", bold)],
        [Segment("e", bold)],
    ]

    assert list(Segment.divide(segments, [1, 2, 12])) == [
        [Segment("H", bold)],
        [Segment("e", bold)],
        [Segment("llo", bold), Segment(" World!", italic)],
    ]

    assert list(Segment.divide(segments, [4, 20])) == [
        [Segment("Hell", bold)],
        [Segment("o", bold), Segment(" World!", italic)],
    ]


# https://github.com/textualize/rich/issues/1755
def test_divide_complex():
    MAP = (
        "[on orange4]          [on green]XX[on orange4]          \n"
        "                        \n"
        "                        \n"
        "                        \n"
        "              [bright_red on black]Y[on orange4]        \n"
        "[on green]X[on orange4]                  [on green]X[on orange4]  \n"
        " [on green]X[on orange4]                   [on green]X\n"
        "[on orange4]                        \n"
        "          [on green]XX[on orange4]          \n"
    )
    from rich.console import Console
    from rich.text import Text

    text = Text.from_markup(MAP)
    console = Console(
        color_system="truecolor", width=30, force_terminal=True, file=StringIO()
    )
    console.print(text)
    result = console.file.getvalue()

    print(repr(result))
    expected = "\x1b[48;5;94m          \x1b[0m\x1b[42mXX\x1b[0m\x1b[48;5;94m          \x1b[0m\n\x1b[48;5;94m                        \x1b[0m\n\x1b[48;5;94m                        \x1b[0m\n\x1b[48;5;94m                        \x1b[0m\n\x1b[48;5;94m              \x1b[0m\x1b[91;40mY\x1b[0m\x1b[91;48;5;94m        \x1b[0m\n\x1b[91;42mX\x1b[0m\x1b[91;48;5;94m                  \x1b[0m\x1b[91;42mX\x1b[0m\x1b[91;48;5;94m  \x1b[0m\n\x1b[91;48;5;94m \x1b[0m\x1b[91;42mX\x1b[0m\x1b[91;48;5;94m                   \x1b[0m\x1b[91;42mX\x1b[0m\n\x1b[91;48;5;94m                        \x1b[0m\n\x1b[91;48;5;94m          \x1b[0m\x1b[91;42mXX\x1b[0m\x1b[91;48;5;94m          \x1b[0m\n\n"
    assert result == expected


def test_divide_emoji():
    bold = Style(bold=True)
    italic = Style(italic=True)
    segments = [
        Segment("Hello", bold),
        Segment("💩💩💩", italic),
    ]

    assert list(Segment.divide(segments, [7])) == [
        [Segment("Hello", bold), Segment("💩", italic)],
    ]
    assert list(Segment.divide(segments, [8])) == [
        [Segment("Hello", bold), Segment("💩 ", italic)],
    ]
    assert list(Segment.divide(segments, [9])) == [
        [Segment("Hello", bold), Segment("💩💩", italic)],
    ]
    assert list(Segment.divide(segments, [8, 11])) == [
        [Segment("Hello", bold), Segment("💩 ", italic)],
        [Segment(" 💩", italic)],
    ]
    assert list(Segment.divide(segments, [9, 11])) == [
        [Segment("Hello", bold), Segment("💩💩", italic)],
        [Segment("💩", italic)],
    ]


def test_divide_edge():
    segments = [Segment("foo"), Segment("bar"), Segment("baz")]
    result = list(Segment.divide(segments, [1, 3, 9]))
    print(result)
    assert result == [
        [Segment("f")],
        [Segment("oo")],
        [Segment("bar"), Segment("baz")],
    ]


def test_divide_edge_2():
    segments = [
        Segment("╭─"),
        Segment(
            "────── Placeholder ───────",
        ),
        Segment(
            "─╮",
        ),
    ]
    result = list(Segment.divide(segments, [30, 60]))
    expected = [segments, []]
    print(repr(result))
    assert result == expected


@pytest.mark.parametrize(
    "text,split,result",
    [
        ("XX", 4, (Segment("XX"), Segment(""))),
        ("X", 1, (Segment("X"), Segment(""))),
        ("💩", 1, (Segment(" "), Segment(" "))),
        ("XY", 1, (Segment("X"), Segment("Y"))),
        ("💩X", 1, (Segment(" "), Segment(" X"))),
        ("💩💩", 1, (Segment(" "), Segment(" 💩"))),
        ("X💩Y", 2, (Segment("X "), Segment(" Y"))),
        ("X💩YZ", 2, (Segment("X "), Segment(" YZ"))),
        ("X💩💩Z", 2, (Segment("X "), Segment(" 💩Z"))),
        ("X💩💩Z", 3, (Segment("X💩"), Segment("💩Z"))),
        ("X💩💩Z", 4, (Segment("X💩 "), Segment(" Z"))),
        ("X💩💩Z", 5, (Segment("X💩💩"), Segment("Z"))),
        ("X💩💩Z", 6, (Segment("X💩💩Z"), Segment(""))),
        ("XYZABC💩💩", 6, (Segment("XYZABC"), Segment("💩💩"))),
        ("XYZABC💩💩", 7, (Segment("XYZABC "), Segment(" 💩"))),
        ("XYZABC💩💩", 8, (Segment("XYZABC💩"), Segment("💩"))),
        ("XYZABC💩💩", 9, (Segment("XYZABC💩 "), Segment(" "))),
        ("XYZABC💩💩", 10, (Segment("XYZABC💩💩"), Segment(""))),
        ("💩💩💩💩💩", 3, (Segment("💩 "), Segment(" 💩💩💩"))),
        ("💩💩💩💩💩", 4, (Segment("💩💩"), Segment("💩💩💩"))),
        ("💩X💩Y💩Z💩A💩", 4, (Segment("💩X "), Segment(" Y💩Z💩A💩"))),
        ("XYZABC", 4, (Segment("XYZA"), Segment("BC"))),
        ("XYZABC", 5, (Segment("XYZAB"), Segment("C"))),
        (
            "a1あ１１bcdaef",
            9,
            (Segment("a1あ１１b"), Segment("cdaef")),
        ),
    ],
)
def test_split_cells_emoji(text, split, result):
    assert Segment(text).split_cells(split) == result


def test_segment_lines_renderable():
    lines = [[Segment("hello"), Segment(" "), Segment("world")], [Segment("foo")]]
    segment_lines = SegmentLines(lines)
    assert list(segment_lines.__rich_console__(None, None)) == [
        Segment("hello"),
        Segment(" "),
        Segment("world"),
        Segment("foo"),
    ]

    segment_lines = SegmentLines(lines, new_lines=True)
    assert list(segment_lines.__rich_console__(None, None)) == [
        Segment("hello"),
        Segment(" "),
        Segment("world"),
        Segment("\n"),
        Segment("foo"),
        Segment("\n"),
    ]


def test_align_top():
    lines = [[Segment("X")]]
    assert Segment.align_top(lines, 3, 1, Style()) == lines
    assert Segment.align_top(lines, 3, 3, Style()) == [
        [Segment("X")],
        [Segment("   ", Style())],
        [Segment("   ", Style())],
    ]


def test_align_middle():
    lines = [[Segment("X")]]
    assert Segment.align_middle(lines, 3, 1, Style()) == lines
    assert Segment.align_middle(lines, 3, 3, Style()) == [
        [Segment("   ", Style())],
        [Segment("X")],
        [Segment("   ", Style())],
    ]


def test_align_bottom():
    lines = [[Segment("X")]]
    assert Segment.align_bottom(lines, 3, 1, Style()) == lines
    assert Segment.align_bottom(lines, 3, 3, Style()) == [
        [Segment("   ", Style())],
        [Segment("   ", Style())],
        [Segment("X")],
    ]
