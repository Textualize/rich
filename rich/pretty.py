import builtins
import os
import sys
from array import array
from collections import Counter, abc, defaultdict, deque
from dataclasses import dataclass
from itertools import islice
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

from .abc import RichRenderable
from . import get_console
from ._pick import pick_bool
from .cells import cell_len
from .highlighter import ReprHighlighter
from .jupyter import JupyterRenderable
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
    indent_guides: bool = False,
    max_length: int = None,
    max_string: int = None,
    expand_all: bool = False,
) -> None:
    """Install automatic pretty printing in the Python REPL.

    Args:
        console (Console, optional): Console instance or ``None`` to use global console. Defaults to None.
        overflow (Optional[OverflowMethod], optional): Overflow method. Defaults to "ignore".
        crop (Optional[bool], optional): Enable cropping of long lines. Defaults to False.
        indent_guides (bool, optional): Enable indentation guides. Defaults to False.
        max_length (int, optional): Maximum length of containers before abbreviating, or None for no abbreviation.
            Defaults to None.
        max_string (int, optional): Maximum length of string before truncating, or None to disable. Defaults to None.
        expand_all (bool, optional): Expand all containers. Defaults to False
    """
    from rich import get_console
    from .console import ConsoleRenderable  # needed here to prevent circular import

    console = console or get_console()
    assert console is not None

    def display_hook(value: Any) -> None:
        """Replacement sys.displayhook which prettifies objects with Rich."""
        if value is not None:
            assert console is not None
            builtins._ = None  # type: ignore
            console.print(
                value
                if isinstance(value, RichRenderable)
                else Pretty(
                    value,
                    overflow=overflow,
                    indent_guides=indent_guides,
                    max_length=max_length,
                    max_string=max_string,
                    expand_all=expand_all,
                ),
                crop=crop,
            )
            builtins._ = value  # type: ignore

    def ipy_display_hook(value: Any) -> None:  # pragma: no cover
        assert console is not None
        # always skip rich generated jupyter renderables or None values
        if isinstance(value, JupyterRenderable) or value is None:
            return
        # on jupyter rich display, if using one of the special representations dont use rich
        if console.is_jupyter and any(attr.startswith("_repr_") for attr in dir(value)):
            return

        # certain renderables should start on a new line
        if isinstance(value, ConsoleRenderable):
            console.line()

        console.print(
            value
            if isinstance(value, RichRenderable)
            else Pretty(
                value,
                overflow=overflow,
                indent_guides=indent_guides,
                max_length=max_length,
                max_string=max_string,
                expand_all=expand_all,
                margin=12,
            ),
            crop=crop,
        )

    try:  # pragma: no cover
        ip = get_ipython()  # type: ignore
        from IPython.core.formatters import BaseFormatter

        # replace plain text formatter with rich formatter
        rich_formatter = BaseFormatter()
        rich_formatter.for_type(object, func=ipy_display_hook)
        ip.display_formatter.formatters["text/plain"] = rich_formatter
    except Exception:
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
        indent_guides (bool, optional): Enable indentation guides. Defaults to False.
        max_length (int, optional): Maximum length of containers before abbreviating, or None for no abbreviation.
            Defaults to None.
        max_string (int, optional): Maximum length of string before truncating, or None to disable. Defaults to None.
        expand_all (bool, optional): Expand all containers. Defaults to False.
        margin (int, optional): Subtrace a margin from width to force containers to expand earlier. Defaults to 0.
        insert_line (bool, optional): Insert a new line if the output has multiple new lines. Defaults to False.
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
        indent_guides: bool = False,
        max_length: int = None,
        max_string: int = None,
        expand_all: bool = False,
        margin: int = 0,
        insert_line: bool = False,
    ) -> None:
        self._object = _object
        self.highlighter = highlighter or ReprHighlighter()
        self.indent_size = indent_size
        self.justify = justify
        self.overflow = overflow
        self.no_wrap = no_wrap
        self.indent_guides = indent_guides
        self.max_length = max_length
        self.max_string = max_string
        self.expand_all = expand_all
        self.margin = margin
        self.insert_line = insert_line

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":
        pretty_str = pretty_repr(
            self._object,
            max_width=options.max_width - self.margin,
            indent_size=self.indent_size,
            max_length=self.max_length,
            max_string=self.max_string,
            expand_all=self.expand_all,
        )
        pretty_text = Text(
            pretty_str,
            justify=self.justify or options.justify,
            overflow=self.overflow or options.overflow,
            no_wrap=pick_bool(self.no_wrap, options.no_wrap),
            style="pretty",
        )
        pretty_text = self.highlighter(pretty_text)
        if self.indent_guides and not options.ascii_only:
            pretty_text = pretty_text.with_indent_guides(
                self.indent_size, style="repr.indent"
            )
        if self.insert_line and "\n" in pretty_text:
            yield ""
        yield pretty_text

    def __rich_measure__(self, console: "Console", max_width: int) -> "Measurement":
        pretty_str = pretty_repr(
            self._object,
            max_width=max_width,
            indent_size=self.indent_size,
            max_length=self.max_length,
            max_string=self.max_string,
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
    tuple: lambda _object: ("(", ")", "()"),
}
_CONTAINERS = tuple(_BRACES.keys())
_MAPPING_CONTAINERS = (dict, os._Environ)


