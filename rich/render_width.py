from operator import itemgetter
from typing import Iterable, NamedTuple, TYPE_CHECKING, Union

from . import errors
from .protocol import is_renderable
from .segment import Segment

if TYPE_CHECKING:
    from .console import Console, RenderableType


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
    def get(
        cls, console: "Console", renderable: "RenderableType", max_width: int
    ) -> "RenderWidth":
        """Get desired width for a renderable."""
        if isinstance(renderable, str):
            renderable = console.render_str(renderable)
        if is_renderable(renderable):
            get_console_width = getattr(renderable, "__console_width__", None)
            if get_console_width is not None:
                render_width = get_console_width(console, max_width).with_maximum(
                    max_width
                )
                return render_width.normalize()
            else:
                return RenderWidth(1, max_width)
        else:
            raise errors.NotRenderableError(
                f"Unable to get render width for {renderable!r}; "
                "a str, Segment, or object with __console__ method is required"
            )

    @classmethod
    def measure(
        cls, console: "Console", renderables: Iterable["RenderableType"], max_width: int
    ) -> "RenderWidth":
        """Measure a number of renderables."""

        render_widths = [
            RenderWidth.get(console, renderable, max_width)
            for renderable in renderables
        ]
        measured_width = RenderWidth(
            max(render_widths, key=itemgetter(0)).minimum,
            max(render_widths, key=itemgetter(1)).maximum,
        )
        return measured_width
