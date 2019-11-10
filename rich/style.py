from __future__ import annotations

from dataclasses import dataclass, field, replace, InitVar
from functools import lru_cache
import sys
from typing import Dict, Iterable, List, Mapping, Optional

from . import errors
from .color import Color


@dataclass
class Style:
    """A terminal style."""

    color: Optional[str] = None
    back: Optional[str] = None
    bold: Optional[bool] = None
    dim: Optional[bool] = None
    italic: Optional[bool] = None
    underline: Optional[bool] = None
    blink: Optional[bool] = None
    blink2: Optional[bool] = None
    reverse: Optional[bool] = None
    strike: Optional[bool] = None

    _color: Optional[Color] = field(init=False, default=None, repr=False)
    _back: Optional[Color] = field(init=False, default=None, repr=False)

    def __str__(self) -> str:
        """Re-generate style definition from attributes."""
        attributes: List[str] = []
        append = attributes.append
        if self.bold is not None:
            append("bold" if self.bold else "not bold")
        if self.dim is not None:
            append("dim" if self.dim else "not dim")
        if self.italic is not None:
            append("italic" if self.italic else "not italic")
        if self.underline is not None:
            append("underline" if self.underline else "not underline")
        if self.blink is not None:
            append("blink" if self.blink else "not blink")
        if self.blink2 is not None:
            append("blink2" if self.blink2 else "not blink2")
        if self.reverse is not None:
            append("reverse" if self.reverse else "not reverse")
        if self.strike is not None:
            append("strike" if self.strike else "not strike")
        if self._color is not None:
            append(self._color.name)
        if self._back is not None:
            append("on")
            append(self._back.name)
        return " ".join(attributes) or "none"

    def __repr__(self):
        return f"<style '{self}'>"

    def __post_init__(self) -> None:
        if self.color:
            self._color = Color.parse(self.color)
        if self.back:
            self._back = Color.parse(self.back)

    @classmethod
    def reset(cls) -> Style:
        """Get a style to reset all attributes."""
        return Style(
            color="default",
            back="default",
            dim=False,
            bold=False,
            italic=False,
            underline=False,
            blink=False,
            blink2=False,
            reverse=False,
            strike=False,
        )

    @classmethod
    def parse(cls, style_definition: str) -> Style:
        """Parse style name(s) in to style object."""
        style_attributes = {
            "dim",
            "bold",
            "italic",
            "underline",
            "blink",
            "blink2",
            "reverse",
            "strike",
        }
        color: Optional[str] = None
        back: Optional[str] = None
        attributes: Dict[str, Optional[bool]] = {}

        words = iter(style_definition.split())
        for original_word in words:
            word = original_word.lower()
            if word == "on":
                word = next(words, "")
                if not word:
                    raise errors.StyleSyntaxError("color expected after 'on'")
                if Color.parse(word) is None:
                    raise errors.StyleSyntaxError(
                        f"color expected after 'on', found {original_word!r}"
                    )
                back = word

            elif word == "not":
                word = next(words, "")
                if word not in style_attributes:
                    raise errors.StyleSyntaxError(
                        f"expected style attribute after 'not', found {original_word!r}"
                    )
                attributes[word] = False

            elif word in style_attributes:
                attributes[word] = True

            else:
                if Color.parse(word) is None:
                    raise errors.StyleSyntaxError(
                        f"unknown word {original_word!r} in style {style_definition!r}"
                    )
                color = word
        style = Style(color=color, back=back, **attributes)
        return style

    @classmethod
    def combine(self, styles: Iterable[Style]) -> Style:
        """Combine styles and get result.
        
        Args:
            styles (Iterable[Style]): Styles to combine.
        
        Returns:
            Style: A new style instance.
        """

        style = Style()
        for _style in styles:
            style = style.apply(_style)
        return style

    def copy(self) -> Style:
        """Get a copy of this style.
        
        Returns:
            Style: A new Style instance with identical attributes.
        """
        return replace(self)

    def render(
        self, text: str = "", *, current_style: Style = None, reset=False
    ) -> str:
        """Render the ANSI codes to implement the style."""
        attrs: List[str] = []
        append = attrs.append

        if current_style is None:
            current = RESET_STYLE
        else:
            current = current_style

        if self._color is not None and current._color != self._color:
            attrs.extend(self._color.get_ansi_codes())

        if self._back is not None and current._back != self._back:
            attrs.extend(self._back.get_ansi_codes(foreground=False))

        if self.bold is not None and current.bold != self.bold:
            append("1" if self.bold else "21")

        if self.dim is not None and current.dim != self.dim:
            append("2" if self.dim else "22")

        if self.italic is not None and current.italic != self.italic:
            append("3" if self.italic else "23")

        if self.underline is not None and current.underline != self.underline:
            append("4" if self.underline else "24")

        if self.blink is not None and current.blink != self.blink:
            append("5" if self.blink else "25")

        if self.blink2 is not None and current.blink2 != self.blink2:
            append("6" if self.blink2 else "26")

        if self.reverse is not None and current.reverse != self.reverse:
            append("7" if self.reverse else "27")

        if self.strike is not None and current.strike != self.strike:
            append("9" if self.strike else "29")

        reset = "\x1b[0m" if reset else ""
        return f"\x1b[{';'.join(attrs)}m{text or ''}{reset}"

    def test(self, text: Optional[str] = None) -> None:
        """Write test text with style to terminal.
        
        Args:
            text (Optional[str], optional): Text to style or None for style name.
        
        Returns:
            None:
        """
        text = text or str(self)
        sys.stdout.write(f"{self.render(text)}\x1b[0m\n")

    def apply(self, style: Optional[Style]) -> Style:
        """Merge this style with another.
        
        Args:
            style (Optional[Style]): A style object to copy attributes from. 
                If `style` is `None`, then a copy of this style will be returned.
        
        Returns:
            (Style): A new style with combined attributes.

        """
        if style is None:
            return self
        style = Style(
            color=self.color if style.color is None else style.color,
            back=self.back if style.back is None else style.back,
            dim=self.dim if style.dim is None else style.dim,
            bold=self.bold if style.bold is None else style.bold,
            italic=self.italic if style.italic is None else style.italic,
            underline=self.underline if style.underline is None else style.underline,
            blink=self.blink if style.blink is None else style.blink,
            blink2=self.blink2 if style.blink2 is None else style.blink2,
            reverse=self.reverse if style.reverse is None else style.reverse,
        )
        return style


RESET_STYLE = Style.reset()

if __name__ == "__main__":
    import sys

    # style = Style(color="blue", bold=True, italic=True, reverse=False, dim=True)

    style = Style.parse("bold")
    print(style)
    print(repr(style))

    style.test()

