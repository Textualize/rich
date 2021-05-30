import asyncio

import logging
import signal
from typing import Any, Dict, Set

from rich.control import Control
from rich.repr import rich_repr, RichReprResult
from rich.screen import Screen

from . import events
from ._context import active_app
from .. import get_console
from ..console import Console
from .driver import Driver, CursesDriver
from .message_pump import MessagePump
from .view import View, LayoutView

log = logging.getLogger("rich")


LayoutDefinition = Dict[str, Any]


@rich_repr
class App(MessagePump):
    view: View

    def __init__(
        self,
        console: Console = None,
        view: View = None,
        screen: bool = True,
        title: str = "Megasoma Application",
    ):
        super().__init__()
        self.console = console or get_console()
        self._screen = screen
        self.title = title
        self.view = view or LayoutView()
        self.children: Set[MessagePump] = set()

    def __rich_repr__(self) -> RichReprResult:
        yield "title", self.title

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

        await self.add(self.view)

        await self.post_message(events.Startup(sender=self))
        self.refresh()
        try:
            await super().process_messages()
        finally:
            loop.remove_signal_handler(signal.SIGINT)
            driver.stop_application_mode()

        await asyncio.gather(*(child.close_messages() for child in self.children))
        self.children.clear()

    async def add(self, child: MessagePump) -> None:
        self.children.add(child)
        asyncio.create_task(child.process_messages())
        await child.post_message(events.Created(sender=self))

    def refresh(self) -> None:
        console = self.console
        with console:
            console.print(
                Screen(Control.home(), self.view, Control.home(), application_mode=True)
            )

    async def on_startup(self, event: events.Startup) -> None:
        pass

    async def on_shutdown_request(self, event: events.ShutdownRequest) -> None:
        await self.close_messages()

    async def on_resize(self, event: events.Resize) -> None:
        await self.view.post_message(event)
        if not event.suppressed:
            self.refresh()

    async def on_mouse_move(self, event: events.MouseMove) -> None:
        await self.view.post_message(event)


if __name__ == "__main__":
    import asyncio
    from logging import FileHandler

    from .widgets.header import Header
    from .widgets.placeholder import Placeholder

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

        async def on_startup(self, event: events.Startup) -> None:
            await self.view.mount(Header(self.title), slot="header")
            await self.view.mount(Placeholder(), slot="body")
            self.refresh()

    MyApp.run()
