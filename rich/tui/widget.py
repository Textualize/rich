from typing import TYPE_CHECKING

from . import events
from .message_pump import MessagePump

if TYPE_CHECKING:
    from .app import App


class Widget(MessagePump):
    async def refresh(self) -> None:
        await self.emit(events.Refresh(self))