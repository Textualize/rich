from __future__ import annotations

from typing import Any, TYPE_CHECKING

from pprintpp import pformat


from .highlighter import ReprHighlighter

if TYPE_CHECKING:
    from .console import Console, ConsoleOptions, RenderResult


class Pretty:
    def __init__(self, _object: Any) -> None:
        self._object = _object

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        highlighter = ReprHighlighter()
        pretty_str = pformat(self._object, width=options.max_width)
        pretty_text = highlighter(pretty_str)
        yield pretty_text
