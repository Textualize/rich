from typing import Optional, TYPE_CHECKING

from .jupyter import JupyterMixin
from .measure import Measurement

if TYPE_CHECKING:
    from .console import Console, ConsoleOptions, RenderableType, RenderResult


class Constrain(JupyterMixin):
    """Constrain the width of a renderable to a given number of characters.
    
    Args:
        renderable (RenderableType): A renderable object.
        width (int, optional): The maximum width (in characters) to render. Defaults to 80.
    """

    def __init__(self, renderable: "RenderableType", width: Optional[int] = 80) -> None:
        self.renderable = renderable
        self.width = width

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":
        if self.width is None:
            yield self.renderable
        else:
            child_options = options.update(width=min(self.width, options.max_width))
            yield from console.render(self.renderable, child_options)

    def __rich_measure__(self, console: "Console", max_width: int) -> "Measurement":
        if self.width is None:
            return Measurement.get(console, self.renderable, max_width)
        else:
            width = min(self.width, max_width)
            return Measurement(width, width)
