from rich.align import Align
from rich.padding import Padding

from rich.tui.widget import Widget
from rich.tui.events import KeyEvent


class ColorChanger(Widget):
    def __init__(self) -> None:
        self.color = 0

    async def render(self):
        return Align.center(
            "Press any key", vertical="middle", style=f"color({self.color})"
        )

    async def on_key(self, event: KeyEvent) -> None:
        self.color = ord(event.key) % 255