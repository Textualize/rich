from time import monotonic
from typing import ClassVar

from .case import camel_to_snake

from .types import MessageTarget


class Message:
    """Base class for a message."""

    sender: MessageTarget
    bubble: ClassVar[bool] = False
    default_priority: ClassVar[int] = 0

    def __init__(self, sender: MessageTarget) -> None:
        self.sender = sender
        self.name = camel_to_snake(self.__class__.__name__)
        self.time = monotonic()

    def __init_subclass__(cls, bubble: bool = False, priority: int = 0) -> None:
        super().__init_subclass__()
        cls.bubble = bubble
        cls.default_priority = priority