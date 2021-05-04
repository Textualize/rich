from typing import TYPE_CHECKING

from . import events

if TYPE_CHECKING:
    from .app import App


class Widget:
    async def run(self, events: events.EventBus) -> None:
        async for event in events:
            dispatch_function = getattr(self, f"on_{event.name}", None)
            if dispatch_function is not None:
                await dispatch_function(event)

    def focus(self):
        pass

    def blur(self):
        pass