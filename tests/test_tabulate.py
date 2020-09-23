import itertools
from rich.style import Style
from rich.table import _Cell
from rich.tabulate import tabulate_mapping


def test_tabulate_mapping():
    # TODO: tabulate_mapping may not be needed shortly
    table = tabulate_mapping({"foo": "1", "bar": "2"})
    assert len(table.columns) == 2
    assert len(table.columns[0]._cells) == 2
    assert len(table.columns[1]._cells) == 2

    # add tests for title and caption justification
    test_title = "Foo v. Bar"
    test_caption = "approximate results"
    for title_justify, caption_justify in itertools.product(
        [None, "left", "center", "right"], repeat=2
    ):
        table = tabulate_mapping(
            {"foo": "1", "bar": "2"},
            title=test_title,
            caption=test_caption,
            title_justify=title_justify,
            caption_justify=caption_justify,
        )
        expected_title_justify = (
            title_justify if title_justify is not None else "center"
        )
        expected_caption_justify = (
            caption_justify if caption_justify is not None else "center"
        )
        assert expected_title_justify == table.title_justify
        assert expected_caption_justify == table.caption_justify
