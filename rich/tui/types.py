from typing import Callable, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from .events import Event

Callback = Callable[[], None]
# IntervalID = int


class EventTarget(Protocol):
    def post_event(self, event: "Event", priority: int = 0) -> bool:
        ...