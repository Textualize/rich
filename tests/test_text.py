from io import StringIO
import pytest

from rich.console import Console
from rich.text import Span, Text
from rich.measure import Measurement
from rich.style import Style


def test_span():
    span = Span(1, 10, "foo")
    repr(span)
    assert bool(span)
    assert not Span(10, 10, "foo")


def test_span_split():
    assert Span(5, 10, "foo").split(2) == (Span(5, 10, "foo"), None)
    assert Span(5, 10, "foo").split(15) == (Span(5, 10, "foo"), None)
    assert Span(0, 10, "foo").split(5) == (Span(0, 5, "foo"), Span(5, 10, "foo"))


def test_span_move():
    assert Span(5, 10, "foo").move(2) == Span(7, 12, "foo")


def test_span_right_crop():
    assert Span(5, 10, "foo").right_crop(15) == Span(5, 10, "foo")
    assert Span(5, 10, "foo").right_crop(7) == Span(5, 7, "foo")


def test_len():
    assert len(Text("foo")) == 3


def test_cell_len():
    assert Text("foo").cell_len == 3
    assert Text("😀").cell_len == 2


def test_bool():
    assert Text("foo")
    assert not Text("")


def test_str():
    assert str(Text("foo")) == "foo"


def test_repr():
    assert isinstance(repr(Text("foo")), str)


def test_add():
    text = Text("foo") + Text("bar")
    assert str(text) == "foobar"
    assert Text("foo").__add__(1) == NotImplemented


def test_eq():
    assert Text("foo") == Text("foo")
    assert Text("foo") != Text("bar")
    assert Text("foo").__eq__(1) == NotImplemented


def test_contain():
    test = Text("foobar")
    assert "foo" in test
    assert "foo " not in test
    assert Text("bar") in test
    assert None not in test


def test_plain_property():
    text = Text("foo")
    text.append("bar")
    text.append("baz")
    assert text.plain == "foobarbaz"


def test_plain_property_setter():
    test = Text("foo")
    test.plain = "bar"
    assert str(test) == "bar"
    test = Text()
    test.append("Hello, World", "bold")
    test.plain = "Hello"
    assert str(test) == "Hello"
    assert test._spans == [Span(0, 5, "bold")]


def test_from_markup():
    text = Text.from_markup("Hello, [bold]World![/bold]")
    assert str(text) == "Hello, World!"
    assert text._spans == [Span(7, 13, "bold")]


def test_copy():
    test = Text()
    test.append("Hello", "bold")
    test.append(" ")
    test.append("World", "italic")
    test_copy = test.copy()
    assert test == test_copy
    assert test is not test_copy


def test_rstrip():
    test = Text("Hello, World!    ")
    test.rstrip()
    assert str(test) == "Hello, World!"


def test_rstrip_end():
    test = Text("Hello, World!    ")
    test.rstrip_end(14)
    assert str(test) == "Hello, World! "


def test_stylize():
    test = Text("Hello, World!")
    test.stylize("bold", 7, 11)
    assert test._spans == [Span(7, 11, "bold")]
    test.stylize("bold", 20, 25)
    assert test._spans == [Span(7, 11, "bold")]


def test_stylize_negative_index():
    test = Text("Hello, World!")
    test.stylize("bold", -6, -1)
    assert test._spans == [Span(7, 12, "bold")]


def test_highlight_regex():
    test = Text("peek-a-boo")

    count = test.highlight_regex(r"NEVER_MATCH", "red")
    assert count == 0
    assert len(test._spans) == 0

    # text: peek-a-boo
    # indx: 0123456789
    count = test.highlight_regex(r"[a|e|o]+", "red")
    assert count == 3
    assert sorted(test._spans) == [
        Span(1, 3, "red"),
        Span(5, 6, "red"),
        Span(8, 10, "red"),
    ]

    test = Text("Ada Lovelace, Alan Turing")
    count = test.highlight_regex(
        r"(?P<yellow>[A-Za-z]+)[ ]+(?P<red>[A-Za-z]+)(?P<NEVER_MATCH>NEVER_MATCH)*"
    )

    # The number of matched name should be 2
    assert count == 2
    assert sorted(test._spans) == [
        Span(0, 3, "yellow"),  # Ada
        Span(4, 12, "red"),  # Lovelace
        Span(14, 18, "yellow"),  # Alan
        Span(19, 25, "red"),  # Turing
    ]


