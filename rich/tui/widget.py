from .app import App
from . import events
from .event_pump import EventPump


class Widget:
    def __init__(self, app: App) -> None:
        self.app = app
        self.events = EventPump()

    async def mount(self, widget: "Widget") -> None:
        self.events.parent = self.events
        widget.events.post(events.MountEvent())

    async def unmount(self) -> None:
        self.events.post(events.UnmountEvent())
        self.events.parent = None

    async def run(self) -> None:
        async for event in self.events:
            dispatch_function = getattr(self, f"on_{event.name}", None)
            if dispatch_function is not None:
                await dispatch_function(event)