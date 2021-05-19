from typing import Awaitable, Callable, Optional, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from .events import Event
    from .message import Message

Callback = Callable[[], None]
# IntervalID = int


class MessageTarget(Protocol):
    async def post_message(
        self,
        message: "Message",
        priority: Optional[int] = None,
    ) -> bool:
        ...


class EventTarget(Protocol):
    async def post_message(
        self,
        message: "Message",
        priority: Optional[int] = None,
    ) -> bool:
        ...


MessageHandler = Callable[["Message"], Awaitable]