def test_highlight_regex_callable():
    test = Text("Vulnerability CVE-2018-6543 detected")
    re_cve = r"CVE-\d{4}-\d+"

    def get_style(text: str) -> Style:
        return Style.parse(
            f"bold yellow link https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={text}"
        )

    count = test.highlight_regex(re_cve, get_style)
    assert count == 1
    assert len(test._spans) == 1
    assert test._spans[0].start == 14
    assert test._spans[0].end == 27
    assert (
        test._spans[0].style.link
        == "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=CVE-2018-6543"
    )


def test_highlight_words():
    test = Text("Do NOT! touch anything!")
    words = ["NOT", "!"]
    count = test.highlight_words(words, "red")
    assert count == 3
    assert sorted(test._spans) == [
        Span(3, 6, "red"),  # NOT
        Span(6, 7, "red"),  # !
        Span(22, 23, "red"),  # !
    ]

    # regex escape test
    test = Text("[o|u]aeiou")
    words = ["[a|e|i]", "[o|u]"]
    count = test.highlight_words(words, "red")
    assert count == 1
    assert test._spans == [Span(0, 5, "red")]

    # case sensitive
    test = Text("AB Ab aB ab")
    words = ["AB"]

    count = test.highlight_words(words, "red")
    assert count == 1
    assert test._spans == [Span(0, 2, "red")]

    test = Text("AB Ab aB ab")
    count = test.highlight_words(words, "red", case_sensitive=False)
    assert count == 4


def test_set_length():
    test = Text("Hello")
    test.set_length(5)
    assert test == Text("Hello")

    test = Text("Hello")
    test.set_length(10)
    assert test == Text("Hello     ")

    test = Text("Hello World")
    test.stylize("bold", 0, 5)
    test.stylize("italic", 7, 9)

    test.set_length(3)
    expected = Text()
    expected.append("Hel", "bold")
    assert test == expected


def test_console_width():
    console = Console()
    test = Text("Hello World!\nfoobarbaz")
    assert test.__rich_measure__(console, 80) == Measurement(9, 12)
    assert Text(" " * 4).__rich_measure__(console, 80) == Measurement(4, 4)
    assert Text(" \n  \n   ").__rich_measure__(console, 80) == Measurement(3, 3)


def test_join():
    test = Text("bar").join([Text("foo", "red"), Text("baz", "blue")])
    assert str(test) == "foobarbaz"
    assert test._spans == [Span(0, 3, "red"), Span(6, 9, "blue")]


def test_trim_spans():
    test = Text("Hello")
    test._spans[:] = [Span(0, 3, "red"), Span(3, 6, "green"), Span(6, 9, "blue")]
    test._trim_spans()
    assert test._spans == [Span(0, 3, "red"), Span(3, 5, "green")]


def test_pad_left():
    test = Text("foo")
    test.pad_left(3, "X")
    assert str(test) == "XXXfoo"


def test_pad_right():
    test = Text("foo")
    test.pad_right(3, "X")
    assert str(test) == "fooXXX"


def test_append():
    test = Text("foo")
    test.append("bar")
    assert str(test) == "foobar"
    test.append(Text("baz", "bold"))
    assert str(test) == "foobarbaz"
    assert test._spans == [Span(6, 9, "bold")]

    with pytest.raises(ValueError):
        test.append(Text("foo"), "bar")

    with pytest.raises(TypeError):
        test.append(1)


def test_append_text():
    test = Text("foo")
    test.append_text(Text("bar", style="bold"))
    assert str(test) == "foobar"
    assert test._spans == [Span(3, 6, "bold")]


