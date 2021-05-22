from abc import ABC, abstractmethod
import asyncio
import logging
import curses
from threading import Event, Thread
from typing import Optional, TYPE_CHECKING

from . import events
from .types import MessageTarget

if TYPE_CHECKING:

    from ..console import Console


log = logging.getLogger("rich")


class Driver(ABC):
    def __init__(self, console: "Console", target: "MessageTarget") -> None:
        self.console = console
        self._target = target

    @abstractmethod
    def start_application_mode(self):
        ...

    @abstractmethod
    def stop_application_mode(self):
        ...


class CursesDriver(Driver):
    def __init__(self, console: "Console", target: "MessageTarget") -> None:
        super().__init__(console, target)
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
                key_event = events.Key(sender=self._target, code=code)
                log.debug("KEY=%r", key_event)
                asyncio.run_coroutine_threadsafe(
                    self._target.post_message(key_event),
                    loop=loop,
                )
