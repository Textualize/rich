from time import time
from typing import Optional, Callable

from asyncio import Event, wait_for, TimeoutError
import weakref

from .events import TimerEvent
from .types import Callback, EventTarget


TimerCallback = Callable[["Timer"], None]


class EventTargetGone(Exception):
    pass


class Timer:
    _timer_count: int = 1

    def __init__(
        self,
        event_target: EventTarget,
        interval: float,
        *,
        name: Optional[str] = None,
        callback: Optional[TimerCallback] = None,
        repeat: int = None,
    ) -> None:
        self._target_repr = repr(event_target)
        self._target = weakref.ref(event_target)
        self._interval = interval
        self.name = f"Timer#{self._timer_count}" if name is None else name
        self._callback = callback
        self._repeat = repeat
        self._stop_event = Event()
        self.count = 0

    def __repr__(self) -> str:
        return f"Timer({self._target_repr}, {self._interval}, name={self.name!r}, repeat={self._repeat})"

    @property
    def target(self) -> EventTarget:
        target = self._target()
        if target is None:
            raise EventTargetGone()
        return target

    def stop(self) -> None:
        self._stop_event.set()

    async def run(self) -> None:
        self.count = 0
        start = time()
        while self._repeat is None or self.count <= self._repeat:
            next_timer = start + (self.count * self._interval)
            sleep_time = max(0, next_timer - time())
            try:
                if await wait_for(self._stop_event.wait(), sleep_time):
                    break
            except TimeoutError:
                pass
            event = TimerEvent(callback=self._callback, timer=self)
            try:
                self.target.post_event(event)
            except EventTargetGone:
                break
            self.count += 1
