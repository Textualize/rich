import asyncio
from contextlib import contextmanager
from dis import dis
import logging
import signal
from typing import AsyncGenerator, ClassVar, Dict, Iterable, Optional

from .events import Event, KeyEvent, ShutdownRequestEvent
from .. import get_console
from ..console import Console
from .driver import Driver, CursesDriver
from .event_pump import EventPump
from .types import Callback
from .widget import Widget


log = logging.getLogger("rich")


# def signal_handler(sig, frame):
#     print("You pressed Ctrl+C!")
#     App.on_keyboard_interupt()


# signal.signal(signal.SIGINT, signal_handler)


class App:

    _active_app: ClassVar[Optional["App"]] = None

    def __init__(self, console: Console = None, screen: bool = True):
        self.console = console or get_console()
        self._screen = screen
        self._events: Optional[EventPump] = None

        self._mounts: Dict[Widget, List[Widget]]

    @property
    def events(self) -> EventPump:
        assert self._events is not None
        return self._events

    @classmethod
    def on_keyboard_interupt(cls) -> None:
        if App._active_app is not None:
            App._active_app.events.post(ShutdownRequestEvent())

    def mount(self, widget: Widget, parent: Optional[Widget] = None) -> None:
        pass

    async def __aiter__(self) -> AsyncGenerator[Event, None]:
        loop = asyncio.get_event_loop()
        self._events = EventPump()
        driver = CursesDriver(self.console, self.events)
        driver.start_application_mode()
        loop.add_signal_handler(signal.SIGINT, self.on_keyboard_interupt)
        App._active_app = self
        try:
            while True:
                event = await self.events.get()
                if event is None:
                    break
                yield event
        finally:
            App._active_app = None
            loop.remove_signal_handler(signal.SIGINT)
            driver.stop_application_mode()

    def run(self) -> None:
        asyncio.run(self._run())

    async def _run(self) -> None:
        async for event in self:
            log.debug(event)
            dispatch_function = getattr(self, f"on_{event.name}", None)
            if dispatch_function is not None:
                log.debug(await dispatch_function(event))
            else:
                log.debug("No handler for %r", event)

    async def on_shutdown_request(self, event: ShutdownRequestEvent) -> None:
        log.debug("%r shutting down", self)
        self.events.close()

    # def add_interval(self, delay: float, callback: Callback = None) -> IntervalID:
    #     pass

    # def add_timer(self, period: float, callback: Callback = None) -> TimerID:
    #     pass


if __name__ == "__main__":
    import asyncio
    from logging import FileHandler

    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[FileHandler("richtui.log")],
    )

    class MyApp(App):
        async def on_key(self, event: KeyEvent) -> None:
            if event.key == ord("q"):
                raise ValueError()

    app = MyApp()
    app.run()