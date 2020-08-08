import sys

from collections import defaultdict
from dataclasses import dataclass, field
from rich.highlighter import ReprHighlighter

from typing import Any, Dict, List, Optional, Set, Tuple, TYPE_CHECKING

from .cells import cell_len
from .highlighter import Highlighter, NullHighlighter, ReprHighlighter
from ._loop import loop_last
from .measure import Measurement
from ._pick import pick_bool
from .text import Text

if TYPE_CHECKING:  # pragma: no cover
    from .console import (
        Console,
        ConsoleOptions,
        HighlighterType,
        OverflowMethod,
        RenderResult,
    )


def install(console: "Console" = None) -> None:
    """Install automatic pretty printing in the Python REPL.

    Args:
        console (Console, optional): Console instance or ``None`` to use global console. Defaults to None.
    """
    from rich import get_console

    console = console or get_console()

    def display_hook(value: Any) -> None:
        if value is not None:
            assert console is not None
            console.print(
                value
                if hasattr(value, "__rich_console__") or hasattr(value, "__rich__")
                else pretty_repr(value, no_wrap=True, overflow="ellipsis")
            )

    sys.displayhook = display_hook


class Pretty:
    """A rich renderable that pretty prints an object."""

    def __init__(
        self,
        _object: Any,
        highlighter: "HighlighterType" = None,
        *,
        indent_size: int = 4,
        overflow: "OverflowMethod" = None,
        no_wrap: bool = None,
    ) -> None:
        self._object = _object
        self.highlighter = highlighter or NullHighlighter()
        self.indent_size = indent_size
        self.overflow = overflow
        self.no_wrap = no_wrap

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":
        pretty_text = pretty_repr(
            self._object,
            max_width=options.max_width,
            indent_size=self.indent_size,
            overflow=self.overflow or options.overflow,
            no_wrap=pick_bool(self.no_wrap, options.no_wrap, True),
        )
        yield pretty_text

    def __rich_measure__(self, console: "Console", max_width: int) -> "Measurement":
        pretty_text = pretty_repr(
            self._object, max_width=max_width, indent_size=self.indent_size
        )
        text_width = max(cell_len(line) for line in pretty_text.plain.splitlines())
        return Measurement(text_width, text_width)


_BRACES: Dict[type, Tuple[Text, Text, Text]] = {
    dict: (Text("{", "repr.brace"), Text("}", "repr.brace"), Text("{}", "repr.brace")),
    frozenset: (
        Text.assemble("frozenset(", ("{", "repr.brace")),
        Text.assemble(("}", "repr.brace"), ")"),
        Text("frozenset()"),
    ),
    list: (Text("[", "repr.brace"), Text("]", "repr.brace"), Text("[]", "repr.brace")),
    set: (Text("{", "repr.brace"), Text("}", "repr.brace"), Text("set()")),
    tuple: (Text("(", "repr.brace"), Text(")", "repr.brace"), Text("()", "repr.brace")),
}
_CONTAINERS = tuple(_BRACES.keys())
_REPR_STYLES = {
    type(None): "repr.none",
    str: "repr.str",
    float: "repr.number",
    int: "repr.number",
}


@dataclass
class _Line:
    """A line in a pretty repr."""

    parts: List[Text] = field(default_factory=list)
    _cell_len: int = 0

    def append(self, text: Text) -> None:
        """Add text to line."""
        # Efficiently keep track of cell length
        self.parts.append(text)
        self._cell_len += text.cell_len

    @property
    def cell_len(self) -> int:
        return (
            self._cell_len
            if self.parts and not self.parts[-1].plain.endswith(" ")
            else self._cell_len - 1
        )

    @property
    def text(self):
        """The text as a while."""
        return Text("").join(self.parts)


