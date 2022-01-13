from rich import cells


def test_cell_len_empty_string():
    assert cells.cell_len("") == 0


def test_cell_len_single_ascii_char():
    assert cells.cell_len("a") == 1


def test_cell_len_single_ascii_num():
    assert cells.cell_len("5") == 1


def test_cell_len_ascii_string():
    assert cells.cell_len("hello") == len("hello")


def test_cell_len_zero_width_character():
    assert cells.cell_len("\u0483") == 0


def test_cell_len_single_width_non_ascii_character():
    assert cells.cell_len("\u0370") == 1


def test_cell_len_japanese_hiragana():
    assert cells.cell_len("こんにちは") == 10


def test_cell_len_poop_emoji_has_width_2():
    assert cells.cell_len("💩") == 2


def test_cell_len_emoji_presentation_sequence():
    # Handled different from standard emoji - we vary from wcwidth here, which reports width 1.
    assert cells.cell_len("🏵️") == 2


def test_set_cell_size():
    assert cells.set_cell_size("foo", 0) == ""
    assert cells.set_cell_size("f", 0) == ""
    assert cells.set_cell_size("", 0) == ""
    assert cells.set_cell_size("😽😽", 0) == ""
    assert cells.set_cell_size("foo", 2) == "fo"
    assert cells.set_cell_size("foo", 3) == "foo"
    assert cells.set_cell_size("foo", 4) == "foo "
    assert cells.set_cell_size("😽😽", 4) == "😽😽"
    assert cells.set_cell_size("😽😽", 3) == "😽 "
    assert cells.set_cell_size("😽😽", 2) == "😽"
    assert cells.set_cell_size("😽😽", 1) == " "
    assert cells.set_cell_size("😽😽", 5) == "😽😽 "


def test_set_cell_size_infinite():
    for size in range(38):
        assert (
            cells.cell_len(
                cells.set_cell_size(
                    "เป็นเกมที่ต้องมีความอดทนมากที่สุดตั้งเเต่เคยเล่นมา", size
                )
            )
            == size
        )
