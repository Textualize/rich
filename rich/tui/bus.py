from asyncio import PriorityQueue
from dataclasses import dataclass
from functools import total_ordering
from typing import AsyncGenerator, Generic, NamedTuple, Optional, TypeVar


BusType = TypeVar("BusType")


@dataclass(order=True, frozen=True)
class QueueItem(Generic[BusType]):
    """An item and meta data on the event queue."""

    event: BusType
    priority: int


class Bus(Generic[BusType]):
    def __init__(self) -> None:
        self.queue: "PriorityQueue[Optional[QueueItem[BusType]]]" = PriorityQueue()
        self._closing = False
        self._closed = False

    @property
    def is_closing(self) -> bool:
        return self._closing

    @property
    def is_closed(self) -> bool:
        return self._closed

    def post(self, event: BusType, priority: int = 0) -> bool:
        """Post an item on the bus.

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
        item: QueueItem[BusType] = QueueItem(event, priority=-priority)
        self.queue.put_nowait(item)
        return True

    def close(self) -> None:
        """Close the event pump after processing remaining events."""
        self._closing = True
        self.queue.put_nowait(None)

    async def get(self) -> Optional[BusType]:
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

    async def __aiter__(self) -> AsyncGenerator[BusType, None]:
        while not self._closed:
            event = await self.get()
            if event is None:
                break
            yield event
