from typing import Any, TYPE_CHECKING

from pprintpp import pformat

from ._render_width import RenderWidth
from .highlighter import ReprHighlighter
from .text import Text

if TYPE_CHECKING:
    from .console import Console, ConsoleOptions, RenderResult


class Pretty:
    def __init__(self, _object: Any) -> None:
        self._object = _object

    def __console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":
        highlighter = ReprHighlighter()
        pretty_str = pformat(self._object, width=options.max_width)
        pretty_text = highlighter(pretty_str)
        yield pretty_text

    def __console_width__(self, max_width: int) -> "RenderWidth":
        text = Text(pformat(self._object, width=max_width))
        return text.__console_width__(max_width)
