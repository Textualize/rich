import builtins
import os
import sys
from array import array
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
)

from rich.highlighter import ReprHighlighter

from ._loop import loop_last
from ._pick import pick_bool
from .cells import cell_len
from .highlighter import ReprHighlighter
from .measure import Measurement
from .text import Text

if TYPE_CHECKING:
    from .console import (
        Console,
        ConsoleOptions,
        HighlighterType,
        JustifyMethod,
        OverflowMethod,
        RenderResult,
    )


def install(
    console: "Console" = None,
    overflow: "OverflowMethod" = "ignore",
    crop: bool = False,
) -> None:
    """Install automatic pretty printing in the Python REPL.

    Args:
        console (Console, optional): Console instance or ``None`` to use global console. Defaults to None.
        overflow (Optional[OverflowMethod], optional): Overflow method. Defaults to "ignore".
        crop (Optional[bool], optional): Enable cropping of long lines. Defaults to False.
    """
    from rich import get_console

    console = console or get_console()

    def display_hook(value: Any) -> None:
        """Replacement sys.displayhook which prettifies objects with Rich."""
        if value is not None:
            assert console is not None
            builtins._ = None  # type: ignore
            console.print(
                value
                if hasattr(value, "__rich_console__") or hasattr(value, "__rich__")
                else Pretty(value, overflow=overflow),
                crop=crop,
            )
            builtins._ = value  # type: ignore

    sys.displayhook = display_hook


class Pretty:
    """A rich renderable that pretty prints an object.

    Args:
        _object (Any): An object to pretty print.
        highlighter (HighlighterType, optional): Highlighter object to apply to result, or None for ReprHighlighter. Defaults to None.
        indent_size (int, optional): Number of spaces in indent. Defaults to 4.
        justify (JustifyMethod, optional): Justify method, or None for default. Defaults to None.
        overflow (OverflowMethod, optional): Overflow method, or None for default. Defaults to None.
        no_wrap (Optional[bool], optional): Disable word wrapping. Defaults to False.
    """

    def __init__(
        self,
        _object: Any,
        highlighter: "HighlighterType" = None,
        *,
        indent_size: int = 4,
        justify: "JustifyMethod" = None,
        overflow: Optional["OverflowMethod"] = "crop",
        no_wrap: Optional[bool] = False,
    ) -> None:
        self._object = _object
        self.highlighter = highlighter or ReprHighlighter()
        self.indent_size = indent_size
        self.justify = justify
        self.overflow = overflow
        self.no_wrap = no_wrap

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":
        pretty_str = pretty_repr(
            self._object, max_width=options.max_width, indent_size=self.indent_size
        )
        pretty_text = Text(
            pretty_str,
            justify=self.justify or options.justify,
            overflow=self.overflow or options.overflow,
            no_wrap=pick_bool(self.no_wrap, options.no_wrap),
        )
        pretty_text = self.highlighter(pretty_text)
        yield pretty_text

    def __rich_measure__(self, console: "Console", max_width: int) -> "Measurement":
        pretty_str = pretty_repr(
            self._object, max_width=max_width, indent_size=self.indent_size
        )
        text_width = max(cell_len(line) for line in pretty_str.splitlines())
        return Measurement(text_width, text_width)


def _get_braces_for_defaultdict(_object: defaultdict) -> Tuple[str, str, str]:
    return (
        f"defaultdict({_object.default_factory!r}, {{",
        "})",
        f"defaultdict({_object.default_factory!r}, {{}})",
    )


def _get_braces_for_array(_object: array) -> Tuple[str, str, str]:
    return (f"array({_object.typecode!r}, [", "])", "array({_object.typecode!r})")


_BRACES: Dict[type, Callable[[Any], Tuple[str, str, str]]] = {
    os._Environ: lambda _object: ("environ({", "})", "environ({})"),
    array: _get_braces_for_array,
    defaultdict: _get_braces_for_defaultdict,
    Counter: lambda _object: ("Counter({", "})", "Counter()"),
    deque: lambda _object: ("deque([", "])", "deque()"),
    dict: lambda _object: ("{", "}", "{}"),
    frozenset: lambda _object: ("frozenset({", "})", "frozenset()"),
    list: lambda _object: ("[", "]", "[]"),
    set: lambda _object: ("{", "}", "set()"),
    tuple: lambda _object: ("(", ")", "tuple()"),
}
_CONTAINERS = tuple(_BRACES.keys())
_MAPPING_CONTAINERS = (dict, os._Environ)


@dataclass
class _Node:
    """A node in a repr tree. May be atomic or a container."""

    key_repr: str = ""
    value_repr: str = ""
    open_brace: str = ""
    close_brace: str = ""
    empty: str = ""
    last: bool = False
    is_tuple: bool = False
    children: Optional[List["_Node"]] = None

    def iter_tokens(self) -> Iterable[str]:
        """Generate tokens for this node."""
        if self.key_repr:
            yield self.key_repr
            yield ": "
        if self.value_repr:
            yield self.value_repr
        elif self.children is not None:
            if self.children:
                yield self.open_brace
                if self.is_tuple and len(self.children) == 1:
                    yield from self.children[0].iter_tokens()
                    yield ","
                else:
                    for child in self.children:
                        yield from child.iter_tokens()
                        if not child.last:
                            yield ", "
                yield self.close_brace
            else:
                yield self.empty

    def check_length(self, start_length: int, max_length: int) -> bool:
        """Check the length fits within a limit.

        Args:
            start_length (int): Starting length of the line (indent, prefix, suffix).
            max_length (int): Maximum length.

        Returns:
            bool: True if the node can be rendered within max length, otherwise False.
        """
        total_length = start_length
        for token in self.iter_tokens():
            total_length += cell_len(token)
            if total_length > max_length:
                return False
        return True

    def __str__(self) -> str:
        repr_text = "".join(self.iter_tokens())
        return repr_text


