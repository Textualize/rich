from rich.highlighter import RegexHighlighter


class EmailHighlighter(RegexHighlighter):
    """Apply style to anything that looks like an email."""

    base_style = "example."
    highlights = [r"(?P<email>[\w-]+@([\w-]+\.)+[\w-]+)"]


from rich.console import Console
from rich.style import Style
from rich.theme import Theme

theme = Theme({"example.email": "bold magenta"})
console = Console(highlighter=EmailHighlighter(), theme=theme)

console.print("Send funds to money@example.org")
