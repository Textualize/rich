from collections.abc import Mapping


from . import box
from .highlighter import ReprHighlighter
from .pretty import Pretty
from .table import Table


def tabulate_mapping(mapping: Mapping, title: str = None) -> Table:
    """Generate a simple table from a mapping.
    
    Args:
        mapping (Mapping): A mapping object (e.g. a dict);
        title (str, optional): Optional title to be displayed over the table.
    
    Returns:
        Table: A table instance which may be rendered by the Console.
    """
    table = Table(show_header=False, title=title, box=box.ROUNDED, border_style="blue")
    table.title = title
    highlighter = ReprHighlighter()
    for key, value in mapping.items():
        table.add_row(
            Pretty(key, highlighter=highlighter), Pretty(value, highlighter=highlighter)
        )
    return table


if __name__ == "__main__":  # pragma: no cover

    from rich import print

    def test(foo, bar):
        list_of_things = [1, 2, 3, None, 4, True, False, "Hello World"]
        dict_of_things = {
            "version": "1.1",
            "method": "confirmFruitPurchase",
            "params": [["apple", "orange", "mangoes", "pomelo"], 1.123],
            "id": "194521489",
        }
        print(tabulate_mapping(locals()))

    print()
    test(20.3423, 3.1427)
    print()