@dataclass
class _Line:
    """A line in repr output."""

    node: Optional[_Node] = None
    text: str = ""
    suffix: str = ""
    whitespace: str = ""
    expanded: bool = False

    @property
    def expandable(self) -> bool:
        """Check if the line may be expanded."""
        return bool(self.node is not None and self.node.children)

    def check_length(self, max_length: int) -> bool:
        """Check this line fits within a given number of cells."""
        start_length = (
            len(self.whitespace) + cell_len(self.text) + cell_len(self.suffix)
        )
        assert self.node is not None
        return self.node.check_length(start_length, max_length)

    def expand(self, indent_size: int) -> Iterable["_Line"]:
        """Expand this line by adding children on their own line."""
        node = self.node
        assert node is not None
        whitespace = self.whitespace
        assert node.children
        if node.key_repr:
            yield _Line(
                text=f"{node.key_repr}: {node.open_brace}", whitespace=whitespace
            )
        else:
            yield _Line(text=node.open_brace, whitespace=whitespace)
        child_whitespace = self.whitespace + " " * indent_size
        for child in node.children:
            line = _Line(
                node=child,
                whitespace=child_whitespace,
                suffix="" if child.last else ",",
            )
            yield line

        yield _Line(
            text=node.close_brace,
            whitespace=whitespace,
            suffix="" if node.last else ",",
        )

    def __str__(self) -> str:
        return f"{self.whitespace}{self.text}{self.node or ''}{self.suffix}"


def pretty_repr(
    _object: Any, *, max_width: int = 80, indent_size: int = 4, expand_all: bool = False
) -> str:
    """Prettify repr string by expanding on to new lines to fit within a given width.

    Args:
        _object (Any): Object to repr.
        max_width (int, optional): Diresired maximum width of repr string. Defaults to 80.
        indent_size (int, optional): Number of spaces to indent. Defaults to 4.
        expand_all (bool, optional): Expand all containers regardless of available width. Defaults to False.

    Returns:
        str: A possibly multi-line representation of the object.
    """

    def to_repr(obj: Any) -> str:
        """Get repr string for an object, but catch errors."""
        try:
            obj_repr = repr(obj)
        except Exception as error:
            obj_repr = f"<repr-error '{error}'>"
        return obj_repr

    visited_ids: Set[int] = set()
    push_visited = visited_ids.add
    pop_visited = visited_ids.remove

    def traverse(obj: Any, root: bool = False) -> _Node:
        """Walk the object depth first."""
        obj_type = type(obj)
        if obj_type in _CONTAINERS:
            obj_id = id(obj)

            if obj_id in visited_ids:
                # Recursion detected
                return _Node(value_repr="...")
            push_visited(obj_id)
            open_brace, close_brace, empty = _BRACES[obj_type](obj)

            if obj:
                children: List[_Node] = []
                node = _Node(
                    open_brace=open_brace,
                    close_brace=close_brace,
                    children=children,
                    last=root,
                )
                append = children.append
                if isinstance(obj, _MAPPING_CONTAINERS):
                    for last, (key, child) in loop_last(obj.items()):
                        child_node = traverse(child)
                        child_node.key_repr = to_repr(key)
                        child_node.last = last
                        append(child_node)
                else:
                    for last, child in loop_last(obj):
                        child_node = traverse(child)
                        child_node.last = last
                        append(child_node)
            else:
                node = _Node(empty=empty, children=[], last=root)

            pop_visited(obj_id)
        else:
            node = _Node(value_repr=to_repr(obj), last=root)
        node.is_tuple = isinstance(obj, tuple)
        return node

    node = traverse(_object, root=True)

    lines = [_Line(node=node)]
    line_no = 0
    while line_no < len(lines):
        line = lines[line_no]
        if line.expandable and not line.expanded:
            if expand_all or not line.check_length(max_width):
                lines[line_no : line_no + 1] = line.expand(indent_size)
        line_no += 1

    repr_str = "\n".join(str(line) for line in lines)
    return repr_str


if __name__ == "__main__":  # pragma: no cover

    class BrokenRepr:
        def __repr__(self):
            1 / 0

    d = defaultdict(int)
    d["foo"] = 5
    data = {
        "foo": [
            1,
            "Hello World!",
            100.123,
            323.232,
            432324.0,
            {5, 6, 7, (1, 2, 3, 4), 8},
        ],
        "bar": frozenset({1, 2, 3}),
        "defaultdict": defaultdict(
            list, {"crumble": ["apple", "rhubarb", "butter", "sugar", "flour"]}
        ),
        "counter": Counter(
            [
                "apple",
                "orange",
                "pear",
                "kumquat",
                "kumquat",
                "durian",
            ]
        ),
        "atomic": (False, True, None),
        "Broken": BrokenRepr(),
    }
    data["foo"].append(data)  # type: ignore

    from rich import print

    print(Pretty(data))
