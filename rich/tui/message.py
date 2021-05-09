from .case import camel_to_snake

from .types import MessageTarget


class Message:
    """Base class for a message."""

    sender: MessageTarget
    bubble: bool = False
    default_priority: int = 0

    def __init__(self, sender: MessageTarget) -> None:
        self.sender = sender
        self.name = camel_to_snake(self.__class__.__name__)
