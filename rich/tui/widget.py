from typing import TYPE_CHECKING

from . import events
from .message_pump import MessagePump

if TYPE_CHECKING:
    from .app import App


class Widget:
    def __init__(self, app: App) -> None:
        self.app = app

    def focus(self):
        pass

    def blur(self):
        pass