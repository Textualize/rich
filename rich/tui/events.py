from dataclasses import dataclass, field
import re
from enum import auto, Enum
from time import monotonic
from typing import ClassVar, Optional, Set, TYPE_CHECKING

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
    CREATED = auto()
    IDLE = auto()
    RESIZE = auto()
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
    MOUSE_MOVE = auto()
    MOUSE_PRESSED = auto()
    MOUSE_RELEASED = auto()
    MOUSE_CLICKED = auto()
    MOUSE_DOUBLE_CLICKED = auto()
    MOUSE_ENTER = auto()
    MOUSE_LEAVE = auto()
    CUSTOM = 1000


@rich_repr
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


class Created(Event, type=EventType.CREATED):
    pass


class Idle(Event, type=EventType.IDLE):
    """Sent when there are no more items in the message queue."""


class Resize(Event, type=EventType.RESIZE):
    width: int
    height: int

    def __init__(self, sender: MessageTarget, width: int, height: int) -> None:
        self.width = width
        self.height = height
        super().__init__(sender)

    def __rich_repr__(self) -> RichReprResult:
        yield self.width
        yield self.height


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
class MouseMove(Event, type=EventType.MOUSE_MOVE):
    def __init__(self, sender: MessageTarget, x: int, y: int) -> None:
        super().__init__(sender)
        self.x = x
        self.y = y

    def __rich_repr__(self) -> RichReprResult:
        yield "x", self.x
        yield "y", self.y


@rich_repr
class MousePressed(Event, type=EventType.MOUSE_PRESSED):
    def __init__(
        self,
        sender: MessageTarget,
        x: int,
        y: int,
        button: int,
        alt: bool = False,
        ctrl: bool = False,
        shift: bool = False,
    ) -> None:
        super().__init__(sender)
        self.x = x
        self.y = y
        self.button = button
        self.alt = alt
        self.ctrl = ctrl
        self.shift = shift

    def __rich_repr__(self) -> RichReprResult:
        yield "x", self.x
        yield "y", self.y
        yield "button", self.button,
        yield "alt", self.alt, False
        yield "ctrl", self.ctrl, False
        yield "shift", self.shift, False


class MouseReleased(MousePressed, type=EventType.MOUSE_RELEASED):
    pass


class MouseClicked(MousePressed, type=EventType.MOUSE_CLICKED):
    pass


class MouseDoubleClicked(MousePressed, type=EventType.MOUSE_DOUBLE_CLICKED):
    pass


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
        yield self.timer.name


@rich_repr
class MouseEnter(Event, type=EventType.MOUSE_ENTER):
    def __init__(self, sender: MessageTarget, x: int, y: int) -> None:
        super().__init__(sender)
        self.x = x
        self.y = y

    def __rich_repr__(self) -> RichReprResult:
        yield "x", self.x
        yield "y", self.y


@rich_repr
class MouseLeave(Event, type=EventType.MOUSE_LEAVE):
    pass


class Focus(Event, type=EventType.FOCUS):
    pass


class Blur(Event, type=EventType.BLUR):
    pass