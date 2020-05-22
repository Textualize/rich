from typing import Any, TYPE_CHECKING

from pprintpp import pformat

from .measure import Measurement
from .highlighter import ReprHighlighter
from .text import Text

if TYPE_CHECKING:  # pragma: no cover
    from .console import Console, ConsoleOptions, HighlighterType, RenderResult


class Pretty:
    def __init__(self, _object: Any, highlighter: "HighlighterType" = None) -> None:
        self._object = _object
        self.highlighter = highlighter or Text

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":
        pretty_str = pformat(self._object, width=options.max_width)
        pretty_str = pretty_str.replace("\r", "")
        pretty_text = self.highlighter(pretty_str)
        yield pretty_text

    def __rich_measure__(self, console: "Console", max_width: int) -> "Measurement":
        text = Text(pformat(self._object, width=max_width))
        return Measurement.get(console, text, max_width)