@dataclass
class Node:
    """A node in a repr tree. May be atomic or a container."""

    key_repr: str = ""
    value_repr: str = ""
    open_brace: str = ""
    close_brace: str = ""
    empty: str = ""
    last: bool = False
    is_tuple: bool = False
    children: Optional[List["Node"]] = None

    @property
    def separator(self) -> str:
        """Get separator between items."""
        return "" if self.last else ","

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

    def render(
        self, max_width: int = 80, indent_size: int = 4, expand_all: bool = False
    ) -> str:
        """Render the node to a pretty repr.

        Args:
            max_width (int, optional): Maximum width of the repr. Defaults to 80.
            indent_size (int, optional): Size of indents. Defaults to 4.
            expand_all (bool, optional): Expand all levels. Defaults to False.

        Returns:
            str: A repr string of the original object.
        """
        lines = [_Line(node=self, is_root=True)]
        line_no = 0
        while line_no < len(lines):
            line = lines[line_no]
            if line.expandable and not line.expanded:
                if expand_all or not line.check_length(max_width):
                    lines[line_no : line_no + 1] = line.expand(indent_size)
            line_no += 1

        repr_str = "\n".join(str(line) for line in lines)
        return repr_str


@dataclass
class _Line:
    """A line in repr output."""

    is_root: bool = False
    node: Optional[Node] = None
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
        tuple_of_one = node.is_tuple and len(node.children) == 1
        for child in node.children:
            separator = "," if tuple_of_one else child.separator
            line = _Line(
                node=child,
                whitespace=child_whitespace,
                suffix=separator,
            )
            yield line

        yield _Line(
            text=node.close_brace,
            whitespace=whitespace,
            suffix="," if (tuple_of_one and not self.is_root) else node.separator,
        )

    def __str__(self) -> str:
        return f"{self.whitespace}{self.text}{self.node or ''}{self.suffix}"


