from typing import Callable, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from .events import Event
    from .message import Message

Callback = Callable[[], None]
# IntervalID = int


class MessageTarget(Protocol):
    async def post_message(self, message: "Message", priority: int = 0) -> bool:
        ...


class EventTarget(Protocol):
    async def post_message(self, event: "Event", priority: int = 0) -> bool:
        ...