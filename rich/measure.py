from operator import itemgetter
from typing import Iterable, NamedTuple, TYPE_CHECKING, Union

from . import errors
from .protocol import is_renderable
from .segment import Segment

if TYPE_CHECKING:
    from .console import Console, RenderableType


class Measurement(NamedTuple):
    """Stores the minimum and maximum widths (in characters) required to render an object."""

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
        """Get a measurement for a renderable.

        Args:
            console (~rich.console.Console): Console instance.
            renderable (RenderableType): An object that may be rendered with Rich.
            max_width (int): The maximum width available.

        Raises:
            errors.NotRenderableError: If the object is not renderable.

        Returns:
            Measurement: Measurement object containing range of character widths required to render the object.
        """

        if isinstance(renderable, str):
            renderable = console.render_str(renderable)

        renderable = getattr(renderable, "__rich__", renderable)
        if is_renderable(renderable):
            get_console_width = getattr(renderable, "__rich_measure__", None)
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
                "a str, Segment, or object with __rich_console__ method is required"
            )


def measure_renderables(
    console: "Console", renderables: Iterable["RenderableType"], max_width: int
) -> "Measurement":
    """Get a measurement that would fit a number of renderables.

    Args:
        console (~rich.console.Console): Console instance.
        renderables (Iterable[RenderableType]): One or more renderable objects.
        max_width (int): The maximum width available.

    Returns:
        Measurement: Measurement object containing range of character widths required to
        contain all given renderables.
    """

    get_measurement = Measurement.get
    measurements = [
        get_measurement(console, renderable, max_width) for renderable in renderables
    ]
    measured_width = Measurement(
        max(measurements, key=itemgetter(0)).minimum,
        max(measurements, key=itemgetter(1)).maximum,
    )
    return measured_width
