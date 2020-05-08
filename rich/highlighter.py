from abc import ABC, abstractmethod
from re import finditer
from typing import List, Union


from .text import Text


class Highlighter(ABC):
    """Abstract base class for highlighters."""

    def __call__(self, text: Union[str, Text]) -> Text:
        """Highlight a str or Text instance.
        
        Args:
            text (Union[str, ~Text]): Text to highlight.
        
        Raises:
            TypeError: If not called with text or str.
        
        Returns:
            Text: A test instance with highlighting applied.
        """
        if isinstance(text, str):
            highlight_text = Text(text)
        elif isinstance(text, Text):
            highlight_text = text.copy()
        else:
            raise TypeError(f"str or Text instance required, not {text!r}")
        self.highlight(highlight_text)
        return highlight_text

    @abstractmethod
    def highlight(self, text: Text) -> None:
        """Apply highlighting in place to text.
        
        Args:
            text (~Text): A text object highlight.
        """


class NullHighlighter(Highlighter):
    """A highlighter object that doesn't highlight.
    
    May be used to disable highlighting entirely.
    
    """

    def highlight(self, text: Text) -> None:
        """Nothing to do"""


class RegexHighlighter(Highlighter):
    """Applies highlighting from a list of regular expressions."""

    highlights: List[str] = []
    base_style: str = ""

    def highlight(self, text: Text) -> None:
        """Highlight :class:`rich.text.Text` using regular expressions.
        
        Args:
            text (~Text): Text to highlighted.
        
        """
        highlight_regex = text.highlight_regex
        for re_highlight in self.highlights:
            highlight_regex(re_highlight, style_prefix=self.base_style)


class ReprHighlighter(RegexHighlighter):
    """Highlights the text typically produced from ``__repr__`` methods."""

    base_style = "repr."
    highlights = [
        r"(?P<brace>[\{\[\(\)\]\}])",
        r"(?P<tag_start>\<)(?P<tag_name>\w*)(?P<tag_contents>.*?)(?P<tag_end>\>)",
        r"(?P<attrib_name>\w+?)=(?P<attrib_value>\"?\w+\"?)",
        r"(?P<bool_true>True)|(?P<bool_false>False)|(?P<none>None)",
        r"(?P<number>(?<!\w)\-?[0-9]+\.?[0-9]*\b)",
        r"(?P<number>0x[0-9a-f]*)",
        r"(?P<path>(\/\w+)+\/)",
        r"(?P<filename>\/\w*\.\w{3,4})\s",
        r"(?<!\\)(?P<str>b?\'\'\'.*?(?<!\\)\'\'\'|b?\'.*?(?<!\\)\'|b?\"\"\".*?(?<!\\)\"\"\"|b?\".*?(?<!\\)\")",
        r"(?P<url>https?:\/\/[0-9a-zA-Z\$\-\_\+\!`\(\)\,\.\?\/\;\:\&\=\%]*)",
        r"(?P<uuid>[a-fA-F0-9]{8}\-[a-fA-F0-9]{4}\-[a-fA-F0-9]{4}\-[a-fA-F0-9]{4}\-[a-fA-F0-9]{12})",
    ]


if __name__ == "__main__":  # pragma: no cover
    from .console import Console

    console = Console()
    console.print("[bold green]hello world![/bold green]")
    console.print("'[bold green]hello world![/bold green]'")
