from rich.console import Console
from rich.text import Text

console = Console()
long_text = "This is a very long line that should wrap in the terminal. " * 3
colored_text = Text(long_text, style="on blue")

console.print(colored_text)
