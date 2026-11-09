"""
Demonstration of Syntax.stylize_range
"""

from rich.console import Console
from rich.style import Style
from rich.syntax import Syntax

console = Console()

# Example 1: Single-line code
code1 = "example = True"
syntax1 = Syntax(code1, "python")
syntax1.stylize_range(Style(bgcolor="bright_yellow"), (1, 10), (1, 14))
console.print("Example 1 - Highlight 'True':")
console.print(syntax1)

# Example 2: Multi-line code with line numbers
code2 = """def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)"""
syntax2 = Syntax(code2, "python", line_numbers=True)
# Highlight "return n" on line 3
syntax2.stylize_range(Style(bgcolor="deep_sky_blue4", bold=True), (3, 4), (3, 13))
console.print("\nExample 2 - Highlight 'return n' (with line numbers):")
console.print(syntax2)
