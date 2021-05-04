from dataclasses import dataclass, field
import re
from enum import auto, Enum
from time import time
from typing import ClassVar, Optional

from rich.repr import rich_repr, RichReprResult
from .bus import Bus
from .case import camel_to_snake
from .types import Callback


class EventType(Enum):
    """Event type enumeration."""

    CUSTOM = auto()
    LOAD = auto()
    STARTUP = auto()
    MOUNT = auto()
    UNMOUNT = auto()
    SHUTDOWN_REQUEST = auto()
    SHUTDOWN = auto()
    EXIT = auto()
    REFRESH = auto()
    TIMER = auto()
    INTERVAL = auto()
    KEY = auto()


EventBus = Bus["Event"]


class Event:
    type: ClassVar[EventType]
    bubble: bool = False

    def __init__(self) -> None:
        self.time = time()
        self._suppressed = False

    def __rich_repr__(self) -> RichReprResult:
        return
        yield

    def __init_subclass__(cls, type: EventType) -> None:
        super().__init_subclass__()
        cls.type = type

    @property
    def is_suppressed(self) -> bool:
        return self._suppressed

    @property
    def name(self) -> str:
        if not hasattr(self, "_name"):
            _name = camel_to_snake(self.__class__.__name__)
            if _name.endswith("_event"):
                _name = _name[:-6]
            self._name = _name
        return self._name

    def __enter__(self) -> "Event":
        return self

    def __exit__(self, exc_type, exc_value, exc_tb) -> Optional[bool]:
        if exc_type is not None:
            # Log and suppress exception
            return True

    def suppress(self, suppress: bool = True) -> None:
        self._suppressed = suppress


class ShutdownRequestEvent(Event, type=EventType.SHUTDOWN_REQUEST):
    pass


class LoadEvent(Event, type=EventType.SHUTDOWN_REQUEST):
    pass


class StartupEvent(Event, type=EventType.SHUTDOWN_REQUEST):
    pass


class MountEvent(Event, type=EventType.MOUNT):
    pass


class UnmountEvent(Event, type=EventType.UNMOUNT):
    pass


class ShutdownEvent(Event, type=EventType.SHUTDOWN):
    pass


class RefreshEvent(Event, type=EventType.REFRESH):
    pass


@rich_repr
class KeyEvent(Event, type=EventType.KEY):
    code: int = 0

    def __init__(self, code: int) -> None:
        super().__init__()
        self.code = code

    def __rich_repr__(self) -> RichReprResult:
        yield "code", self.code
        yield "key", self.key

    @property
    def key(self) -> str:
        return chr(self.code)


class TimerEvent(Event, type=EventType.TIMER):
    pass


class IntervalEvent(Event, type=EventType.INTERVAL):
    pass
