"""
Demonstration of syntax.stylize_range
"""

from rich.console import Console
from rich.style import Style
from rich.syntax import Syntax

console = Console()

syntax = Syntax("example = True", "python")

syntax.stylize_range(Style(bgcolor="deep_pink4"), (1, 10), (1, 14))

console.print("Example 1")
console.print(syntax)
console.print("\nExample 2")
syntax = Syntax("123\n456\n789", "python")

syntax.stylize_range(Style(bgcolor="deep_pink4"), (2, 0), (2, 3))

console.print(syntax)
