from rich.align import Align
from rich.console import Console, ConsoleOptions, RenderResult, RenderableType
from rich.pretty import Pretty
from rich.panel import Panel
from rich.repr import rich_repr, RichReprResult

from typing import ClassVar, NamedTuple, Optional, TYPE_CHECKING

from . import events
from ._context import active_app
from .message_pump import MessagePump

if TYPE_CHECKING:
    from .app import App


class WidgetDimensions(NamedTuple):
    width: int
    height: int


class WidgetPlaceholder:
    def __init__(self, widget: "Widget") -> None:
        self.widget = widget

    def __rich__(self) -> Panel:
        return Panel(
            Align.center(Pretty(self.widget), vertical="middle"), title="Widget"
        )


@rich_repr
class Widget(MessagePump):
    _count: ClassVar[int] = 0

    def __init__(self, name: Optional[str] = None) -> None:
        self.name = name or f"Widget#{self._count}"
        Widget._count += 1
        self.size = WidgetDimensions(0, 0)
        self.size_changed = False
        super().__init__()

    @property
    def app(self) -> "App":
        return active_app.get()

    @property
    def console(self) -> Console:
        return active_app.get().console

    async def refresh(self) -> None:
        self.app.refresh()
        # await self.emit(events.Refresh(self))

    def __rich_repr__(self) -> RichReprResult:
        yield "name", self.name

    def render(
        self, console: Console, options: ConsoleOptions, new_size: WidgetDimensions
    ) -> RenderableType:
        return WidgetPlaceholder(self)

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        new_size = WidgetDimensions(options.max_width, options.height or console.height)
        renderable = self.render(console, options, new_size)
        self.size = new_size
        yield renderable