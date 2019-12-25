from collections.abc import Mapping


from . import box
from .pretty import Pretty
from .table import Table
from .text import Text


def tabulate_mapping(mapping: Mapping, title: str = None) -> Table:
    """Generate a simple table from a mapping.
    
    Args:
        mapping (Mapping): A mapping object (e.g. a dict);
        title (str, optional): [description]. Optional title to be displayed over the table.
    
    Returns:
        Table: A table instance which may be rendered by the Console.
    """
    table = Table(title=title, box=box.ROUNDED, border_style="blue", padding=0)
    for key, value in mapping.items():
        table.add_row(Pretty(key), Pretty(value))
    return table
