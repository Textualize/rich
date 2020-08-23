import builtins
import sys

from collections import defaultdict
from dataclasses import dataclass, field
from rich.highlighter import ReprHighlighter

from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, TYPE_CHECKING

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
        overflow (Optional[OverflowMethod], optional): Overflow method. Defaults to None.
        crop (Optional[bool], optional): Enable cropping of long lines. Defaults to False.
    """
    from rich import get_console

    console = console or get_console()

    def display_hook(value: Any) -> None:

        if value is not None:
            assert console is not None
            builtins._ = None  # type: ignore
            console.print(
                value
                if hasattr(value, "__rich_console__") or hasattr(value, "__rich__")
                else pretty_repr(value, max_width=console.width, overflow=overflow),
                crop=crop,
            )
            builtins._ = value  # type: ignore

    sys.displayhook = display_hook


class Pretty:
    """A rich renderable that pretty prints an object."""

    def __init__(
        self,
        _object: Any,
        highlighter: "HighlighterType" = None,
        *,
        indent_size: int = 4,
        justify: "JustifyMethod" = None,
        overflow: "OverflowMethod" = None,
    ) -> None:
        self._object = _object
        self.highlighter = highlighter or NullHighlighter()
        self.indent_size = indent_size
        self.justify = justify
        self.overflow = overflow

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":
        pretty_text = pretty_repr(
            self._object,
            max_width=options.max_width,
            indent_size=self.indent_size,
            justify=self.justify or options.justify,
            overflow=self.overflow or options.overflow,
        )
        yield pretty_text

    def __rich_measure__(self, console: "Console", max_width: int) -> "Measurement":
        pretty_text = pretty_repr(
            self._object, max_width=max_width, indent_size=self.indent_size
        )
        text_width = max(cell_len(line) for line in pretty_text.plain.splitlines())
        return Measurement(text_width, text_width)


_BRACES: Dict[type, Tuple[str, str, str]] = {
    dict: ("{", "}", "{}"),
    frozenset: ("frozenset({", "})", "frozenset()"),
    list: ("[", "]", "[]"),
    set: ("{", "}", "set()"),
    tuple: ("(", ")", "tuple()"),
}
_CONTAINERS = tuple(_BRACES.keys())


# @dataclass
# class _Line:
#     """A line in a pretty repr."""

#     parts: List[str] = field(default_factory=list)
#     _cell_len: int = 0
#     _space: bool = False

#     def append(self, text: str) -> None:
#         """Add text to line."""
#         # Efficiently keep track of cell length
#         self.parts.append(text)
#         self._cell_len += cell_len(text)
#         self._space = text.endswith(" ")

#     @property
#     def cell_len(self) -> int:
#         return self._cell_len - 1 if self._space else self._cell_len

#     @property
#     def text(self) -> str:
#         """The text as a while."""
#         return "".join(self.parts)


# def pretty_repr(
#     _object: Any,
#     *,
#     max_width: Optional[int] = 80,
#     indent_size: int = 4,
#     highlighter: Highlighter = None,
#     justify: "JustifyMethod" = None,
#     overflow: "OverflowMethod" = None,
#     no_wrap: bool = True,
# ) -> Text:
#     """Return a 'pretty' repr.

#     Args:
#         _object (Any): Object to repr.
#         max_width (int, optional): Maximum desired width. Defaults to 80.
#         indent_size (int, optional): Number of spaces in an indent. Defaults to 4.
#         highlighter (Highlighter, optional): A highlighter for repr strings. Defaults to ReprHighlighter.

#     Returns:
#         Text: A Text instance conaining a pretty repr.
#     """

#     class MaxLineReached(Exception):
#         """Line is greater than maximum"""

#     if highlighter is None:
#         highlighter = ReprHighlighter()

#     indent = " " * indent_size
#     expand_level = 0
#     lines: List[_Line] = [_Line()]

#     visited_set: Set[int] = set()
#     repr_cache: Dict[int, str] = {}
#     repr_cache_get = repr_cache.get

#     def to_repr_text(node: Any) -> str:
#         """Convert object to repr."""
#         node_id = id(node)
#         cached = repr_cache_get(node_id)
#         if cached is not None:
#             return cached
#         try:
#             repr_text = repr(node)
#         except Exception as error:
#             repr_text = f"<error in repr: {error}>"
#         repr_cache[node_id] = repr_text
#         return repr_text

#     line_break: Optional[int] = None

#     def traverse(node: Any, level: int = 0) -> None:
#         """Walk the data structure."""

#         nonlocal line_break
#         append_line = lines.append

#         def append_text(text: str) -> None:
#             nonlocal max_width
#             nonlocal line_break
#             line = lines[-1]
#             line.append(text)
#             if max_width is not None and line.cell_len > max_width:
#                 if line_break is not None and len(lines) <= line_break:
#                     max_width = None
#                 else:
#                     line_break = len(lines)
#                     raise MaxLineReached(level)

#         node_id = id(node)
#         if node_id in visited_set:
#             # Recursion detected
#             append_text("...")
#             return

#         visited_set.add(node_id)
#         if type(node) in _CONTAINERS:
#             brace_open, brace_close, empty = _BRACES[type(node)]
#             expanded = level < expand_level

