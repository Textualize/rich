from typing import List, TypeVar

T = TypeVar("T")


class Stack(List[T]):
    """A small shim over builtin list."""

    @property
    def top(self) -> T:
        """Get top of stack."""
        return self[-1]

    def push(self, item: T) -> None:
        self.append(item)
