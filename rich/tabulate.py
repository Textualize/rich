from collections.abc import Mapping


from . import box
from .highlighter import ReprHighlighter
from .pretty import Pretty
from .table import Table

_NOT_PROVIDED = object()


def tabulate_mapping(
    mapping: Mapping,
    title: str = None,
    caption: str = None,
    title_justify: str = _NOT_PROVIDED,
    caption_justify: str = _NOT_PROVIDED,
) -> Table:
    """Generate a simple table from a mapping.

    Args:
        mapping (Mapping): A mapping object (e.g. a dict);
        title (str, optional): Optional title to be displayed over the table.
        caption (str, optional): Optional caption to be displayed below the table.
        title_justify (str, optional): Optional "right", "center", "left" string indicating title justification
        caption_justify (str, optional): Optional "right", "center", "left" string indicating caption justification

    Returns:
        Table: A table instance which may be rendered by the Console.
    """
    table = Table(
        show_header=False,
        title=title,
        caption=caption,
        box=box.ROUNDED,
        border_style="blue",
    )
    table.title = title
    table.caption = caption
    if title_justify is not _NOT_PROVIDED:
        table.title_justify = title_justify
    if caption_justify is not _NOT_PROVIDED:
        table.caption_justify = caption_justify
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
        print(
            tabulate_mapping(
                locals(),
                title="locals()",
                caption="__main__.test",
                caption_justify="right",
            )
        )

    print()
    test(20.3423, 3.1427)
    print()
