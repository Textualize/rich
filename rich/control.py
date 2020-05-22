from typing import NamedTuple, TYPE_CHECKING

from .segment import Segment

if TYPE_CHECKING:
    from .console import Console, ConsoleOptions, RenderResult

STRIP_CONTROL_CODES = [
    8,  # Backspace
    11,  # Vertical tab
    12,  # Form feed
    13,  # Carriage return
]
_CONTROL_TRANSLATE = {_codepoint: None for _codepoint in STRIP_CONTROL_CODES}


class Control:
    """A renderable that inserts a control code (non printable but may move cursor).

    Args:
        control_codes (str): A string containing control codes.
    """

    __slots__ = ["_control_codes"]

    def __init__(self, control_codes: str) -> None:
        self._control_codes = Segment.control(control_codes)

    def __str__(self) -> str:
        return self._control_codes.text

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":
        yield self._control_codes


def strip_control_codes(text: str, _translate_table=_CONTROL_TRANSLATE) -> str:
    """Remove control codes from text.

    Args:
        text (str): A string possibly contain control codes.        

    Returns:
        str: String with control codes removed.
    """
    return text.translate(_translate_table)


if __name__ == "__main__":  # pragma: no cover

    print(strip_control_codes("hello\rWorld"))