def test_split():
    test = Text()
    test.append("foo", "red")
    test.append("\n")
    test.append("bar", "green")
    test.append("\n")

    line1 = Text()
    line1.append("foo", "red")
    line2 = Text()
    line2.append("bar", "green")
    split = test.split("\n")
    assert len(split) == 2
    assert split[0] == line1
    assert split[1] == line2

    assert list(Text("foo").split("\n")) == [Text("foo")]


def test_split_spans():
    test = Text.from_markup("[red]Hello\n[b]World")
    lines = test.split("\n")
    assert lines[0].plain == "Hello"
    assert lines[1].plain == "World"
    assert lines[0].spans == [Span(0, 5, "red")]
    assert lines[1].spans == [Span(0, 5, "red"), Span(0, 5, "bold")]


def test_divide():
    lines = Text("foo").divide([])
    assert len(lines) == 1
    assert lines[0] == Text("foo")

    text = Text()
    text.append("foo", "bold")
    lines = text.divide([1, 2])
    assert len(lines) == 3
    assert str(lines[0]) == "f"
    assert str(lines[1]) == "o"
    assert str(lines[2]) == "o"
    assert lines[0]._spans == [Span(0, 1, "bold")]
    assert lines[1]._spans == [Span(0, 1, "bold")]
    assert lines[2]._spans == [Span(0, 1, "bold")]

    text = Text()
    text.append("foo", "red")
    text.append("bar", "green")
    text.append("baz", "blue")
    lines = text.divide([8])
    assert len(lines) == 2
    assert str(lines[0]) == "foobarba"
    assert str(lines[1]) == "z"
    assert lines[0]._spans == [
        Span(0, 3, "red"),
        Span(3, 6, "green"),
        Span(6, 8, "blue"),
    ]
    assert lines[1]._spans == [Span(0, 1, "blue")]

    lines = text.divide([1])
    assert len(lines) == 2
    assert str(lines[0]) == "f"
    assert str(lines[1]) == "oobarbaz"
    assert lines[0]._spans == [Span(0, 1, "red")]
    assert lines[1]._spans == [
        Span(0, 2, "red"),
        Span(2, 5, "green"),
        Span(5, 8, "blue"),
    ]


def test_right_crop():
    test = Text()
    test.append("foobar", "red")
    test.right_crop(3)
    assert str(test) == "foo"
    assert test._spans == [Span(0, 3, "red")]


def test_wrap_3():
    test = Text("foo bar baz")
    lines = test.wrap(Console(), 3)
    print(repr(lines))
    assert len(lines) == 3
    assert lines[0] == Text("foo")
    assert lines[1] == Text("bar")
    assert lines[2] == Text("baz")


def test_wrap_4():
    test = Text("foo bar baz", justify="left")
    lines = test.wrap(Console(), 4)
    assert len(lines) == 3
    assert lines[0] == Text("foo ")
    assert lines[1] == Text("bar ")
    assert lines[2] == Text("baz ")


def test_wrap_long():
    test = Text("abracadabra", justify="left")
    lines = test.wrap(Console(), 4)
    assert len(lines) == 3
    assert lines[0] == Text("abra")
    assert lines[1] == Text("cada")
    assert lines[2] == Text("bra ")


def test_wrap_overflow():
    test = Text("Some more words")
    lines = test.wrap(Console(), 4, overflow="ellipsis")
    assert (len(lines)) == 3
    assert lines[0] == Text("Some")
    assert lines[1] == Text("more")
    assert lines[2] == Text("wor…")


def test_wrap_overflow_long():
    test = Text("bigword" * 10)
    lines = test.wrap(Console(), 4, overflow="ellipsis")
    assert len(lines) == 1
    assert lines[0] == Text("big…")


def test_wrap_long_words():
    test = Text("X 123456789", justify="left")
    lines = test.wrap(Console(), 4)

    assert len(lines) == 3
    assert lines[0] == Text("X 12")
    assert lines[1] == Text("3456")
    assert lines[2] == Text("789 ")


def test_no_wrap_no_crop():
    test = Text("Hello World!" * 3)

    console = Console(width=20, file=StringIO())
    console.print(test, no_wrap=True)
    console.print(test, no_wrap=True, crop=False, overflow="ignore")

    print(repr(console.file.getvalue()))
    assert (
        console.file.getvalue()
        == "Hello World!Hello Wo\nHello World!Hello World!Hello World!\n"
    )


