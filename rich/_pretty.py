from dataclasses import dataclass
from typing import Any, NamedTuple, Optional, Iterable, List, Tuple

from .text import Text


@dataclass
class Node:
    braces: Tuple[str, str] = ("", "")
    children: List["Node"] = []


class StackEntry:
    node: Node
    iter_children: Optional[Iterable[Any]] = None


def pretty_format(root_obj: Any):
    stack: List[StackEntry] = []
    root = Node()
    obj = root_obj

    while stack:
        entry = stack.pop()
        node, iter_children = entry
        if iter_children is not None:
            next(iter_children, None)

    if isinstance(obj, list):
        node
