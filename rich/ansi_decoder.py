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


class AnsiDecoder:
    """Translate ANSI code in to styled Text."""

    def __init__(self):
        self.style = Style()

    def decode(self, lines: Iterable[str]) -> Iterable[Text]:

        for line in lines:
            text = Text()
            append = text.append
            for plain_text, ansi_codes in ansi_tokenize(line):
                print(repr(plain_text), repr(ansi_codes))
                if plain_text is not None:
                    append(plain_text, self.style or None)
                elif ansi_codes is not None and ansi_codes.startswith("["):
                    codes = ansi_codes[1:].split(";")
                    iter_codes = iter(codes)
                    while True:
                        try:
                            code = int(next(iter_codes))
                        except StopIteration:
                            break

                        if code == 0:
                            self.style = Style()
                        elif code == 39:
                            self.style += Style(color="default")
                        elif code == 49:
                            self.style += Style(bgcolor="default")
                        elif 38 > code >= 30:
                            self.style += Style(color=Color.from_ansi(code - 30))
                        elif 48 > code >= 40:
                            self.style += Style(bgcolor=Color.from_ansi(code - 40))
                        elif code in (38, 48):
                            color_type = next(iter_codes)
                            if color_type == "5":
                                code = next(iter_codes)
                                number = int(code)
                                if code == 38:
                                    self.style += Style(color=Color.from_ansi(number))
                                else:
                                    self.style += Style(bgcolor=Color.from_ansi(number))
                            elif color_type == "2":
                                red, green, blue = (
                                    int(_code)
                                    for _code in (
                                        next(iter_codes),
                                        next(iter_codes),
                                        next(iter_codes),
                                    )
                                )
                                if code == 38:
                                    self.style = Style(
                                        color=Color.from_rgb(red, green, blue)
                                    )
                                else:
                                    self.style = Style(
                                        bgcolor=Color.from_rgb(red, green, blue)
                                    )
            yield text


if __name__ == "__main__":
    from .console import Console
    from .text import Text

    console = Console()
    console.begin_capture()
    console.print("Hello [bold Magenta]World[/]!")
    ansi = console.end_capture()

    print(ansi)

    ansi_decoder = AnsiDecoder()
    for line in ansi_decoder.decode(ansi.splitlines()):
        print("*", repr(line))
        print(line)
        console.print(line)