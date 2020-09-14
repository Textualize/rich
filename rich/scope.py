from typing import Any, Tuple, TYPE_CHECKING

from collections.abc import Mapping

from .highlighter import ReprHighlighter
from .panel import Panel
from .pretty import Pretty
from .text import Text, TextType
from .table import Table


if TYPE_CHECKING:
    from .console import ConsoleRenderable, RenderableType


def render_scope(
    scope: Mapping, *, title: TextType = None, sort_keys: bool = True
) -> "ConsoleRenderable":
    """Render python variables in a given scope.

    Args:
        scope (Mapping): A mapping containing variable names and values.
        title (str, optional): Optional title. Defaults to None.
        sort_keys (bool, optional): Enable sorting of items. Defaults to True.

    Returns:
        RenderableType: A renderable object.
    """
    highlighter = ReprHighlighter()
    items_table = Table.grid(padding=(0, 1), expand=False)
    items_table.add_column(justify="right")

    def sort_items(item: Tuple[str, Any]) -> Tuple[bool, str]:
        """Sort special variables first, then alphabetically."""
        key, _ = item
        return (not key.startswith("__"), key.lower())

    items = sorted(scope.items(), key=sort_items) if sort_keys else scope.items()
    for key, value in items:
        key_text = Text.assemble(
            (key, "scope.key.special" if key.startswith("__") else "scope.key"),
            (" =", "scope.equals"),
        )
        items_table.add_row(key_text, Pretty(value, highlighter=highlighter))
    return Panel.fit(
        items_table,
        title=title,
        border_style="scope.border",
        padding=(0, 1),
    )


if __name__ == "__main__":  # pragma: no cover
    from rich import print

    print()

    def test(foo, bar):
        list_of_things = [1, 2, 3, None, 4, True, False, "Hello World"]
        dict_of_things = {
            "version": "1.1",
            "method": "confirmFruitPurchase",
            "params": [["apple", "orange", "mangoes", "pomelo"], 1.123],
            "id": "194521489",
        }
        print(render_scope(locals(), title="[i]locals", sort_keys=False))

    test(20.3423, 3.1427)
    print()
