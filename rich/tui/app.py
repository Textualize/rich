import asyncio
from contextvars import ContextVar
import logging
import signal
from typing import Any, Dict


from . import events
from .. import get_console
from ..console import Console
from .driver import Driver, CursesDriver
from .message_pump import MessagePump


log = logging.getLogger("rich")


active_app: ContextVar["App"] = ContextVar("active_app")


LayoutDefinition = Dict[str, Any]


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

        await self.post_message(events.Startup(sender=self))

        try:
            await super().process_messages()
        finally:
            loop.remove_signal_handler(signal.SIGINT)
            driver.stop_application_mode()

    def set_layout(self, layout: LayoutDefinition) -> None:
        pass

    async def on_startup(self, event: events.Startup) -> None:
        pass

    async def on_shutdown_request(self, event: events.ShutdownRequest) -> None:
        await self.close_messages()


if __name__ == "__main__":
    import asyncio
    from logging import FileHandler
    from rich.layout import Layout
    from rich.panel import Panel

    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[FileHandler("richtui.log")],
    )

    layout = {
        "split": "column",
        "children": [
            {"name": "title", "height": 3},
            {
                "name": "main",
                "children": [
                    {"name": "left", "ratio": 1, "visible": False},
                    {"name": "right", "ratio": 2},
                ],
            },
            {"name": "footer", "height": "1"},
        ],
    }

    layout = """
        <column>
            <slot name="title" height="3"/>
            <row name="main">
                <slot name="left" ratio="1" visible="false"/>
                <slot name="right" ratio="2"/>
            </row>
            <slot name="footer" height="1"/>
        </column>
    """

    class MyApp(App):
        async def on_key(self, event: events.Key) -> None:
            log.debug("on_key %r", event)
            if event.key == "q":
                await self.close_messages()

        async def on_startup(self) -> None:

            self.set_layout(
                {
                    "split": "column",
                    "children": [
                        {"name": "header", "height": 3, "mount": TitleBar()},
                        {
                            "name": "main",
                            "children": [
                                {"name": "left", "ratio": 1, "visible": False},
                                {"name": "right", "ratio": 2},
                            ],
                        },
                        {"name": "footer", "height": 1},
                    ],
                }
            )
            # self.mount(TitleBar(clock=True), slot="header")

    MyApp.run()
