from io import StringIO
from typing import List

import pytest

from rich.console import Console, Group
from rich.measure import Measurement
from rich.style import Style
from rich.text import Span, Text


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
    text = Text("foobar")
    assert "foo" in text
    assert "foo " not in text
    assert Text("bar") in text
    assert None not in text


def test_plain_property():
    text = Text("foo")
    text.append("bar")
    text.append("baz")
    assert text.plain == "foobarbaz"


def test_plain_property_setter():
    text = Text("foo")
    text.plain = "bar"
    assert str(text) == "bar"
    text = Text()
    text.append("Hello, World", "bold")
    text.plain = "Hello"
    assert str(text) == "Hello"
    assert text._spans == [Span(0, 5, "bold")]


def test_from_markup():
    text = Text.from_markup("Hello, [bold]World![/bold]")
    assert str(text) == "Hello, World!"
    assert text._spans == [Span(7, 13, "bold")]


def test_from_ansi():
    text = Text.from_ansi("Hello, \033[1mWorld!\033[0m")
    assert str(text) == "Hello, World!"
    assert text._spans == [Span(7, 13, Style(bold=True))]

    text = Text.from_ansi("Hello, \033[1m\nWorld!\033[0m")
    assert str(text) == "Hello, \nWorld!"
    assert text._spans == [Span(8, 14, Style(bold=True))]

    text = Text.from_ansi("\033[1mBOLD\033[m not bold")
    assert str(text) == "BOLD not bold"
    assert text._spans == [Span(0, 4, Style(bold=True))]

    text = Text.from_ansi("\033[1m\033[Kfoo barmbaz")
    assert str(text) == "foo barmbaz"
    assert text._spans == [Span(0, 11, Style(bold=True))]


def test_copy():
    text = Text()
    text.append("Hello", "bold")
    text.append(" ")
    text.append("World", "italic")
    test_copy = text.copy()
    assert text == test_copy
    assert text is not test_copy


def test_rstrip():
    text = Text("Hello, World!    ")
    text.rstrip()
    assert str(text) == "Hello, World!"


def test_rstrip_end():
    text = Text("Hello, World!    ")
    text.rstrip_end(14)
    assert str(text) == "Hello, World! "


def test_stylize():
    text = Text("Hello, World!")
    text.stylize("bold", 7, 11)
    assert text._spans == [Span(7, 11, "bold")]
    text.stylize("bold", 20, 25)
    assert text._spans == [Span(7, 11, "bold")]


def test_stylize_before():
    text = Text("Hello, World!")
    text.stylize("bold", 0, 5)
    text.stylize_before("italic", 2, 7)
    assert text._spans == [Span(2, 7, "italic"), Span(0, 5, "bold")]


def test_stylize_negative_index():
    text = Text("Hello, World!")
    text.stylize("bold", -6, -1)
    assert text._spans == [Span(7, 12, "bold")]


def test_highlight_regex():
    text = Text("peek-a-boo")

    count = text.highlight_regex(r"NEVER_MATCH", "red")
    assert count == 0
    assert len(text._spans) == 0

    # text: peek-a-boo
    # indx: 0123456789
    count = text.highlight_regex(r"[a|e|o]+", "red")
    assert count == 3
    assert sorted(text._spans) == [
        Span(1, 3, "red"),
        Span(5, 6, "red"),
        Span(8, 10, "red"),
    ]

    text = Text("Ada Lovelace, Alan Turing")
    count = text.highlight_regex(
        r"(?P<yellow>[A-Za-z]+)[ ]+(?P<red>[A-Za-z]+)(?P<NEVER_MATCH>NEVER_MATCH)*"
    )

    # The number of matched name should be 2
    assert count == 2
    assert sorted(text._spans) == [
        Span(0, 3, "yellow"),  # Ada
        Span(4, 12, "red"),  # Lovelace
        Span(14, 18, "yellow"),  # Alan
        Span(19, 25, "red"),  # Turing
    ]


def test_highlight_regex_callable():
    text = Text("Vulnerability CVE-2018-6543 detected")
    re_cve = r"CVE-\d{4}-\d+"

    def get_style(text: str) -> Style:
        return Style.parse(
            f"bold yellow link https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={text}"
        )

    count = text.highlight_regex(re_cve, get_style)
    assert count == 1
    assert len(text._spans) == 1
    assert text._spans[0].start == 14
    assert text._spans[0].end == 27
    assert (
        text._spans[0].style.link
        == "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=CVE-2018-6543"
    )


