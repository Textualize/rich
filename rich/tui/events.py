from dataclasses import dataclass, field
import re
from enum import auto, Enum
from time import monotonic
from typing import ClassVar, Optional, TYPE_CHECKING

from ..repr import rich_repr, RichReprResult

from .message import Message
from .types import Callback, MessageTarget


if TYPE_CHECKING:
    from ._timer import Timer as TimerClass
    from ._timer import TimerCallback


class EventType(Enum):
    """Event type enumeration."""

    LOAD = auto()
    STARTUP = auto()
    MOUNT = auto()
    UNMOUNT = auto()
    SHUTDOWN_REQUEST = auto()
    SHUTDOWN = auto()
    EXIT = auto()
    REFRESH = auto()
    TIMER = auto()
    FOCUS = auto()
    BLUR = auto()
    KEY = auto()

    CUSTOM = 1000


class Event(Message):
    type: ClassVar[EventType]

    def __rich_repr__(self) -> RichReprResult:
        return
        yield

    def __init_subclass__(
        cls, type: EventType, priority: int = 0, bubble: bool = False
    ) -> None:
        super().__init_subclass__(priority=priority, bubble=bubble)

    def __enter__(self) -> "Event":
        return self

    def __exit__(self, exc_type, exc_value, exc_tb) -> Optional[bool]:
        if exc_type is not None:
            # Log and suppress exception
            return True


class ShutdownRequest(Event, type=EventType.SHUTDOWN_REQUEST):
    pass


class Load(Event, type=EventType.SHUTDOWN_REQUEST):
    pass


class Startup(Event, type=EventType.SHUTDOWN_REQUEST):
    pass


class Mount(Event, type=EventType.MOUNT):
    pass


class Unmount(Event, type=EventType.UNMOUNT):
    pass


class Shutdown(Event, type=EventType.SHUTDOWN):
    pass


class Refresh(Event, type=EventType.REFRESH):
    pass


@rich_repr
class Key(Event, type=EventType.KEY, bubble=True):
    code: int = 0

    def __init__(self, sender: MessageTarget, code: int) -> None:
        super().__init__(sender)
        self.code = code

    def __rich_repr__(self) -> RichReprResult:
        yield "code", self.code
        yield "key", self.key

    @property
    def key(self) -> str:
        return chr(self.code)


@rich_repr
class Timer(Event, type=EventType.TIMER, priority=10):
    def __init__(
        self,
        sender: MessageTarget,
        timer: "TimerClass",
        count: int = 0,
        callback: Optional["TimerCallback"] = None,
    ) -> None:
        super().__init__(sender)
        self.timer = timer
        self.count = count
        self.callback = callback

    def __rich_repr__(self) -> RichReprResult:
        yield "timer", self.timer


class Focus(Event, type=EventType.FOCUS):
    pass


class Blur(Event, type=EventType.BLUR):
    pass