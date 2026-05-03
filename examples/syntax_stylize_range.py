"""Demonstration of Syntax.stylize_range to highlight portions of code."""

from rich.console import Console
from rich.style import Style
from rich.syntax import Syntax

console = Console()

# Example 1: Highlight a single token on one line
code = "example = True"
syntax = Syntax(code, "python")
syntax.stylize_range(Style(bgcolor="red"), (1, 10), (1, 14))
console.print("Example 1 – highlight 'True' on line 1:")
console.print(syntax)

# Example 2: Highlight part of a multi-line snippet
code = "123\n456\n789"
syntax = Syntax(code, "python")
syntax.stylize_range(Style(bgcolor="red"), (2, 0), (2, 3))
console.print("\nExample 2 – highlight '456' on line 2:")
console.print(syntax)

# Example 3: Highlight a range spanning multiple lines
code = "def greet(name):\n    return f'Hello {name}'"
syntax = Syntax(code, "python")
syntax.stylize_range(Style(bgcolor="red"), (1, 4), (2, 22))
console.print("\nExample 3 – highlight across lines 1–2:")
console.print(syntax)