def test_highlight_words():
    text = Text("Do NOT! touch anything!")
    words = ["NOT", "!"]
    count = text.highlight_words(words, "red")
    assert count == 3
    assert sorted(text._spans) == [
        Span(3, 6, "red"),  # NOT
        Span(6, 7, "red"),  # !
        Span(22, 23, "red"),  # !
    ]

    # regex escape test
    text = Text("[o|u]aeiou")
    words = ["[a|e|i]", "[o|u]"]
    count = text.highlight_words(words, "red")
    assert count == 1
    assert text._spans == [Span(0, 5, "red")]

    # case sensitive
    text = Text("AB Ab aB ab")
    words = ["AB"]

    count = text.highlight_words(words, "red")
    assert count == 1
    assert text._spans == [Span(0, 2, "red")]

    text = Text("AB Ab aB ab")
    count = text.highlight_words(words, "red", case_sensitive=False)
    assert count == 4


def test_set_length():
    text = Text("Hello")
    text.set_length(5)
    assert text == Text("Hello")

    text = Text("Hello")
    text.set_length(10)
    assert text == Text("Hello     ")

    text = Text("Hello World")
    text.stylize("bold", 0, 5)
    text.stylize("italic", 7, 9)

    text.set_length(3)
    expected = Text()
    expected.append("Hel", "bold")
    assert text == expected


def test_console_width():
    console = Console()
    text = Text("Hello World!\nfoobarbaz")
    assert text.__rich_measure__(console, 80) == Measurement(9, 12)
    assert Text(" " * 4).__rich_measure__(console, 80) == Measurement(4, 4)
    assert Text(" \n  \n   ").__rich_measure__(console, 80) == Measurement(3, 3)


def test_join():
    text = Text("bar").join([Text("foo", "red"), Text("baz", "blue")])
    assert str(text) == "foobarbaz"
    assert text._spans == [Span(0, 3, "red"), Span(6, 9, "blue")]


def test_trim_spans():
    text = Text("Hello")
    text._spans[:] = [Span(0, 3, "red"), Span(3, 6, "green"), Span(6, 9, "blue")]
    text._trim_spans()
    assert text._spans == [Span(0, 3, "red"), Span(3, 5, "green")]


def test_pad_left():
    text = Text("foo")
    text.pad_left(3, "X")
    assert str(text) == "XXXfoo"


def test_pad_right():
    text = Text("foo")
    text.pad_right(3, "X")
    assert str(text) == "fooXXX"


def test_append():
    text = Text("foo")
    text.append("bar")
    assert str(text) == "foobar"
    text.append(Text("baz", "bold"))
    assert str(text) == "foobarbaz"
    assert text._spans == [Span(6, 9, "bold")]

    with pytest.raises(ValueError):
        text.append(Text("foo"), "bar")

    with pytest.raises(TypeError):
        text.append(1)


def test_append_text():
    text = Text("foo")
    text.append_text(Text("bar", style="bold"))
    assert str(text) == "foobar"
    assert text._spans == [Span(3, 6, "bold")]


def test_end():
    console = Console(width=20, file=StringIO())
    text = Group(Text.from_markup("foo", end=" "), Text.from_markup("bar"))
    console.print(text)
    assert console.file.getvalue() == "foo bar\n"


def test_split():
    text = Text()
    text.append("foo", "red")
    text.append("\n")
    text.append("bar", "green")
    text.append("\n")

    line1 = Text()
    line1.append("foo", "red")
    line2 = Text()
    line2.append("bar", "green")
    split = text.split("\n")
    assert len(split) == 2
    assert split[0] == line1
    assert split[1] == line2

    assert list(Text("foo").split("\n")) == [Text("foo")]


def test_split_spans():
    text = Text.from_markup("[red]Hello\n[b]World")
    lines = text.split("\n")
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
    text = Text()
    text.append("foobar", "red")
    text.right_crop(3)
    assert str(text) == "foo"
    assert text._spans == [Span(0, 3, "red")]


def test_wrap_3():
    text = Text("foo bar baz")
    lines = text.wrap(Console(), 3)
    print(repr(lines))
    assert len(lines) == 3
    assert lines[0] == Text("foo")
    assert lines[1] == Text("bar")
    assert lines[2] == Text("baz")


def test_wrap_4():
    text = Text("foo bar baz", justify="left")
    lines = text.wrap(Console(), 4)
    assert len(lines) == 3
    assert lines[0] == Text("foo ")
    assert lines[1] == Text("bar ")
    assert lines[2] == Text("baz ")


def test_wrap_wrapped_word_length_greater_than_available_width():
    text = Text("1234 12345678")
    lines = text.wrap(Console(), 7)
    assert lines._lines == [
        Text("1234 "),
        Text("1234567"),
        Text("8"),
    ]


def test_wrap_cjk():
    text = Text("わさび")
    lines = text.wrap(Console(), 4)
    assert lines._lines == [
        Text("わさ"),
        Text("び"),
    ]


def test_wrap_cjk_width_mid_character():
    text = Text("わさび")
    lines = text.wrap(Console(), 3)
    assert lines._lines == [
        Text("わ"),
        Text("さ"),
        Text("び"),
    ]


