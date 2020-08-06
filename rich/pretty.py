from dataclasses import dataclass

from typing import Any, Iterable, List, Optional, Tuple, TYPE_CHECKING

from pprintpp import pformat

from ._loop import loop_last
from .measure import Measurement
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
        # TODO: pformat tends to render a smaller width than it needs to, investigate why
        print(options)
        _min, max_width = Measurement.get(console, self, options.max_width)
        pretty_str = pformat(self._object, width=max_width)
        pretty_str = pretty_str.replace("\r", "")
        pretty_text = self.highlighter(pretty_str)
        yield pretty_text

    def __rich_measure__(self, console: "Console", max_width: int) -> "Measurement":
        pretty_str = pformat(self._object, width=max_width)
        pretty_str = pretty_str.replace("\r", "")
        text = Text(pretty_str)
        measurement = Measurement.get(console, text, max_width)
        print(measurement)
        return measurement


@dataclass
class _Node:
    indent: int = -1
    object_repr: Optional[str] = None
    name: str = ""
    braces: Optional[Tuple[str, str]] = None
    values: Optional[List["_Node"]] = None
    items: Optional[List[Tuple[str, "_Node"]]] = None
    expanded: bool = False


_BRACES = {
    list: ("", "[", "]"),
    tuple: ("", "(", ")"),
    set: ("", "{", "}"),
    frozenset: ("frozenset", "({", "})"),
}


@dataclass
class _Value:
    object_repr: str


@dataclass
class _Container:
    braces: Tuple[str]


def pretty_repr(_object: Any, *, width: int = 80, indent_size: int = 4) -> str:

    indent = " " * indent_size

    stack = []
    push = stack.append

    node = _object

    if isinstance(node, (tuple, list, set, dict)):
        braces = _BRACES[type(node)]
        push(_Container())

    def add_node(parent_node: _Node, node_object: Any) -> _Node:
        if isinstance(node_object, (list, set, frozenset, tuple)):
            name, open_brace, close_brace = _BRACES[type(node_object)]
            node = _Node(
                indent=parent_node.indent + 1, braces=(open_brace, close_brace)
            )
            node.values = [add_node(node, child) for child in node_object]
        elif isinstance(node_object, dict):
            node = _Node(indent=parent_node.indent + 1, braces=("{", "}"))
            node.items = [
                (key, add_node(node, value)) for key, value in node_object.items()
            ]
        else:
            node = _Node(indent=parent_node.indent + 1, object_repr=repr(node_object))
        return node

    node = add_node(_Node(), _object)
    print(node)
    node.expanded = True

    output = []

    return ""


if __name__ == "__main__":
    data = {"d": [1, "Hello World!", 2, 3, 4, {5, 6, 7, (1, 2, 3, 4), 8}]}
    from rich import print

    print(pretty_repr(data))

