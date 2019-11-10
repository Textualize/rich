from typing import Dict

from .style import Style

DEFAULT_STYLES: Dict[str, Style] = {
    "none": Style(),
    "reset": Style.reset(),
    "dim": Style(dim=True),
    "bright": Style(dim=False),
    "bold": Style(bold=True),
    "b": Style(bold=True),
    "italic": Style(italic=True),
    "i": Style(italic=True),
    "underline": Style(underline=True),
    "u": Style(underline=True),
    "blink": Style(blink=True),
    "blink2": Style(blink2=True),
    "reverse": Style(reverse=True),
    "strike": Style(strike=True),
    "s": Style(strike=True),
    "black": Style(color="black"),
    "red": Style(color="red"),
    "green": Style(color="green"),
    "yellow": Style(color="yellow"),
    "magenta": Style(color="magenta"),
    "cyan": Style(color="cyan"),
    "white": Style(color="white"),
    "on_black": Style(back="black"),
    "on_red": Style(back="red"),
    "on_green": Style(back="green"),
    "on_yellow": Style(back="yellow"),
    "on_magenta": Style(back="magenta"),
    "on_cyan": Style(back="cyan"),
    "on_white": Style(back="white"),
}

MARKDOWN_STYLES = {
    "markdown.text": Style(),
    "markdown.emph": Style(italic=True),
    "markdown.strong": Style(bold=True),
    "markdown.code": Style(dim=True),
    "markdown.code_block": Style(dim=True),
    "markdown.heading1": Style(bold=True),
    "markdown.heading2": Style(bold=True, dim=True),
    "markdown.heading3": Style(bold=True),
    "markdown.heading4": Style(bold=True),
    "markdown.heading5": Style(bold=True),
    "markdown.heading6": Style(bold=True),
    "markdown.heading7": Style(bold=True),
}
DEFAULT_STYLES.update(MARKDOWN_STYLES)
