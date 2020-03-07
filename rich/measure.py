from operator import itemgetter
from typing import Iterable, NamedTuple, TYPE_CHECKING, Union

from . import errors
from .protocol import is_renderable
from .segment import Segment

if TYPE_CHECKING:
    from .console import Console, RenderableType


class Measurement(NamedTuple):
    """Range of widths for a renderable object."""

    minimum: int
    maximum: int

    @property
    def span(self) -> int:
        """Get difference between maximum and minimum."""
        return self.maximum - self.minimum

    def normalize(self) -> "Measurement":
        minimum, maximum = self
        minimum = max(0, minimum)
        return Measurement(minimum, max(minimum, maximum))

    def with_maximum(self, width: int) -> "Measurement":
        """Get a RenderableWith where the widths are <= width.
        
        Args:
            width (int): Maximum desired width.
        
        Returns:
            RenderableWidth: new RenderableWidth object.
        """
        minimum, maximum = self
        return Measurement(min(minimum, width), min(maximum, width))

    @classmethod
    def get(
        cls, console: "Console", renderable: "RenderableType", max_width: int
    ) -> "Measurement":
        """Get desired width for a renderable."""
        if isinstance(renderable, str):
            renderable = console.render_str(renderable)
        if is_renderable(renderable):
            get_console_width = getattr(renderable, "__measure__", None)
            if get_console_width is not None:
                render_width = get_console_width(console, max_width).with_maximum(
                    max_width
                )
                return render_width.normalize()
            else:
                return Measurement(1, max_width)
        else:
            raise errors.NotRenderableError(
                f"Unable to get render width for {renderable!r}; "
                "a str, Segment, or object with __console__ method is required"
            )


def measure_renderables(
    console: "Console", renderables: Iterable["RenderableType"], max_width: int
) -> "Measurement":
    """Measure a number of renderables."""

    get_measurement = Measurement.get
    measurements = [
        get_measurement(console, renderable, max_width) for renderable in renderables
    ]
    measured_width = Measurement(
        max(measurements, key=itemgetter(0)).minimum,
        max(measurements, key=itemgetter(1)).maximum,
    )
    return measured_width
