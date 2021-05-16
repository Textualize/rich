from typing import AsyncIterable, Optional, TYPE_CHECKING
from asyncio import ensure_future, Task, PriorityQueue
from asyncio import Event as AIOEvent
from dataclasses import dataclass
import logging

from . import events
from .message import Message
from ._timer import Timer, TimerCallback

log = logging.getLogger("rich")


@dataclass(order=True, frozen=True)
class MessageQueueItem:
    message: Message
    priority: int


class MessagePump:
    def __init__(self, queue_size: int = 10) -> None:
        self._queue_size = queue_size
        self._message_queue: "PriorityQueue[Optional[MessageQueueItem]]" = (
            PriorityQueue(queue_size)
        )
        self._closing: bool = False
        self._closed: bool = False

    async def get_message(self) -> Optional[Message]:
        """Get the next event on the queue, or None if queue is closed.

        Returns:
            Optional[Event]: Event object or None.
        """
        if self._closed:
            return None
        queue_item = await self._message_queue.get()
        if queue_item is None:
            self._closed = True
            return None
        return queue_item.message

    def set_timer(
        self,
        delay: float,
        *,
        name: Optional[str] = None,
        callback: TimerCallback = None,
    ) -> Timer:
        timer = Timer(self, delay, name=name, callback=callback, repeat=0)
        asyncio.get_event_loop().create_task(timer.run())
        return timer

    def set_interval(
        self,
        interval: float,
        *,
        name: Optional[str] = None,
        callback: TimerCallback = None,
        repeat: int = 0,
    ):
        timer = Timer(
            self, interval, self, name=name, callback=callback, repeat=repeat or None
        )
        asyncio.get_event_loop().create_task(timer.run())
        return timer

    async def close_messages(self) -> None:
        self._closing = True
        await self._message_queue.put(None)

    async def process_messages(self) -> None:

        while not self._closed:
            try:
                message = await self.get_message()
            except Exception as error:
                log.exception("error getting message")
                raise
            log.debug("message=%r", message)
            if message is None:
                break
            await self.dispatch_message(message)

    async def dispatch_message(self, message: Message) -> None:
        if isinstance(message, events.Event):
            method_name = f"on_{message.name}"
            log.debug("method=%s", method_name)
            dispatch_function = getattr(self, method_name, None)
            log.debug("dispatch=%r", dispatch_function)
            if dispatch_function is not None:
                await dispatch_function(message)
        else:
            await self.on_message(message)

    async def on_message(self, message: Message) -> None:
        pass

    async def post_message(
        self, message: Message, priority: Optional[int] = None
    ) -> bool:
        if self._closing or self._closed:
            return False
        event_priority = priority if priority is not None else message.default_priority
        item = MessageQueueItem(message, priority=event_priority)
        await self._message_queue.put(item)
        return True

    async def on_timer(self, event: events.Timer) -> None:
        if event.callback is not None:
            await event.callback(event)


if __name__ == "__main__":

    class Widget(MessagePump):
        pass

    widget1 = Widget()
    widget2 = Widget()

    import asyncio

    asyncio.get_event_loop().run_until_complete(widget1.run_message_loop())