from typing import Optional

from rich.console import RenderableType
from ..widget import Widget


class Window(Widget):
    renderable: Optional[RenderableType]

    def __init__(self, renderable: RenderableType):
        self.renderable = renderable

    def update(self, renderable: RenderableType) -> None:
        self.renderable = renderable