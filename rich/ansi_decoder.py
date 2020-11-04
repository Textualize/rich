import re
from typing import Iterable, NamedTuple

from .color import Color
from .style import Style
from .text import Text

re_ansi = re.compile(r"(?:\x1b\[(.*?)m)|(?:\x1b\](.*?)\x1b\\)")
re_csi = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


class AnsiToken(NamedTuple):
    """Result of ansi tokenized string."""

    plain: str = ""
    sgr: str = ""
    osc: str = ""


def _ansi_tokenize(ansi_text: str) -> Iterable[AnsiToken]:
    """Tokenize a string in to plain text and ANSI codes.

    Args:
        ansi_text (str): A String containing ANSI codes.

    Yields:
        Tuple[Optional[str], Optional[str]]: A tuple of plain text, ansi codes.
    """

    def remove_csi(ansi_text: str) -> str:
        return re_csi.sub("", ansi_text)

    position = 0
    for match in re_ansi.finditer(ansi_text):
        start, end = match.span(0)
        sgr, osc = match.groups()
        if start > position:
            yield AnsiToken(remove_csi(ansi_text[position:start]))
        yield AnsiToken("", sgr, osc)
        position = end
    if position < len(ansi_text):
        yield AnsiToken(remove_csi(ansi_text[position:]))


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
        for token in _ansi_tokenize(line):
            plain_text, sgr, osc = token
            if plain_text:
                append(plain_text, self.style or None)
            elif osc:
                if not osc.startswith("8;"):
                    continue
                _params, semicolon, link = osc[2:].partition(";")
                if semicolon:
                    self.style = self.style.update_link(link)
            elif sgr:
                # Translate in to semi-colon separated codes
                # Ignore invalid codes, because we want to be lenient
                codes = [int(_code) for _code in sgr.split(";") if _code.isdigit()]
                # codes = [code for code in codes if code <= 255]
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
                    elif 99 > code >= 90:
                        self.style += _Style(color=_Color.from_ansi(code - 90 + 8))
                    elif 108 > code >= 100:
                        self.style += _Style(bgcolor=_Color.from_ansi(code - 100 + 8))
                    elif code in (38, 48):
                        try:
                            color_type = next(iter_codes)
                            if color_type == 5:
                                number = next(iter_codes)
                                color = _Color.from_ansi(number)
                                self.style += (
                                    _Style(color=color)
                                    if code == 38
                                    else _Style(bgcolor=color)
                                )
                            elif color_type == 2:
                                color = _Color.from_rgb(
                                    next(iter_codes), next(iter_codes), next(iter_codes)
                                )
                                self.style += (
                                    _Style(color=color)
                                    if code == 38
                                    else _Style(bgcolor=color)
                                )
                        except StopIteration:
                            # Unexpected end of codes
                            break
        return text


# if __name__ == "__main__":  # pragma: no cover
#     from .console import Console
#     from .text import Text

#     console = Console()
#     console.begin_capture()
#     console.print(
#         "[bold magenta]bold magenta [i]italic[/i][/] [link http://example.org]Hello World[/] not linked"
#     )
#     ansi = console.end_capture()

#     print(ansi)

#     ansi_decoder = AnsiDecoder()
#     for line in ansi_decoder.decode(ansi):
#         print("*", repr(line))
#         print(line)
#         console.print(line)

if __name__ == "__main__":  # pragma: no cover
    import pty
    import io
    import os
    import sys

    decoder = AnsiDecoder()

    stdout = io.BytesIO()

    def read(fd):
        data = os.read(fd, 1024)
        stdout.write(data)
        return data

    pty.spawn(sys.argv[1:], read)

    from .console import Console

    console = Console(record=True)

    stdout_result = stdout.getvalue().decode("utf-8")
    print(stdout_result)

    for line in decoder.decode(stdout_result):
        console.print(line)

    console.save_html("stdout.html")
