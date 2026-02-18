import pytest
from rich._wrap import divide_line


def test_short_sentence_wide_width():
    result = divide_line("hello world", 20)
    assert result == []


def test_no_text():
    result = divide_line("", 10)
    assert result == []


def test_single_word_at_limit():
    result = divide_line("hello", 5)
    assert result == []


def test_second_word_overflow():
    result = divide_line("hello world", 8)
    assert result == [6]


def test_three_words_tight():
    result = divide_line("aa bb cc", 3)
    assert len(result) == 2


def test_four_chunk_fold():
    result = divide_line("abcdefghij", 3)
    assert result == [3, 6, 9]


def test_two_chunk_fold():
    result = divide_line("abcdef", 3)
    assert result == [3]


def test_fold_after_prefix():
    result = divide_line("hi abcdefghij", 5)
    assert 3 in result


def test_no_fold_long_word_beginning():
    result = divide_line("abcdefghij", 3, fold=False)
    assert result == []


def test_no_fold_long_word_mid_sentence():
    result = divide_line("hi abcdefghij", 5, fold=False)
    assert result == [3]


def test_spaces_only():
    result = divide_line("     ", 5)
    assert result == []