def test_fit():
    test = Text("Hello\nWorld")
    lines = test.fit(3)
    assert str(lines[0]) == "Hel"
    assert str(lines[1]) == "Wor"


def test_wrap_tabs():
    test = Text("foo\tbar", justify="left")
    lines = test.wrap(Console(), 4)
    assert len(lines) == 2
    assert str(lines[0]) == "foo "
    assert str(lines[1]) == "bar "


def test_render():
    console = Console(width=15, record=True)
    test = Text.from_markup(
        "[u][b]Where[/b] there is a [i]Will[/i], there is a Way.[/u]"
    )
    console.print(test)
    output = console.export_text(styles=True)
    expected = "\x1b[1;4mWhere\x1b[0m\x1b[4m there is \x1b[0m\n\x1b[4ma \x1b[0m\x1b[3;4mWill\x1b[0m\x1b[4m, there \x1b[0m\n\x1b[4mis a Way.\x1b[0m\n"
    assert output == expected


def test_render_simple():
    console = Console(width=80)
    console.begin_capture()
    console.print(Text("foo"))
    result = console.end_capture()
    assert result == "foo\n"


@pytest.mark.parametrize(
    "print_text,result",
    [
        (("."), ".\n"),
        ((".", "."), ". .\n"),
        (("Hello", "World", "!"), "Hello World !\n"),
    ],
)
def test_print(print_text, result):
    console = Console(record=True)
    console.print(*print_text)
    assert console.export_text(styles=False) == result


@pytest.mark.parametrize(
    "print_text,result",
    [
        (("."), ".X"),
        ((".", "."), "..X"),
        (("Hello", "World", "!"), "HelloWorld!X"),
    ],
)
def test_print_sep_end(print_text, result):
    console = Console(record=True, file=StringIO())
    console.print(*print_text, sep="", end="X")
    assert console.file.getvalue() == result


def test_tabs_to_spaces():
    test = Text("\tHello\tWorld", tab_size=8)
    test.expand_tabs()
    assert test.plain == "        Hello   World"

    test = Text("\tHello\tWorld", tab_size=4)
    test.expand_tabs()
    assert test.plain == "    Hello   World"

    test = Text(".\t..\t...\t....\t", tab_size=4)
    test.expand_tabs()
    assert test.plain == ".   ..  ... ....    "

    test = Text("No Tabs")
    test.expand_tabs()
    assert test.plain == "No Tabs"


def test_markup_switch():
    """Test markup can be disabled."""
    console = Console(file=StringIO(), markup=False)
    console.print("[bold]foo[/bold]")
    assert console.file.getvalue() == "[bold]foo[/bold]\n"


def test_emoji():
    """Test printing emoji codes."""
    console = Console(file=StringIO())
    console.print(":+1:")
    assert console.file.getvalue() == "👍\n"


def test_emoji_switch():
    """Test emoji can be disabled."""
    console = Console(file=StringIO(), emoji=False)
    console.print(":+1:")
    assert console.file.getvalue() == ":+1:\n"


def test_assemble():
    text = Text.assemble("foo", ("bar", "bold"))
    assert str(text) == "foobar"
    assert text._spans == [Span(3, 6, "bold")]


def test_assemble_meta():
    text = Text.assemble("foo", ("bar", "bold"), meta={"foo": "bar"})
    assert str(text) == "foobar"
    assert text._spans == [Span(3, 6, "bold"), Span(0, 6, Style(meta={"foo": "bar"}))]
    console = Console()
    assert text.get_style_at_offset(console, 0).meta == {"foo": "bar"}


def test_styled():
    text = Text.styled("foo", "bold red")
    assert text.style == ""
    assert str(text) == "foo"
    assert text._spans == [Span(0, 3, "bold red")]


def test_strip_control_codes():
    text = Text("foo\rbar")
    assert str(text) == "foobar"
    text.append("\x08")
    assert str(text) == "foobar"


