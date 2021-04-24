from dataclasses import dataclass, field
import re
from enum import auto, Enum
from time import time
from typing import ClassVar, Optional

from rich.repr import rich_repr, RichReprResult
from .case import camel_to_snake
from .types import Callback


class EventType(Enum):
    """Event type enumeration."""

    LOAD = auto()
    STARTUP = auto()
    SHUTDOWN_REQUEST = auto
    SHUTDOWN = auto()
    EXIT = auto()
    REFRESH = auto()
    TIMER = auto()
    INTERVAL = auto()
    KEY = auto()


class Event:
    type: ClassVar[EventType]

    def __init__(self) -> None:
        self.time = time()

    def __rich_repr__(self) -> RichReprResult:
        return
        yield

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


class ShutdownRequestEvent(Event):
    type: EventType = EventType.SHUTDOWN_REQUEST


class LoadEvent(Event):
    type: EventType = EventType.SHUTDOWN_REQUEST


class StartupEvent(Event):
    type: EventType = EventType.SHUTDOWN_REQUEST


class ShutdownEvent(Event):
    pass


class RefreshEvent(Event):
    pass


@rich_repr
class KeyEvent(Event):
    type: EventType = EventType.KEY
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


class TimerEvent(Event):
    type: EventType = EventType.TIMER


class IntervalEvent(Event):
    type: EventType = EventType.INTERVAL
