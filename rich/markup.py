from collections import defaultdict
from operator import itemgetter
import re
from typing import Dict, Iterable, List, Match, Optional, Tuple, Union

from .errors import MarkupError
from .style import Style
from .text import Span, Text


re_tags = re.compile(r"(\[\".*?\"\])|(\[.*?\])")
re_emphasize_sub = re.compile(r"\*(.+?)\*|_(.+?)_").sub
re_strong_sub = re.compile(r"\*\*(.+?)\*\*|__(.+?)__").sub
re_strike_sub = re.compile(r"\~(.+?)\~").sub
re_code_sub = re.compile(r"`(.+?)`").sub


def _parse(markup: str) -> Iterable[Tuple[Optional[str], Optional[str]]]:
    """Parse markup in to an iterable of pairs of text, tag.
    
    Args:
        markup (str): A string containing console markup
    
    """

    def repl_strong(match: Match[str]) -> str:
        group = match.group
        return f"[strong]{group(1) or group(2)}[/strong]"

    def repl_emphasize(match: Match[str]) -> str:
        group = match.group
        return f"[emphasize]{group(1) or group(2)}[/emphasize]"

    def repl_strike(match: Match[str]) -> str:
        return f"[strike]{match.group(1)}[/strike]"

    def repl_code(match: Match[str]) -> str:
        return f"[code]{match.group(1)}[/code]"

    markup = re_strong_sub(repl_strong, markup)
    markup = re_emphasize_sub(repl_emphasize, markup)
    markup = re_strike_sub(repl_strike, markup)
    markup = re_code_sub(repl_code, markup)

    position = 0
    for match in re_tags.finditer(markup):
        escaped_text, tag_text = match.groups()

        start, end = match.span()
        if start > position:
            yield markup[position:start], None
        if tag_text is not None:
            yield None, tag_text
        else:
            yield escaped_text[2:-2], None  # type: ignore

        position = end
    if position < len(markup):
        yield markup[position:], None


def render_text(markup: str, style: Union[str, Style] = "") -> Text:
    """Convert markup to Text instance."""
    return Text(markup, style=style)


def render(markup: str, style: Union[str, Style] = "") -> Text:
    """Render console markup in to a Text instance.

    Args:
        markup (str): A string containing console markup.
    
    Raises:
        MarkupError: If there is a syntax error in the markup.
    
    Returns:
        Text: A test instance.
    """
    text = Text(style=style)
    stylize = text.stylize

    styles: Dict[str, List[int]] = defaultdict(list)
    style_stack: List[str] = []

    for plain_text, tag in _parse(markup):
        if plain_text is not None:
            text.append(plain_text)
        if tag is not None:
            if tag.startswith("[/"):
                style_name = tag[2:-1].strip()
                if style_name:
                    style_name = Style.normalize(style_name)
                else:
                    try:
                        style_name = style_stack[-1]
                    except IndexError:
                        raise MarkupError(
                            f"closing tag '[/]' at position {len(text)} has nothing to close"
                        )
                try:
                    style_position = styles[style_name].pop()
                except (KeyError, IndexError):
                    raise MarkupError(
                        f"closing tag {tag!r} at position {len(text)} doesn't match open tag"
                    )
                style_stack.remove(style_name)
                stylize(style_position, len(text), style_name)
            else:
                style_name = Style.normalize(tag[1:-1].strip())
                styles[style_name].append(len(text))
                style_stack.append(style_name)

    text_length = len(text)
    while style_stack:
        style_name = style_stack.pop()
        style_position = styles[style_name].pop()
        text.stylize(style_position, text_length, style_name)

    return text


if __name__ == "__main__":  # pragma: no cover
    text = """*Hello* **World**! [bold blue]~~strike~~[/blue bold] `code`"""

    from .console import Console

    console = Console()
    console.print(render(text))
