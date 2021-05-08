from typing import AsyncIterable, Optional, TYPE_CHECKING
from asyncio import ensure_future, Task, PriorityQueue
from asyncio import Event as AIOEvent
from dataclasses import dataclass

from . import events
from ._timer import Timer, TimerCallback


@dataclass(order=True, frozen=True)
class EventQueueItem:
    event: events.Event
    priority: int


class EventLoop:
    def __init__(self) -> None:
        self._event_queue: "PriorityQueue[Optional[EventQueueItem]]" = PriorityQueue()
        self._closing: bool = False
        self._closed: bool = False
        self._done_event = AIOEvent()

    async def get_event(self) -> Optional[events.Event]:
        """Get the next event on the queue, or None if queue is closed.

        Returns:
            Optional[Event]: Event object or None.
        """
        if self._closed:
            return None
        queue_item = await self._event_queue.get()
        if queue_item is None:
            self._closed = True
            return None
        return queue_item.event

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
            self, interval, name=name, callback=callback, repeat=repeat or None
        )
        asyncio.get_event_loop().create_task(timer.run())
        return timer

    def close_events(self) -> None:
        self._closing = True
        self._event_queue.put_nowait(None)

    async def wait_for_events(self) -> None:
        await self._done_event.wait()

    async def run(self) -> None:
        async def stuff(timer: Timer):
            print("TIMER", timer)

        self.set_interval(1, callback=stuff, repeat=1)
        try:
            while not self._closed:
                event = await self.get_event()
                if event is None:
                    break
                dispatch_function = getattr(self, f"on_{event.name}", None)
                if dispatch_function is not None:
                    await dispatch_function(event)
        finally:
            self._done_event.set()

    def post_event(self, event: events.Event, priority: Optional[int] = None) -> bool:
        if self._closing or self._closed:
            return False
        event_priority = priority if priority is not None else event.default_priority
        item = EventQueueItem(event, priority=event_priority or 0)
        self._event_queue.put_nowait(item)
        return True

    async def on_timer(self, event: events.TimerEvent) -> None:
        if event.callback is not None:
            await event.callback(event.timer)


if __name__ == "__main__":

    class Widget(EventLoop):
        pass

    widget1 = Widget()
    widget2 = Widget()

    import asyncio

    asyncio.get_event_loop().run_until_complete(widget1.run())