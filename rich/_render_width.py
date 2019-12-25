from typing import NamedTuple

from .segment import Segment


class RenderWidth(NamedTuple):
    """Range of widths for a renderable object."""

    minimum: int
    maximum: int

    @property
    def span(self) -> int:
        """Get difference between maximum and minimum."""
        return self.maximum - self.minimum

    def normalize(self) -> "RenderWidth":
        minimum, maximum = self
        minimum = max(0, minimum)
        return RenderWidth(minimum, max(minimum, maximum))

    def with_maximum(self, width: int) -> "RenderWidth":
        """Get a RenderableWith where the widths are <= width.
        
        Args:
            width (int): Maximum desired width.
        
        Returns:
            RenderableWidth: new RenderableWidth object.
        """
        minimum, maximum = self
        return RenderWidth(min(minimum, width), min(maximum, width))

    @classmethod
    def get(cls, renderable: "RenderableType", max_width: int) -> "RenderWidth":
        """Get desired width for a renderable."""
        if hasattr(renderable, "__console__"):
            get_console_width = getattr(renderable, "__console_width__", None)
            if get_console_width is not None:
                render_width = get_console_width(max_width).with_maximum(max_width)
                return render_width.normalize()
            else:
                return RenderWidth(1, max_width)
        elif isinstance(renderable, Segment):
            text, _style = renderable
            width = min(max_width, len(text))
            return RenderWidth(width, width)
        elif isinstance(renderable, str):
            text = renderable.rstrip()
            return RenderWidth(len(text), len(text))
        else:
            raise errors.NotRenderableError(
                f"Unable to get render width for {renderable!r}; "
                "a str, Segment, or object with __console__ method is required"
            )
