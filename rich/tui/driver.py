from abc import ABC, abstractmethod
import asyncio
import curses
from functools import partial
from threading import Event, Thread
from typing import Optional, TYPE_CHECKING

from .events import KeyEvent

if TYPE_CHECKING:
    from .event_pump import EventPump
    from ..console import Console


class Driver(ABC):
    def __init__(self, console: "Console", events: "EventPump") -> None:
        self.console = console
        self.events = events

    @abstractmethod
    def start_application_mode(self):
        ...

    @abstractmethod
    def stop_application_mode(self):
        ...


class CursesDriver(Driver):
    def __init__(self, console: "Console", events: "EventPump") -> None:
        super().__init__(console, events)
        self._stdscr = None
        self._exit_event = Event()

        self._key_thread: Optional[Thread] = None

    def start_application_mode(self):
        self._stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.halfdelay(1)
        self._stdscr.keypad(True)
        self.console.show_cursor(False)
        self._key_thread = Thread(
            target=self.run_key_thread, args=(asyncio.get_event_loop(),)
        )
        self._key_thread.start()

    def stop_application_mode(self):
        self._exit_event.set()
        self._key_thread.join()
        curses.nocbreak()
        self._stdscr.keypad(False)
        curses.echo()
        curses.endwin()
        self.console.show_cursor(True)

    def run_key_thread(self, loop) -> None:
        stdscr = self._stdscr
        assert stdscr is not None
        exit_event = self._exit_event
        while not exit_event.is_set():
            code = stdscr.getch()
            if code != -1:
                loop.call_soon_threadsafe(
                    partial(self.events.post, KeyEvent(code=code))
                )
