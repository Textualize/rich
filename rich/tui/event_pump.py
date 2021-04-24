from asyncio import PriorityQueue
from functools import total_ordering
from typing import AsyncGenerator, NamedTuple, Optional

from .events import Event


@total_ordering
class QueueItem(NamedTuple):
    """An item and meta data on the event queue."""

    event: Event
    priority: int

    def __eq__(self, other: "QueueItem") -> bool:
        return self.priority == other.priority

    def __lt__(self, other: "QueueItem") -> bool:
        return self.priority < other.priority


class EventPump:
    def __init__(self) -> None:
        self.queue: "PriorityQueue[Optional[QueueItem]]" = PriorityQueue()
        self._closing = False
        self._closed = False

    @property
    def is_closing(self) -> bool:
        return self._closing

    @property
    def is_closed(self) -> bool:
        return self._closed

    def post(self, event: Event, priority: int = 0) -> bool:
        """Post an event on the queue.

        If the event pump is closing or closed, the event will not be posted, and the method
        will return ``False``.

        Args:
            event (Event): An Event object
            priority (int, optional): Priority of event (greater priority processed first). Defaults to 0.

        Returns:
            bool: Return True if the event was posted, otherwise False.
        """
        if self._closing or self._closed:
            return False
        self.queue.put_nowait(QueueItem(event, priority=-priority))
        return True

    def close(self) -> None:
        """Close the event pump after processing remaining events."""
        self._closing = True
        self.queue.put_nowait(None)

    async def get(self) -> Optional[Event]:
        """Get the next event on the queue, or None if queue is closed.

        Returns:
            Optional[Event]: Event object or None.
        """
        if self._closed:
            return None
        queue_item = await self.queue.get()
        if queue_item is None:
            self._closed = True
            return None
        return queue_item.event

    async def __aiter__(self) -> AsyncGenerator[Event, None]:
        while not self._closed:
            event = await self.get()
            if event is None:
                break
            yield event