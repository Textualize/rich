from typing import NamedTuple, Optional

from .style import Style


class StyledText(NamedTuple):
    """A piece of text with associated style."""

    text: str
    style: Optional[Style] = None

    def __repr__(self) -> str:
        """Simplified repr."""
        return f"StyledText({self.text!r}, {self.style!r})"
