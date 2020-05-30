import re
from typing import Match, Union

from .console import Console, ConsoleOptions, ConsoleRenderable, RenderResult
from .jupyter import JupyterMixin
from .segment import Segment
from .style import Style
from ._emoji_codes import EMOJI
from ._emoji_replace import _emoji_replace


class NoEmoji(Exception):
    """No emoji by that name."""


class Emoji(JupyterMixin):
    __slots__ = ["name", "style", "_char"]

    def __init__(self, name: str, style: Union[str, Style] = "none") -> None:
        """A single emoji character.
        
        Args:
            name (str): Name of emoji.
            style (Union[str, Style], optional): Optional style. Defaults to None.
        
        Raises:
            NoEmoji: If the emoji doesn't exist.
        """
        self.name = name
        self.style = style
        try:
            self._char = EMOJI[name]
        except KeyError:
            raise NoEmoji(f"No emoji called {name!r}")

    @classmethod
    def replace(cls, text: str) -> str:
        """Replace emoji markup with coresponding unicode characters.
        
        Args:
            text (str): A string with emojis codes, e.g. "Hello :smiley:!"
        
        Returns:
            str: A string with emoji codes replaces with actual emoji.
        """
        return _emoji_replace(text)

    def __repr__(self) -> str:
        return f"<emoji {self.name!r}>"

    def __str__(self) -> str:
        return self._char

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        yield Segment(self._char, console.get_style(self.style))


if __name__ == "__main__":  # pragma: no cover
    from .console import Console

    c = Console(markup=False)

    e = Emoji("thumbs_up")
    print(repr(e))
    print(e)

    c.print(Emoji("thumbs_up"))
    # c.print("Hello")
    c.print("Hello World")
    from .panel import Panel

    c.print(Panel(Emoji.replace("Hello, :smiley: ! :thumbs_up: :sfwdfwer:")))

    c.print("Here is a :smiley:  :link: Hello World")

    c.print(":beer:")
