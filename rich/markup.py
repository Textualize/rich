import re
from typing import Iterable, List, NamedTuple, Optional, Tuple, Union

from .errors import MarkupError
from .style import Style
from .text import Span, Text
from ._emoji_replace import _emoji_replace


RE_TAGS = re.compile(
    r"""
(\\\[)|
\[([a-z#\/].*?)\]
""",
    re.VERBOSE,
)


class Tag(NamedTuple):
    """A tag in console markup."""

    name: str
    """The tag name. e.g. 'bold'."""
    parameters: Optional[str]
    """Any additional parameters after the name."""

    def __str__(self) -> str:
        return (
            self.name if self.parameters is None else f"{self.name} {self.parameters}"
        )

    @property
    def markup(self) -> str:
        return (
            f"[{self.name}]"
            if self.parameters is None
            else f"[{self.name}={self.parameters}]"
        )


def escape(markup: str) -> str:
    """Escapes text so that it won't be interpreted as markup.

    Args:
        markup (str): Content to be inserted in to markup.

    Returns:
        str: Markup with square brackets escaped.
    """
    return markup.replace("[", r"\[")


def _parse(markup: str) -> Iterable[Tuple[int, Optional[str], Optional[Tag]]]:
    """Parse markup in to an iterable of tuples of (position, text, tag).

    Args:
        markup (str): A string containing console markup

    """
    position = 0
    for match in RE_TAGS.finditer(markup):
        (escape_open, tag_text) = match.groups()
        start, end = match.span()
        if start > position:
            yield start, markup[position:start], None
        if escape_open:
            yield start, "[", None
        else:
            text, equals, parameters = tag_text.partition("=")
            if equals:
                yield start, None, Tag(text, parameters)
            else:
                yield start, None, Tag(tag_text.strip(), None)
        position = end
    if position < len(markup):
        yield position, markup[position:], None


def render(markup: str, style: Union[str, Style] = "", emoji: bool = True) -> Text:
    """Render console markup in to a Text instance.

    Args:
        markup (str): A string containing console markup.
        emoji (bool, optional): Also render emoji code. Defaults to True.

    Raises:
        MarkupError: If there is a syntax error in the markup.

    Returns:
        Text: A test instance.
    """
    emoji_replace = _emoji_replace
    if "[" not in markup:
        return Text(emoji_replace(markup) if emoji else markup, style=style)
    text = Text(style=style)
    append = text.append
    normalize = Style.normalize

    style_stack: List[Tuple[int, Tag]] = []
    pop = style_stack.pop

    spans: List[Span] = []
    append_span = spans.append

    _Span = Span

    def pop_style(style_name: str) -> Tuple[int, Tag]:
        """Pop tag matching given style name."""
        for index, (_, tag) in enumerate(reversed(style_stack), 1):
            if tag.name == style_name:
                return pop(-index)
        raise KeyError(style_name)

    for position, plain_text, tag in _parse(markup):
        if plain_text is not None:
            append(emoji_replace(plain_text) if emoji else plain_text)
        elif tag is not None:
            if tag.name.startswith("/"):  # Closing tag
                style_name = tag.name[1:].strip()
                if style_name:  # explicit close
                    style_name = normalize(style_name)
                    try:
                        start, open_tag = pop_style(style_name)
                    except KeyError:
                        raise MarkupError(
                            f"closing tag '{tag.markup}' at position {position} doesn't match any open tag"
                        )
                else:  # implicit close
                    try:
                        start, open_tag = pop()
                    except IndexError:
                        raise MarkupError(
                            f"closing tag '[/]' at position {position} has nothing to close"
                        )

                append_span(_Span(start, len(text), str(open_tag)))
            else:  # Opening tag
                normalized_tag = Tag(normalize(tag.name), tag.parameters)
                style_stack.append((len(text), normalized_tag))

    text_length = len(text)
    while style_stack:
        start, tag = style_stack.pop()
        append_span(_Span(start, text_length, str(tag)))

    text.spans = sorted(spans)
    return text


if __name__ == "__main__":  # pragma: no cover
    # from rich import print
    from rich.console import Console
    from rich.text import Text

    console = Console(highlight=False)

    # t = Text.from_markup('Hello [link="https://www.willmcgugan.com"]W[b]o[/b]rld[/]!')
    # print(repr(t._spans))

    console.print("Hello [1], [1,2,3] ['hello']")
    console.print("foo")
    console.print("Hello [link=https://www.willmcgugan.com]W[b]o[/b]rld[/]!")

    # console.print("[bold]1 [not bold]2[/] 3[/]")

    # console.print("[green]XXX[blue]XXX[/]XXX[/]")
