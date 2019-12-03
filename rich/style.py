from __future__ import annotations

from functools import lru_cache
import sys
from typing import Any, Dict, Iterable, List, Mapping, Optional, Type

from . import errors
from .color import Color, ColorParseError, ColorSystem
from . import themes
from .theme import Theme


class _Bit:
    """A descriptor to get/set a style attribute bit."""

    def __init__(self, bit_no: int) -> None:
        self.bit = 1 << bit_no

    def __get__(self, obj: Style, objtype: Type[Style]) -> Optional[bool]:
        if obj._set_attributes & self.bit:
            return obj._attributes & self.bit != 0
        return None


class Style:
    """A terminal style."""

    def __init__(
        self,
        *,
        color: str = None,
        bgcolor: str = None,
        bold: bool = None,
        dim: bool = None,
        italic: bool = None,
        underline: bool = None,
        blink: bool = None,
        blink2: bool = None,
        reverse: bool = None,
        conceal: bool = None,
        strike: bool = None,
    ):
        self._color = None if color is None else Color.parse(color)
        self._bgcolor = None if bgcolor is None else Color.parse(bgcolor)
        _bool = bool
        self._attributes = (
            (bold or 0)
            | (dim or 0) << 1
            | (italic or 0) << 2
            | (underline or 0) << 3
            | (blink or 0) << 4
            | (blink2 or 0) << 5
            | (reverse or 0) << 6
            | (conceal or 0) << 7
            | (strike or 0) << 8
        )
        self._set_attributes = (
            (bold is not None)
            | (dim is not None) << 1
            | (italic is not None) << 2
            | (underline is not None) << 3
            | (blink is not None) << 4
            | (blink2 is not None) << 5
            | (reverse is not None) << 6
            | (conceal is not None) << 7
            | (strike is not None) << 8
        )

    bold = _Bit(0)
    dim = _Bit(1)
    italic = _Bit(2)
    underline = _Bit(3)
    blink = _Bit(4)
    blink2 = _Bit(5)
    reverse = _Bit(6)
    conceal = _Bit(7)
    strike = _Bit(8)

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
        if self.conceal is not None:
            append("conceal" if self.conceal else "not conceal")
        if self.strike is not None:
            append("strike" if self.strike else "not strike")
        if self._color is not None:
            append(self._color.name)
        if self._bgcolor is not None:
            append("on")
            append(self._bgcolor.name)
        return " ".join(attributes) or "none"

    def __repr__(self):
        """Render a named style differently from an anonymous style."""
        return f'<style "{self}">'

    def __eq__(self, other) -> bool:
        if not isinstance(other, Style):
            return NotImplemented
        return (
            self._color == other._color
            and self._bgcolor == other._bgcolor
            and self._set_attributes == other._set_attributes
            and self._attributes == other._attributes
        )

    @property
    def color(self) -> Optional[Color]:
        """Get the style foreground color or None if it is not set."""
        return self._color

    @property
    def bgcolor(self) -> Optional[Color]:
        """Get the style background color or None if it is not set."""
        return self._bgcolor

    @classmethod
    def reset(cls) -> Style:
        """Get a style to reset all attributes."""
        return Style(
            color="default",
            bgcolor="default",
            dim=False,
            bold=False,
            italic=False,
            underline=False,
            blink=False,
            blink2=False,
            reverse=False,
            conceal=False,
            strike=False,
        )

    @classmethod
    @lru_cache(maxsize=1000)
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
            "conceal",
            "strike",
        }
        color: Optional[str] = None
        bgcolor: Optional[str] = None
        attributes: Dict[str, Optional[bool]] = {}

        words = iter(style_definition.split())
        for original_word in words:
            word = original_word.lower()
            if word == "on":
                word = next(words, "")
                if not word:
                    raise errors.StyleSyntaxError("color expected after 'on'")
                try:
                    Color.parse(word) is None
                except ColorParseError as error:
                    raise errors.StyleSyntaxError(
                        f"unable to parse background color {word} in style {style_definition!r}; {error}"
                    )
                bgcolor = word

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
                try:
                    Color.parse(word)
                except ColorParseError as error:
                    raise errors.StyleSyntaxError(
                        f"unable to parse color {word} in style {style_definition!r}; {error}"
                    )
                color = word
        style = Style(color=color, bgcolor=bgcolor, **attributes)
        return style

    def get_html_style(self, theme: Theme = None) -> str:
        """Get a CSS style rule."""
        theme = theme or themes.DEFAULT
        css: List[str] = []
        append = css.append
        if self.bold:
            append("font-weight: bold")
        if self.italic:
            append("font-style: italic")
        if self.underline:
            append("text-decoration: underline")
        color = self.color
        bgcolor = self.bgcolor
        if self.reverse:
            color, bgcolor = bgcolor, color
        if color is not None:
            theme_color = color.get_truecolor(theme)
            append(f"color: {theme_color.css}")
        if bgcolor is not None:
            theme_color = bgcolor.get_truecolor(theme, foreground=False)
            append(f"background-color: {theme_color.css}")
        return "; ".join(css)

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
        style = self.__new__(Style)
        style._color = self._color
        style._bgcolor = self._bgcolor
        style._attributes = self._attributes
        style._set_attributes = self._attributes
        return style

    def render(
        self,
        text: str = "",
        *,
        color_system: ColorSystem = ColorSystem.TRUECOLOR,
        reset=False,
    ) -> str:
        """Render the ANSI codes to implement the style."""
        attrs: List[str] = []
        if self._color is not None:
            attrs.extend(self._color.downgrade(color_system).get_ansi_codes())

        if self._bgcolor is not None:
            attrs.extend(
                self._bgcolor.downgrade(color_system).get_ansi_codes(foreground=False)
            )

        set_bits = self._set_attributes
        if set_bits:
            append = attrs.append
            bits = self._attributes
            for bit_no in range(0, 9):
                bit = 1 << bit_no
                if set_bits & bit:
                    append(str(1 + bit_no) if bits & bit else str(21 + bit_no))

        reset = "\x1b[0m" if reset else ""
        if attrs:
            return f"\x1b[{';'.join(attrs)}m{text or ''}{reset}"
        else:
            return f"{text or ''}{reset}"

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

        new_style = self.__new__(Style)
        new_style.__dict__ = {
            "_color": style._color or self._color,
            "_bgcolor": style._bgcolor or self._bgcolor,
            "_attributes": (
                (style._attributes & ~self._set_attributes)
                | (self._attributes & self._set_attributes)
            ),
            "_set_attributes": self._set_attributes | style._set_attributes,
        }
        return new_style


