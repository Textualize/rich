from __future__ import annotations

import sys
from typing import Any, Dict, Iterable, List, Mapping, Optional, Type

from . import errors
from .color import Color


class _Bit:
    """A descriptor to get/set a style attribute bit."""

    def __init__(self, bit_no: int) -> None:
        self.bit = 1 << bit_no

    def __get__(self, obj: Style, objtype: Type[Style]) -> Optional[bool]:
        if obj._set_attributes & self.bit:
            return obj._attributes & self.bit != 0
        return None

    def __set__(self, obj: Style, val: Optional[bool]) -> None:
        bit = self.bit
        if val is None:
            obj._set_attributes &= ~bit
            obj._attributes &= ~bit
        else:
            obj._set_attributes |= bit
            if val:
                obj._attributes |= bit
            else:
                obj._attributes &= ~bit


class Style:
    """A terminal style."""

    def __init__(
        self,
        *,
        color: str = None,
        back: str = None,
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
        self._back = None if back is None else Color.parse(back)
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
        if self._back is not None:
            append("on")
            append(self._back.name)
        return " ".join(attributes) or "none"

    def __repr__(self):
        """Render a named style differently from an anonymous style."""
        return f'<style "{self}">'

    def __eq__(self, other) -> bool:
        if not isinstance(other, Style):
            return NotImplemented
        return (
            self._color == other._color
            and self._back == other._back
            and self._set_attributes == other._set_attributes
            and self._attributes == other._attributes,
        )

    @property
    def color(self) -> Optional[str]:
        return self._color.name if self._color is not None else None

    @color.setter
    def color(self, new_color: Optional[str]) -> None:
        self._color = None if new_color is None else Color.parse(new_color)

    @property
    def back(self) -> Optional[str]:
        return self._back.name if self._back is not None else None

    @back.setter
    def back(self, new_color: Optional[str]) -> None:
        self._back = None if new_color is None else Color.parse(new_color)

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
            conceal=False,
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
            "conceal",
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
        style = self.__new__(Style)
        style._color = self.color
        style._back = self.back
        style._attributes = self._attributes
        style._set_attributes = self._attributes
        return style

    def render(self, text: str = "", *, reset=False) -> str:
        """Render the ANSI codes to implement the style."""
        attrs: List[str] = []
        append = attrs.append

        if self._color is not None:
            attrs.extend(self._color.get_ansi_codes())

        if self._back is not None:
            attrs.extend(self._back.get_ansi_codes(foreground=False))

        set_bits = self._set_attributes
        bits = self._attributes
        for bit_no in range(0, 10):
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

        new_style = style.__new__(Style)
        new_style._color = self._color if style._color is None else style._color
        new_style._back = self._back if style._back is None else style._back
        new_style._attributes = (style._attributes & ~self._set_attributes) | (
            self._attributes & self._set_attributes
        )
        new_style._set_attributes = self._set_attributes | style._set_attributes
        return new_style


class StyleStack:
    """A stack of styles that maintains a current style."""

    def __init__(self, default_style: Style) -> None:
        self._stack: List[Style] = []
        self._stack.append(default_style)
        self.current = default_style

    def __repr__(self) -> str:
        return f"<stylestack {self._stack!r}>"

    def push(self, style: Style) -> None:
        self.current = self.current.apply(style)
        self._stack.append(self.current)

    def pop(self) -> Style:
        self._stack.pop()
        self.current = self._stack[-1]
        return self.current


RESET_STYLE = Style.reset()

if __name__ == "__main__":
    import sys

    # style = Style(color="blue", bold=True, italic=True, reverse=False, dim=True)

    style = Style.parse("bold  not italic  #6ab825")
    print(bin(style._attributes), bin(style._set_attributes))

    print(repr(style.bold))
    print(repr(style.italic))
    print(style.render("hello", reset=True))

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

