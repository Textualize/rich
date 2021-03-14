from typing import Callable, Dict, TYPE_CHECKING, Union, Tuple

from .segment import ControlType, Segment

if TYPE_CHECKING:
    from .console import Console, ConsoleOptions, RenderResult

STRIP_CONTROL_CODES = [
    8,  # Backspace
    11,  # Vertical tab
    12,  # Form feed
    13,  # Carriage return
]
_CONTROL_TRANSLATE = {_codepoint: None for _codepoint in STRIP_CONTROL_CODES}


CONTROL_CODES_FORMAT: Dict[ControlType, Callable[[int], str]] = {
    ControlType.BELL: lambda _: "\x07",
    ControlType.CARRIAGE_RETURN: lambda _: "\r",
    ControlType.HOME: lambda _: "\x1b[H",
    ControlType.CLEAR: lambda _: "\x1b[2J",
    ControlType.ENABLE_ALT_SCREEN: lambda _: "\x1b[?1049h",
    ControlType.DISABLE_ALT_SCREEN: lambda _: "\x1b[?1049l",
    ControlType.SHOW_CURSOR: lambda _: "\x1b[?25h",
    ControlType.HIDE_CURSOR: lambda _: "\x1b[?25l",
    ControlType.CURSOR_UP: lambda param: f"\x1b[{param}A",
    ControlType.CURSOR_DOWN: lambda param: f"\x1b[{param}B",
    ControlType.CURSOR_FORWARD: lambda param: f"\x1b[{param}C",
    ControlType.CURSOR_BACKWARD: lambda param: f"\x1b[{param}D",
    ControlType.ERASE_IN_LINE: lambda param: f"\x1b[{param}K",
}


class Control:
    """A renderable that inserts a control code (non printable but may move cursor).

    Args:
        *codes (str): Positional arguments are either a :class:`~rich.segment.ControlType` enum or a
            tuple of ControlType and an integer parameter
    """

    __slots__ = ["_segment"]

    def __init__(self, *codes: Union[ControlType, Tuple[ControlType, int]]) -> None:
        control_codes = [
            code if isinstance(code, tuple) else (code, 0) for code in codes
        ]
        _format_map = CONTROL_CODES_FORMAT
        self._segment = Segment(
            "".join(_format_map[code](param) for code, param in control_codes),
            None,
            control_codes,
        )

    @property
    def segment(self) -> "Segment":
        return self._segment

    @classmethod
    def bell(cls) -> "Control":
        """Ring the 'bell'."""
        return cls(ControlType.BELL)

    @classmethod
    def home(cls) -> "Control":
        """Move cursor to 'home' position."""
        return cls(ControlType.HOME)

    @classmethod
    def clear(cls) -> "Control":
        """Clear the screen."""
        return cls(ControlType.CLEAR)

    @classmethod
    def show_cursor(cls, show: bool) -> "Control":
        """Show or hide the cursor."""
        return cls(ControlType.SHOW_CURSOR if show else ControlType.HIDE_CURSOR)

    @classmethod
    def alt_screen(cls, enable: bool) -> "Control":
        """Enable or disable alt screen."""
        if enable:
            return cls(ControlType.ENABLE_ALT_SCREEN, ControlType.HOME)
        else:
            return cls(ControlType.DISABLE_ALT_SCREEN)

    def __str__(self) -> str:
        return self._segment.text

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":
        yield self._segment


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
