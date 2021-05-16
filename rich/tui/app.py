import asyncio
from contextvars import ContextVar
import logging
import signal
from typing import AsyncGenerator, ClassVar, Optional

from . import events
from .. import get_console
from ..console import Console
from .driver import Driver, CursesDriver
from .message_pump import MessagePump
from .types import Callback


log = logging.getLogger("rich")


active_app: ContextVar["App"] = ContextVar("active_app")


class App(MessagePump):
    def __init__(self, console: Console = None, screen: bool = True):
        super().__init__()
        self.console = console or get_console()
        self._screen = screen

    @classmethod
    def run(cls, console: Console = None, screen: bool = True):
        async def run_app() -> None:
            app = cls(console=console, screen=screen)
            await app.process_messages()

        asyncio.run(run_app())

    def on_keyboard_interupt(self) -> None:
        loop = asyncio.get_event_loop()
        event = events.ShutdownRequest(sender=self)
        asyncio.run_coroutine_threadsafe(self.post_message(event), loop=loop)

    async def process_messages(self) -> None:
        loop = asyncio.get_event_loop()
        driver = CursesDriver(self.console, self)
        driver.start_application_mode()
        loop.add_signal_handler(signal.SIGINT, self.on_keyboard_interupt)
        active_app.set(self)

        try:
            await super().process_messages()
            log.debug("Message loop exited")
        finally:
            loop.remove_signal_handler(signal.SIGINT)
            driver.stop_application_mode()

    async def on_shutdown_request(self, event: events.ShutdownRequest) -> None:
        log.debug("%r shutting down", self)
        await self.close_messages()


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
        async def on_key(self, event: events.Key) -> None:
            log.debug("on_key %r", event)
            if event.key == "q":
                await self.close_messages()

    MyApp.run()