def test_wrap_cjk_mixed():
    """Regression test covering https://github.com/Textualize/rich/issues/3176 and
    https://github.com/Textualize/textual/issues/3567 - double width characters could
    result in text going missing when wrapping."""
    text = Text("123ありがとうございました")
    console = Console(width=20)  # let's ensure the width passed to wrap() wins.

    wrapped_lines = text.wrap(console, width=8)
    with console.capture() as capture:
        console.print(wrapped_lines)

    assert capture.get() == "123あり\nがとうご\nざいまし\nた\n"


def test_wrap_long():
    text = Text("abracadabra", justify="left")
    lines = text.wrap(Console(), 4)
    assert len(lines) == 3
    assert lines[0] == Text("abra")
    assert lines[1] == Text("cada")
    assert lines[2] == Text("bra ")


def test_wrap_overflow():
    text = Text("Some more words")
    lines = text.wrap(Console(), 4, overflow="ellipsis")
    assert (len(lines)) == 3
    assert lines[0] == Text("Some")
    assert lines[1] == Text("more")
    assert lines[2] == Text("wor…")


def test_wrap_overflow_long():
    text = Text("bigword" * 10)
    lines = text.wrap(Console(), 4, overflow="ellipsis")
    assert len(lines) == 1
    assert lines[0] == Text("big…")


def test_wrap_long_words():
    text = Text("XX 12345678912")
    lines = text.wrap(Console(), 4)

    assert lines._lines == [
        Text("XX "),
        Text("1234"),
        Text("5678"),
        Text("912"),
    ]


def test_wrap_long_words_2():
    # https://github.com/Textualize/rich/issues/2273
    text = Text("Hello, World...123")
    lines = text.wrap(Console(), 10)
    assert lines._lines == [
        Text("Hello, "),
        Text("World...12"),
        Text("3"),
    ]


def test_wrap_long_words_followed_by_other_words():
    """After folding a word across multiple lines, we should continue from
    the next word immediately after the folded word (don't take a newline
    following completion of the folded word)."""
    text = Text("123 12345678 123 123")
    lines = text.wrap(Console(), 6)
    assert lines._lines == [
        Text("123 "),
        Text("123456"),
        Text("78 123"),
        Text("123"),
    ]


def test_wrap_long_word_preceeded_by_word_of_full_line_length():
    """The width of the first word is the same as the available width.
    Ensures that folding works correctly when there's no space available
    on the current line."""
    text = Text("123456 12345678 123 123")
    lines = text.wrap(Console(), 6)
    assert lines._lines == [
        Text("123456"),
        Text("123456"),
        Text("78 123"),
        Text("123"),
    ]


def test_wrap_multiple_consecutive_spaces():
    """Adding multiple consecutive spaces at the end of a line does not impact
    the location at which a break will be added during the process of wrapping."""
    text = Text("123456    12345678 123 123")
    lines = text.wrap(Console(), 6)
    assert lines._lines == [
        Text("123456"),
        Text("123456"),
        Text("78 123"),
        Text("123"),
    ]


def test_wrap_long_words_justify_left():
    text = Text("X 123456789", justify="left")
    lines = text.wrap(Console(), 4)

    assert len(lines) == 4
    assert lines[0] == Text("X   ")
    assert lines[1] == Text("1234")
    assert lines[2] == Text("5678")
    assert lines[3] == Text("9   ")


def test_wrap_leading_and_trailing_whitespace():
    text = Text("   123  456 789   ")
    lines = text.wrap(Console(), 4)
    assert lines._lines == [
        Text("   1"),
        Text("23  "),
        Text("456 "),
        Text("789 "),
    ]


def test_no_wrap_no_crop():
    text = Text("Hello World!" * 3)

    console = Console(width=20, file=StringIO())
    console.print(text, no_wrap=True)
    console.print(text, no_wrap=True, crop=False, overflow="ignore")

    print(repr(console.file.getvalue()))
    assert (
        console.file.getvalue()
        == "Hello World!Hello Wo\nHello World!Hello World!Hello World!\n"
    )


def test_fit():
    text = Text("Hello\nWorld")
    lines = text.fit(3)
    assert str(lines[0]) == "Hel"
    assert str(lines[1]) == "Wor"


def test_wrap_tabs():
    text = Text("foo\tbar", justify="left")
    lines = text.wrap(Console(), 4)
    assert len(lines) == 2
    assert str(lines[0]) == "foo "
    assert str(lines[1]) == "bar "