def pretty_repr(
    _object: Any,
    *,
    max_width: Optional[int] = 80,
    indent_size: int = 4,
    highlighter: Highlighter = None,
    overflow: "OverflowMethod" = None,
    no_wrap: bool = True,
) -> Text:
    """Return a 'pretty' repr.

    Args:
        _object (Any): Object to repr.
        max_width (int, optional): Maximum desired width. Defaults to 80.
        indent_size (int, optional): Number of spaces in an indent. Defaults to 4.
        highlighter (Highlighter, optional): A highlighter for repr strings. Defaults to ReprHighlighter.

    Returns:
        Text: A Text instance conaining a pretty repr.
    """

    class MaxLineReached(Exception):
        """Line is greater than maximum"""

        def __init__(self, line_no: int) -> None:
            self.line_no = line_no
            super().__init__()

    if highlighter is None:
        highlighter = ReprHighlighter()

    indent = " " * indent_size
    expand_level = 0
    lines: List[_Line] = [_Line()]

    visited_set: Set[int] = set()
    repr_cache: Dict[int, Text] = {}
    repr_cache_get = repr_cache.get

    def to_repr_text(node: Any) -> Text:
        """Convert object to repr."""
        node_id = id(node)
        cached = repr_cache_get(node_id)
        if cached is not None:
            return cached
        style: Optional[str]
        if node is True:
            style = "repr.bool_true"
        elif node is False:
            style = "repr.bool_false"
        else:
            style = _REPR_STYLES.get(type(node))
        try:
            repr_text = repr(node)
        except Exception as error:
            text = Text(f"<error in repr: {error}>", "repr.error")
        else:
            if style is None and highlighter is not None:
                text = highlighter(Text(repr_text))
            else:
                text = Text(repr_text, style or "")
        repr_cache[node_id] = text
        return text

    comma = Text(", ")
    colon = Text(": ")
    line_break: Optional[int] = None

    def traverse(node: Any, level: int = 0) -> None:
        """Walk the data structure."""
        nonlocal line_break
        append_line = lines.append

        def append_text(text: Text) -> None:
            nonlocal line_break
            line = lines[-1]
            line.append(text)
            if max_width is not None and line.cell_len > max_width:
                if line_break is not None and len(lines) <= line_break:
                    return
                line_break = len(lines)
                raise MaxLineReached(level)

        node_id = id(node)
        if node_id in visited_set:
            # Recursion detected
            append_text(Text("...", "repr.error"))
            return

        visited_set.add(node_id)
        if type(node) in _CONTAINERS:
            brace_open, brace_close, empty = _BRACES[type(node)]
            expanded = level < expand_level

            if not node:
                append_text(empty)
            else:
                append_text(brace_open)
                if isinstance(node, dict):
                    for last, (key, value) in loop_last(node.items()):
                        if expanded:
                            append_line(_Line())
                            append_text(Text(indent * (level + 1)))
                        append_text(to_repr_text(key))
                        append_text(colon)
                        traverse(value, level + 1)
                        if not last:
                            append_text(comma)
                else:
                    for last, value in loop_last(node):
                        if expanded:
                            append_line(_Line())
                            append_text(Text(indent * (level + 1)))
                        traverse(value, level + 1)
                        if not last:
                            append_text(comma)
                if expanded:
                    lines.append(_Line())
                    append_text(Text.assemble(f"{indent * level}", brace_close))
                else:
                    append_text(brace_close)
        else:
            append_text(to_repr_text(node))
        visited_set.remove(node_id)

    # Keep expanding levels until the text fits
    while True:
        try:
            traverse(_object)
        except MaxLineReached as max_line:
            del lines[:]
            visited_set.clear()
            lines.append(_Line())
            expand_level += 1
        else:
            break  # pragma: no cover

    text = Text("\n", overflow=overflow, no_wrap=no_wrap).join(
        line.text for line in lines
    )
    return text


if __name__ == "__main__":  # pragma: no cover
    from collections import defaultdict

    class BrokenRepr:
        def __repr__(self):
            1 / 0

    d = defaultdict(int)
    d["foo"] = 5
    data = {
        "foo": [1, "Hello World!", 2, 3, 4, {5, 6, 7, (1, 2, 3, 4), 8}],
        "bar": frozenset({1, 2, 3}),
        False: "This is false",
        True: "This is true",
        None: "This is None",
        "Broken": BrokenRepr(),
    }
    data["foo"].append(data)  # type: ignore

    from rich.console import Console

    console = Console()
    from rich import print

    p = Pretty(data, overflow="ellipsis")
    print(Measurement.get(console, p))
    console.print(p)