def test_get_style_at_offset():
    console = Console()
    text = Text.from_markup("Hello [b]World[/b]")
    assert text.get_style_at_offset(console, 0) == Style()
    assert text.get_style_at_offset(console, 6) == Style(bold=True)


@pytest.mark.parametrize(
    "input, count, expected",
    [
        ("Hello", 10, "Hello"),
        ("Hello", 5, "Hello"),
        ("Hello", 4, "Hel…"),
        ("Hello", 3, "He…"),
        ("Hello", 2, "H…"),
        ("Hello", 1, "…"),
    ],
)
def test_truncate_ellipsis(input, count, expected):
    text = Text(input)
    text.truncate(count, overflow="ellipsis")
    assert text.plain == expected


@pytest.mark.parametrize(
    "input, count, expected",
    [
        ("Hello", 5, "Hello"),
        ("Hello", 10, "Hello     "),
        ("Hello", 3, "He…"),
    ],
)
def test_truncate_ellipsis_pad(input, count, expected):
    text = Text(input)
    text.truncate(count, overflow="ellipsis", pad=True)
    assert text.plain == expected


def test_pad():
    test = Text("foo")
    test.pad(2)
    assert test.plain == "  foo  "


def test_align_left():
    test = Text("foo")
    test.align("left", 10)
    assert test.plain == "foo       "


def test_align_right():
    test = Text("foo")
    test.align("right", 10)
    assert test.plain == "       foo"


def test_align_center():
    test = Text("foo")
    test.align("center", 10)
    assert test.plain == "   foo    "


def test_detect_indentation():
    test = """\
foo
    bar
    """
    assert Text(test).detect_indentation() == 4
    test = """\
foo
    bar
      baz
    """
    assert Text(test).detect_indentation() == 2
    assert Text("").detect_indentation() == 1
    assert Text(" ").detect_indentation() == 1


def test_indentation_guides():
    test = Text(
        """\
for a in range(10):
    print(a)

foo = [
    1,
    {
        2
    }
]

"""
    )
    result = test.with_indent_guides()
    print(result.plain)
    print(repr(result.plain))
    expected = "for a in range(10):\n│   print(a)\n\nfoo = [\n│   1,\n│   {\n│   │   2\n│   }\n]\n\n"
    assert result.plain == expected


def test_slice():

    text = Text.from_markup("[red]foo [bold]bar[/red] baz[/bold]")
    assert text[0] == Text("f", spans=[Span(0, 1, "red")])
    assert text[4] == Text("b", spans=[Span(0, 1, "red"), Span(0, 1, "bold")])

    assert text[:3] == Text("foo", spans=[Span(0, 3, "red")])
    assert text[:4] == Text("foo ", spans=[Span(0, 4, "red")])
    assert text[:5] == Text("foo b", spans=[Span(0, 5, "red"), Span(4, 5, "bold")])
    assert text[4:] == Text("bar baz", spans=[Span(0, 3, "red"), Span(0, 7, "bold")])

    with pytest.raises(TypeError):
        text[::-1]


def test_wrap_invalid_style():
    # https://github.com/willmcgugan/rich/issues/987
    console = Console(width=100, color_system="truecolor")
    a = "[#######.................] xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx [#######.................]"
    console.print(a, justify="full")


def test_apply_meta():
    text = Text("foobar")
    text.apply_meta({"foo": "bar"}, 1, 3)

    console = Console()
    assert text.get_style_at_offset(console, 0).meta == {}
    assert text.get_style_at_offset(console, 1).meta == {"foo": "bar"}
    assert text.get_style_at_offset(console, 2).meta == {"foo": "bar"}
    assert text.get_style_at_offset(console, 3).meta == {}


def test_on():
    console = Console()
    text = Text("foo")
    text.on({"foo": "bar"}, click="CLICK")
    expected = {"foo": "bar", "@click": "CLICK"}
    assert text.get_style_at_offset(console, 0).meta == expected
    assert text.get_style_at_offset(console, 1).meta == expected
    assert text.get_style_at_offset(console, 2).meta == expected