class StyleStack:
    """A stack of styles that maintains a current style."""

    def __init__(self, default_style: Style) -> None:
        self._stack: List[Style] = [default_style]
        self.current = default_style

    def __repr__(self) -> str:
        return f"<stylestack {self._stack!r}>"

    def push(self, style: Style) -> None:
        """Push a new style on to the stack.
        
        Args:
            style (Style): New style to combine with current style.
        """
        self.current = self.current.apply(style)
        self._stack.append(self.current)

    def pop(self) -> Style:
        """Pop last style and discard.
        
        Returns:
            Style: New current style (also available as stack.current)
        """
        self._stack.pop()
        self.current = self._stack[-1]
        return self.current


RESET_STYLE = Style.reset()

if __name__ == "__main__":
    import sys

    # style = Style(color="blue", bold=True, italic=True, reverse=False, dim=True)

    from .console import Console

    c = Console()
    style = Style.parse("bold not italic  #6ab825")
    print(bin(style._attributes), bin(style._set_attributes))

    print(repr(style.bold))
    print(repr(style.italic))
    print(style.render("hello", reset=True))

    c.print("hello", style=style)

    print(Style.parse("dim cyan").render("COLOR", reset=True))
    print(Style.parse("dim cyan+").render("COLOR", reset=True))

    print(Style.parse("cyan").render("COLOR", reset=True))
    print(Style.parse("cyan+").render("COLOR", reset=True))

    print(Style.parse("bold blue on magenta+ red").render("COLOR", reset=True))

    print(Style.parse("bold blue on magenta+ red").get_html_style())

    # style.italic = True
    # print(style._attributes, style._set_attributes)
    # print(style.italic)
    # print(style.bold)

    # # style = Style.parse("bold")
    # # print(style)
    # # print(repr(style))

    # # style.test()

    # style = Style.parse("bold on black")
    # print(style.bold)
    # print(style)
    # print(repr(style))

