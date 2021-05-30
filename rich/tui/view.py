from abc import ABC, abstractmethod
import logging
from typing import Optional, Tuple, TYPE_CHECKING

from rich.console import Console, ConsoleOptions, RenderResult, RenderableType
from rich.layout import Layout
from rich.region import Region
from rich.repr import rich_repr, RichReprResult

from . import events
from ._context import active_app
from .message_pump import MessagePump
from .widget import Widget
from .widgets.header import Header

if TYPE_CHECKING:
    from .app import App

log = logging.getLogger("rich")


class NoWidget(Exception):
    pass


@rich_repr
class View(ABC, MessagePump):
    @property
    def app(self) -> "App":
        return active_app.get()

    @property
    def console(self) -> Console:
        return active_app.get().console

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        return
        yield

    def __rich_repr__(self) -> RichReprResult:
        return
        yield

    async def on_resize(self, event: events.Resize) -> None:
        pass

    @abstractmethod
    async def mount(self, widget: Widget, *, slot: str = "main") -> None:
        ...


class LayoutView(View):
    layout: Layout

    def __init__(
        self,
        layout: Layout = None,
        name: str = "default",
        title: str = "Layout Application",
    ) -> None:
        self.name = name
        self.title = title
        if layout is None:
            layout = Layout()
            layout.split_column(
                Layout(name="header", size=3, ratio=0),
                Layout(name="main", ratio=1),
                Layout(name="footer", size=1, ratio=0),
            )
            layout["main"].split_row(
                Layout(name="left", size=30, visible=True),
                Layout(name="body", ratio=1),
                Layout(name="right", size=30, visible=False),
            )
        self.layout = layout
        self.mouse_over: Optional[MessagePump] = None
        super().__init__()

    def __rich_repr__(self) -> RichReprResult:
        yield "name", self.name

    def __rich__(self) -> RenderableType:
        return self.layout

    def get_widget_at(self, x: int, y: int) -> Tuple[MessagePump, Region]:
        for layout, (region, render) in self.layout.map.items():
            if region.contains(x, y):
                if isinstance(layout.renderable, MessagePump):
                    return layout.renderable, region
                else:
                    break
        raise NoWidget(f"No widget at ${x}, ${y}")

    async def on_create(self, event: events.Created) -> None:
        await self.mount(Header(self.title))

    async def mount(self, widget: Widget, *, slot: str = "main") -> None:
        self.layout[slot].update(widget)
        await self.app.add(widget)
        await widget.post_message(events.Mount(sender=self))

    async def on_startup(self, event: events.Startup) -> None:
        await self.mount(Header(self.title), slot="header")

    async def on_mouse_move(self, event: events.MouseMove) -> None:
        try:
            widget, region = self.get_widget_at(event.x, event.y)
        except NoWidget:
            if self.mouse_over is not None:
                try:
                    await self.mouse_over.post_message(events.MouseLeave(self))
                finally:
                    self.mouse_over = None
        else:
            if self.mouse_over != widget:
                try:
                    if self.mouse_over is not None:
                        await self.mouse_over.post_message(events.MouseLeave(self))
                    if widget is not None:
                        await widget.post_message(
                            events.MouseEnter(
                                self, event.x - region.x, event.y - region.x
                            )
                        )
                finally:
                    self.mouse_over = widget
            await widget.post_message(
                events.MouseMove(self, event.x - region.x, event.y - region.y)
            )
