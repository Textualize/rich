from time import monotonic
from typing import Optional, Callable

from asyncio import Event, wait_for, TimeoutError
import weakref

from . import events
from .types import Callback, EventTarget, MessageTarget


TimerCallback = Callable[[events.Timer], None]


class EventTargetGone(Exception):
    pass


class Timer:
    _timer_count: int = 1

    def __init__(
        self,
        event_target: EventTarget,
        interval: float,
        sender: MessageTarget,
        *,
        name: Optional[str] = None,
        callback: Optional[TimerCallback] = None,
        repeat: int = None,
    ) -> None:
        self._target_repr = repr(event_target)
        self._target = weakref.ref(event_target)
        self._interval = interval
        self.sender = sender
        self.name = f"Timer#{self._timer_count}" if name is None else name
        self._timer_count += 1
        self._callback = callback
        self._repeat = repeat
        self._stop_event = Event()

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
        count = 0
        _repeat = self._repeat
        _interval = self._interval
        _wait = self._stop_event.wait
        start = monotonic()
        while _repeat is None or count <= _repeat:
            next_timer = start + (count * _interval)
            try:
                if await wait_for(_wait(), max(0, next_timer - monotonic())):
                    break
            except TimeoutError:
                pass
            event = events.Timer(
                self.sender, timer=self, count=count, callback=self._callback
            )
            try:
                await self.target.post_message(event)
            except EventTargetGone:
                break
            count += 1
