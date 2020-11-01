import re
from typing import Iterable, Optional, Tuple

from .color import Color
from .style import Style
from .text import Text

re_ansi = re.compile("\x1b(.*?)m")


def ansi_tokenize(ansi_text: str) -> Iterable[Tuple[Optional[str], Optional[str]]]:
    """Tokenize a string in to plain text and ANSI codes.

    Args:
        ansi_text (str): A String containing ANSI codes.

    Yields:
        Tuple[Optional[str], Optional[str]]: A tuple of plain text, ansi codes.
    """
    position = 0
    for match in re_ansi.finditer(ansi_text):
        start, end = match.span(0)
        ansi_code = match.group(1)
        if start > position:
            yield ansi_text[position:start], None
        yield None, ansi_code
        position = end
    if position < len(ansi_text):
        yield ansi_text[position:], None


STYLE_MAP = {
    1: "bold",
    21: "not bold",
    2: "dim",
    22: "not dim",
    3: "italic",
    23: "not italic",
    4: "underline",
    24: "not underline",
    5: "blink",
    25: "not blink",
    6: "blink2",
    26: "not blink2",
    7: "reverse",
    27: "not reverse",
    8: "conceal",
    28: "not conceal",
    9: "strike",
    29: "not strike",
    21: "underline2",
    51: "frame",
    54: "not frame not encircle",
    52: "encircle",
    53: "overline",
    55: "not overline",
}
SGR_CODES = set(STYLE_MAP.keys())


class AnsiDecoder:
    """Translate ANSI code in to styled Text."""

    def __init__(self):
        self.style = Style()

    def decode(self, terminal_text: str) -> Iterable[Text]:
        """Decode ANSI codes in an interable of lines.

        Args:
            lines (Iterable[str]): An iterable of lines of terminal output.


        Yields:
            Text: Marked up Text.
        """
        for line in terminal_text.splitlines():
            yield self.decode_line(line)

    def decode_line(self, line: str) -> Text:
        """Decode a line containing ansi codes.

        Args:
            line (str): A line of terminal output.

        Returns:
            Text: A Text instance marked up according to ansi codes.
        """
        _Color = Color
        _Style = Style
        text = Text()
        append = text.append
        for plain_text, ansi_codes in ansi_tokenize(line):
            if plain_text is not None:
                append(plain_text, self.style or None)
            elif ansi_codes is not None and ansi_codes.startswith("["):
                # Translate in to semi-colon separated codes
                # Ignore invalid codes, because we want to be lenient
                codes = [
                    int(_code) for _code in ansi_codes[1:].split(";") if _code.isdigit()
                ]
                codes = [code for code in codes if code <= 255]
                iter_codes = iter(codes)
                for code in iter_codes:
                    if code == 0:
                        self.style = _Style()
                    elif code in SGR_CODES:
                        self.style += _Style.parse(STYLE_MAP[code])
                    elif code == 39:
                        self.style += _Style(color="default")
                    elif code == 49:
                        self.style += _Style(bgcolor="default")
                    elif 38 > code >= 30:
                        self.style += _Style(color=_Color.from_ansi(code - 30))
                    elif 48 > code >= 40:
                        self.style += _Style(bgcolor=_Color.from_ansi(code - 40))
                    elif code in (38, 48):
                        try:
                            color_type = next(iter_codes)
                            if color_type == "5":
                                number = next(iter_codes)
                                color = _Color.from_ansi(number)
                                self.style += (
                                    _Style(color=color)
                                    if code == 38
                                    else _Style(bgcolor=color)
                                )
                            elif color_type == "2":
                                color = _Color.from_rgb(
                                    next(iter_codes), next(iter_codes), next(iter_codes)
                                )
                                self.style = (
                                    _Style(color=color)
                                    if code == 38
                                    else _Style(bgcolor=color)
                                )
                        except StopIteration:
                            # Unexpected end of codes
                            break
        return text


if __name__ == "__main__":  # pragma: no cover
    from .console import Console
    from .text import Text

    console = Console()
    console.begin_capture()
    console.print(
        "[u]H[s]ell[/s]o[/u] [bold Magenta][blink]World[/][/]!\n[reverse]Reverse"
    )
    ansi = console.end_capture()

    print(ansi)

    ansi_decoder = AnsiDecoder()
    for line in ansi_decoder.decode(ansi):
        print("*", repr(line))
        print(line)
        console.print(line)