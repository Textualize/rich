from rich import cells


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
