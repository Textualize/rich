from typing import AsyncIterable, Optional, TYPE_CHECKING
from asyncio import ensure_future, Task, PriorityQueue
from asyncio import Event as AIOEvent
from dataclasses import dataclass

from . import events
from .message import Message
from ._timer import Timer, TimerCallback


@dataclass(order=True, frozen=True)
class MessageQueueItem:
    message: Message
    priority: int


class MessagePump:
    def __init__(self, queue_size: int = 10) -> None:
        self._message_queue: "PriorityQueue[Optional[MessageQueueItem]]" = (
            PriorityQueue(maxsize=queue_size)
        )
        self._closing: bool = False
        self._closed: bool = False
        self._done_event = AIOEvent()

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

    async def close_messages(self, wait: bool = True) -> None:
        self._closing = True
        await self._message_queue.put(None)
        if wait:
            await self._done_event.wait()

    async def run(self) -> None:
        from time import time

        start = time()

        async def stuff(event: events.Timer):
            print("TIMER", event)
            print(time() - start)

        self.set_interval(0.1, callback=stuff)
        try:
            while not self._closed:
                message = await self.get_message()
                if message is None:
                    break
                await self.dispatch_message(message)
        finally:
            self._done_event.set()

    async def dispatch_message(self, message: Message) -> None:
        if isinstance(message, events.Event):
            dispatch_function = getattr(self, f"on_{message.name}", None)
            if dispatch_function is not None:
                await dispatch_function(message)
        else:
            await self.on_message(message)

    async def on_message(self, message: Message) -> None:
        pass

    async def post_message(
        self, event: Message, priority: Optional[int] = None
    ) -> bool:
        if self._closing or self._closed:
            return False
        event_priority = priority if priority is not None else event.default_priority
        item = MessageQueueItem(event, priority=event_priority)
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

    asyncio.get_event_loop().run_until_complete(widget1.run())