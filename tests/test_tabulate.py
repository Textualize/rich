from rich.style import Style
from rich.table import _Cell
from rich.tabulate import tabulate_mapping


def test_tabulate_mapping():
    # TODO: tabulate_mapping may not be needed shortly
    table = tabulate_mapping({"foo": "1", "bar": "2"})
    assert len(table.columns) == 2
    assert len(table.columns[0]._cells) == 2
    assert len(table.columns[1]._cells) == 2
