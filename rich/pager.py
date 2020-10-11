from abc import ABC, abstractmethod
import pydoc


class SystemPager:
    """Uses the pager installed on the system."""

    _pager = lambda self, content: pydoc.pager(content)

    def show(self, content: str) -> None:
        """Use the same pager used by pydoc."""
        self._pager(content)


if __name__ == "__main__":  # pragma: no cover
    from .__main__ import make_test_card
    from .console import Console

    console = Console()
    with console.pager(styles=True):
        console.print(make_test_card())
