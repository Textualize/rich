"""A global instance of a Console."""

from .console import Console
from . import jupyter

console = jupyter.get_console() if jupyter.is_jupyter() else Console()