def test_render():
    console = Console(width=15, record=True)
    text = Text.from_markup(
        "[u][b]Where[/b] there is a [i]Will[/i], there is a Way.[/u]"
    )
    console.print(text)
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
    text = Text("\tHello\tWorld", tab_size=8)
    text.expand_tabs()
    assert text.plain == "        Hello   World"

    text = Text("\tHello\tWorld", tab_size=4)
    text.expand_tabs()
    assert text.plain == "    Hello   World"

    text = Text(".\t..\t...\t....\t", tab_size=4)
    text.expand_tabs()
    assert text.plain == ".   ..  ... ....    "

    text = Text("No Tabs")
    text.expand_tabs()
    assert text.plain == "No Tabs"

    text = Text("No Tabs", style="bold")
    text.expand_tabs()
    assert text.plain == "No Tabs"
    assert text.style == "bold"


@pytest.mark.parametrize(
    "markup,tab_size,expected_text,expected_spans",
    [
        ("", 4, "", []),
        ("\t", 4, "    ", []),
        ("\tbar", 4, "    bar", []),
        ("foo\tbar", 4, "foo bar", []),
        ("foo\nbar\nbaz", 4, "foo\nbar\nbaz", []),
        (
            "[bold]foo\tbar",
            4,
            "foo bar",
            [
                Span(0, 4, "bold"),
                Span(4, 7, "bold"),
            ],
        ),
        (
            "[bold]\tbar",
            4,
            "    bar",
            [
                Span(0, 4, "bold"),
                Span(4, 7, "bold"),
            ],
        ),
        (
            "\t[bold]bar",
            4,
            "    bar",
            [
                Span(4, 7, "bold"),
            ],
        ),
        (
            "[red]foo\tbar\n[green]egg\tbaz",
            8,
            "foo     bar\negg     baz",
            [
                Span(0, 8, "red"),
                Span(8, 12, "red"),
                Span(12, 20, "red"),
                Span(12, 20, "green"),
                Span(20, 23, "red"),
                Span(20, 23, "green"),
            ],
        ),
        (
            "[bold]X\tY",
            8,
            "X       Y",
            [
                Span(0, 8, "bold"),
                Span(8, 9, "bold"),
            ],
        ),
        (
            "[bold]💩\t💩",
            8,
            "💩      💩",
            [
                Span(0, 7, "bold"),
                Span(7, 8, "bold"),
            ],
        ),
        (
            "[bold]💩💩💩💩\t💩",
            8,
            "💩💩💩💩        💩",
            [
                Span(0, 12, "bold"),
                Span(12, 13, "bold"),
            ],
        ),
    ],
)
def test_tabs_to_spaces_spans(
    markup: str, tab_size: int, expected_text: str, expected_spans: List[Span]
):
    """Test spans are correct after expand_tabs"""
    text = Text.from_markup(markup)
    text.expand_tabs(tab_size)
    print(text._spans)
    assert text.plain == expected_text
    assert text._spans == expected_spans


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
    text = Text("foo")
    text.pad(2)
    assert text.plain == "  foo  "


def test_align_left():
    text = Text("foo")
    text.align("left", 10)
    assert text.plain == "foo       "


def test_align_right():
    text = Text("foo")
    text.align("right", 10)
    assert text.plain == "       foo"


def test_align_center():
    text = Text("foo")
    text.align("center", 10)
    assert text.plain == "   foo    "


def test_detect_indentation():
    text = """\
foo
    bar
    """
    assert Text(text).detect_indentation() == 4
    text = """\
foo
    bar
      baz
    """
    assert Text(text).detect_indentation() == 2
    assert Text("").detect_indentation() == 1
    assert Text(" ").detect_indentation() == 1


def test_indentation_guides():
    text = Text(
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
    result = text.with_indent_guides()
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
    # https://github.com/textualize/rich/issues/987
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


def test_markup_property():
    assert Text("").markup == ""
    assert Text("foo").markup == "foo"
    assert Text("foo", style="bold").markup == "[bold]foo[/bold]"
    assert Text.from_markup("foo [red]bar[/red]").markup == "foo [red]bar[/red]"
    assert (
        Text.from_markup("foo [red]bar[/red]", style="bold").markup
        == "[bold]foo [red]bar[/red][/bold]"
    )
    assert (
        Text.from_markup("[bold]foo [italic]bar[/bold] baz[/italic]").markup
        == "[bold]foo [italic]bar[/bold] baz[/italic]"
    )
    assert Text("[bold]foo").markup == "\\[bold]foo"


def test_extend_style():
    text = Text.from_markup("[red]foo[/red] [bold]bar")
    text.extend_style(0)

    assert text.plain == "foo bar"
    assert text.spans == [Span(0, 3, "red"), Span(4, 7, "bold")]

    text.extend_style(-1)
    assert text.plain == "foo bar"
    assert text.spans == [Span(0, 3, "red"), Span(4, 7, "bold")]

    text.extend_style(2)
    assert text.plain == "foo bar  "
    assert text.spans == [Span(0, 3, "red"), Span(4, 9, "bold")]
