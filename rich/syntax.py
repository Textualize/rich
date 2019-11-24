from __future__ import annotations

import textwrap
from typing import Any, Dict

from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name
from pygments.util import ClassNotFound

from .style import Style
from .text import Text


# def _get_pygments_style(style, name:str) -> Style:
#     syle.


def highlight(
    lexer_name: str, code: str, *, style_name: str = "monokai", dedent: bool = True
) -> Text:

    if dedent:
        code = textwrap.dedent(code)
    try:
        pygments_style_class = get_style_by_name(style_name)
    except ClassNotFound:
        return Text(code)

    style_cache: Dict[Any, Style] = {}

    lexer = get_lexer_by_name(lexer_name)
    background_style = Style(bgcolor=pygments_style_class.background_color)
    text = Text(style=background_style)
    for token_type, token in lexer.get_tokens(code):
        if token_type in style_cache:
            style = style_cache[token_type]
        else:
            pygments_style = pygments_style_class.style_for_token(token_type)
            color = pygments_style["color"]
            bgcolor = pygments_style["bgcolor"]
            style = Style(
                color="#" + color if color else None,
                bgcolor="#" + bgcolor if bgcolor else None,
                bold=pygments_style["bold"],
                italic=pygments_style["italic"],
                underline=pygments_style["underline"],
            )
            style_cache[token_type] = style
        text.append(token, style)

    return text


CODE = """
    @property
    def width(self) -> int:
        \"\"\"Get the width of the console.
        
        Returns:
            int: The width (in characters) of the console.
        \"\"\"
        width, _ = self.size
        return width
"""

if __name__ == "__main__":

    text = highlight("python", CODE)

    from .console import Console

    c = Console()
    c.print(text)

    for line in text.split():
        print()
        print(repr(line.text))
        print(line._spans)