#             if not node:
#                 append_text(empty)
#             else:
#                 append_text(brace_open)
#                 if isinstance(node, dict):
#                     for last, (key, value) in loop_last(node.items()):
#                         if expanded:
#                             append_line(_Line())
#                             append_text(indent * (level + 1))
#                         append_text(f"{to_repr_text(key)}: ")
#                         traverse(value, level + 1)
#                         if not last:
#                             append_text(", ")
#                 else:
#                     for last, value in loop_last(node):
#                         if expanded:
#                             append_line(_Line())
#                             append_text(indent * (level + 1))
#                         traverse(value, level + 1)
#                         if not last:
#                             append_text(", ")
#                 if expanded:
#                     append_line(_Line())
#                     append_text(f"{indent * level}{brace_close}")
#                 else:
#                     append_text(brace_close)
#         else:
#             append_text(to_repr_text(node))
#         visited_set.remove(node_id)

#     # Keep expanding levels until the text fits
#     while True:
#         try:
#             traverse(_object)
#         except MaxLineReached:
#             del lines[:]
#             visited_set.clear()
#             lines.append(_Line())
#             expand_level += 1
#         else:
#             break  # pragma: no cover

#     text = Text(
#         "\n".join(line.text for line in lines),
#         justify=justify,
#         overflow=overflow,
#         no_wrap=no_wrap,
#     )
#     text = highlighter(text)
#     return text


@dataclass
class _Node:

    key_repr: str = ""
    value_repr: str = ""
    open_brace: str = ""
    close_brace: str = ""
    empty: str = ""
    children: Optional[List["_Node"]] = None
    _tokens: Optional[List[str]] = None

    def expandable(self) -> bool:
        return self.children is not None

    def iter_tokens(self) -> Iterable[str]:
        if self._tokens is not None:
            yield from self._tokens

        def tokenize() -> Iterable[str]:
            if self.key_repr:
                yield self.key_repr
                yield ": "
            if self.value_repr:
                yield self.value_repr
            elif self.children is not None:
                if self.children:
                    yield self.open_brace
                    for last, child in loop_last(self.children):
                        yield from child.iter_tokens()
                        if not last:
                            yield ", "
                    yield self.close_brace
                else:
                    self.empty

        tokens: List[str] = []
        append = tokens.append
        for token in tokenize():
            append(token)
            yield token
        self._tokens = tokens

    def check_length(self, start_length: int, max_length: int) -> bool:
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
    node: Optional[_Node] = None
    text: str = ""
    suffix: str = ""
    whitespace: str = ""
    expanded: bool = False

    def check_length(self, max_length: int) -> bool:
        start_length = len(self.whitespace) + cell_len(self.suffix)
        return self.node.check_length(start_length, max_length)

    def expand(self, indent_size: int) -> Iterable["_Line"]:
        node = self.node
        whitespace = self.whitespace
        yield _Line(
            text=node.open_brace, whitespace=whitespace, expanded=True,
        )
        child_whitespace = self.whitespace + " " * indent_size
        for child in self.node.children:
            line = _Line(node=child, whitespace=child_whitespace, suffix=",")
            yield line

        yield _Line(
            text=node.close_brace, whitespace=whitespace, expanded=True,
        )

    def __str__(self) -> str:
        return f"{self.whitespace}{self.text}{self.node or ''}{self.suffix}"


def pretty_repr(
    _object: Any,
    *,
    max_width: Optional[int] = 80,
    indent_size: int = 4,
    highlighter: Highlighter = None,
    justify: "JustifyMethod" = None,
    overflow: "OverflowMethod" = None,
    no_wrap: bool = True,
) -> Text:

    comma = ", "
    colon = ": "

    def to_repr(obj: Any) -> str:
        try:
            obj_repr = repr(obj)
        except Exception as error:
            obj_repr = f"<repr error {error}>"
        return obj_repr

    def traverse(obj: Any) -> _Node:

        if isinstance(obj, _CONTAINERS):
            open_brace, close_brace, empty = _BRACES[type(obj)]
            if obj:
                node = _Node(
                    open_brace=open_brace, close_brace=close_brace, children=[],
                )
                children = node.children
                append = children.append
                if isinstance(obj, dict):
                    for key, child in obj.items():
                        child_node = traverse(child)
                        child_node.key_repr = to_repr(key)
                        append(child_node)
                else:
                    for child in obj:
                        child_node = traverse(child)
                        append(child_node)
            else:
                node = _Node(value_repr=empty)
        else:
            node = _Node(value_repr=to_repr(obj))

        return node

    node = traverse(_object)
    print(str(node))

    def render(lines: List[_Line]):
        line_no = 0

        while line_no < len(lines):
            line = lines[line_no]
            if line.node and not line.expanded:
                if not line.check_length(max_width):
                    expand_lines = list(line.expand(indent_size))
                    lines[line_no : line_no + 1] = expand_lines
            line_no += 1

    lines = [_Line(node=node)]

    render(lines)
    repr_str = "\n".join(str(line) for line in lines)
    print("-" * max_width)
    return repr_str


if __name__ == "__main__":  # pragma: no cover

    data = [["Hello, world!"] * 3, [1000, 2323, 2424, 23423, 2323, 343434]]

    # data = {
    #     "foo": [1, "Hello World!", 2, 3, 4, {5, 6, 7, (1, 2, 3, 4), 8}],
    #     "bar": frozenset({1, 2, 3}),
    #     False: "This is false",
    #     True: "This is true",
    #     None: "This is None",
    #     # "Broken": BrokenRepr(),
    # }

    print(pretty_repr(data, max_width=50))

    if 0:

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
            # "Broken": BrokenRepr(),
        }
        # data["foo"].append(data)  # type: ignore

        print(pretty_repr(data, max_width=60))

        # from rich.console import Console

        # console = Console()
        # from rich import print

        # p = Pretty(data, overflow="ignore")
        # print(Measurement.get(console, p))
        # console.print(p, crop=False)