def traverse(_object: Any, max_length: int = None, max_string: int = None) -> Node:
    """Traverse object and generate a tree.

    Args:
        _object (Any): Object to be traversed.
        max_length (int, optional): Maximum length of containers before abbreviating, or None for no abbreviation.
            Defaults to None.
        max_string (int, optional): Maximum length of string before truncating, or None to disable truncating.
            Defaults to None.

    Returns:
        Node: The root of a tree structure which can be used to render a pretty repr.
    """

    def to_repr(obj: Any) -> str:
        """Get repr string for an object, but catch errors."""
        if (
            max_string is not None
            and isinstance(obj, (bytes, str))
            and len(obj) > max_string
        ):
            truncated = len(obj) - max_string
            obj_repr = f"{obj[:max_string]!r}+{truncated}"
        else:
            try:
                obj_repr = repr(obj)
            except Exception as error:
                obj_repr = f"<repr-error '{error}'>"
        return obj_repr

    visited_ids: Set[int] = set()
    push_visited = visited_ids.add
    pop_visited = visited_ids.remove

    def _traverse(obj: Any, root: bool = False) -> Node:
        """Walk the object depth first."""
        obj_type = type(obj)
        if obj_type in _CONTAINERS:
            obj_id = id(obj)

            if obj_id in visited_ids:
                # Recursion detected
                return Node(value_repr="...")
            push_visited(obj_id)
            open_brace, close_brace, empty = _BRACES[obj_type](obj)

            if obj:
                children: List[Node] = []
                node = Node(
                    open_brace=open_brace,
                    close_brace=close_brace,
                    children=children,
                    last=root,
                )
                append = children.append
                num_items = len(obj)
                last_item_index = num_items - 1

                if isinstance(obj, _MAPPING_CONTAINERS):
                    iter_items = iter(obj.items())
                    if max_length is not None:
                        iter_items = islice(iter_items, max_length)
                    for index, (key, child) in enumerate(iter_items):
                        child_node = _traverse(child)
                        child_node.key_repr = to_repr(key)
                        child_node.last = index == last_item_index
                        append(child_node)
                else:
                    iter_values = iter(obj)
                    if max_length is not None:
                        iter_values = islice(iter_values, max_length)
                    for index, child in enumerate(iter_values):
                        child_node = _traverse(child)
                        child_node.last = index == last_item_index
                        append(child_node)
                if max_length is not None and num_items > max_length:
                    append(Node(value_repr=f"... +{num_items-max_length}", last=True))
            else:
                node = Node(empty=empty, children=[], last=root)

            pop_visited(obj_id)
        else:
            node = Node(value_repr=to_repr(obj), last=root)
        node.is_tuple = isinstance(obj, tuple)
        return node

    node = _traverse(_object, root=True)
    return node


def pretty_repr(
    _object: Any,
    *,
    max_width: int = 80,
    indent_size: int = 4,
    max_length: int = None,
    max_string: int = None,
    expand_all: bool = False,
) -> str:
    """Prettify repr string by expanding on to new lines to fit within a given width.

    Args:
        _object (Any): Object to repr.
        max_width (int, optional): Desired maximum width of repr string. Defaults to 80.
        indent_size (int, optional): Number of spaces to indent. Defaults to 4.
        max_length (int, optional): Maximum length of containers before abbreviating, or None for no abbreviation.
            Defaults to None.
        max_string (int, optional): Maximum length of string before truncating, or None to disable truncating.
            Defaults to None.
        expand_all (bool, optional): Expand all containers regardless of available width. Defaults to False.

    Returns:
        str: A possibly multi-line representation of the object.
    """

    if isinstance(_object, Node):
        node = _object
    else:
        node = traverse(_object, max_length=max_length, max_string=max_string)
    repr_str = node.render(
        max_width=max_width, indent_size=indent_size, expand_all=expand_all
    )
    return repr_str


def pprint(
    _object: Any,
    *,
    console: "Console" = None,
    indent_guides: bool = True,
    max_length: int = None,
    max_string: int = None,
    expand_all: bool = False,
):
    """A convenience function for pretty printing.

    Args:
        _object (Any): Object to pretty print.
        console (Console, optional): Console instance, or None to use default. Defaults to None.
        max_length (int, optional): Maximum length of containers before abbreviating, or None for no abbreviation.
            Defaults to None.
        max_string (int, optional): Maximum length of strings before truncating, or None to disable. Defaults to None.
        indent_guides (bool, optional): Enable indentation guides. Defaults to True.
        expand_all (bool, optional): Expand all containers. Defaults to False.
    """
    _console = get_console() if console is None else console
    _console.print(
        Pretty(
            _object,
            max_length=max_length,
            max_string=max_string,
            indent_guides=indent_guides,
            expand_all=expand_all,
            overflow="ignore",
        ),
        soft_wrap=True,
    )


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
                "durian" * 100,
            ]
        ),
        "atomic": (False, True, None),
        "Broken": BrokenRepr(),
    }
    data["foo"].append(data)  # type: ignore

    from rich import print

    print(Pretty(data, indent_guides=True, max_string=20))
