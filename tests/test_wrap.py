from rich._wrap import divide_line


def test_divide_line_keep_whitespace():
    text = "foo bar     baz"
    result = divide_line(text, 10, keep_whitespace=True)
    assert result == [4, 12]


def test_divide_line_keep_whitespace_double_width():
    text = "あああ foo bar    baz"
    #             4    8   indices
    #             67890    widths
    result = divide_line(text, 10, keep_whitespace=True)
    assert result == [4, 8]
