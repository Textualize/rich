from rich.cells import cell_len


def test_cell_len_zwj_does_not_raise() -> None:
    cell_len("\u200d")
    cell_len("a\u200d")
    cell_len("a\u200d\n b")
    cell_len("a\u200d b(")
