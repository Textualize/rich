from abc import ABC, abstractmethod
import asyncio
import logging
import os
import signal
import curses
import platform
import sys
import shutil
from threading import Event, Thread
from typing import Optional, Tuple, TYPE_CHECKING

from . import events
from .types import MessageTarget

if TYPE_CHECKING:
    from ..console import Console


log = logging.getLogger("rich")

WINDOWS = platform.system() == "Windows"


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

    _MOUSE_PRESSED = [
        curses.BUTTON1_PRESSED,
        curses.BUTTON2_PRESSED,
        curses.BUTTON3_PRESSED,
        curses.BUTTON4_PRESSED,
    ]

    _MOUSE_RELEASED = [
        curses.BUTTON1_RELEASED,
        curses.BUTTON2_RELEASED,
        curses.BUTTON3_RELEASED,
        curses.BUTTON4_RELEASED,
    ]

    _MOUSE_CLICKED = [
        curses.BUTTON1_CLICKED,
        curses.BUTTON2_CLICKED,
        curses.BUTTON3_CLICKED,
        curses.BUTTON4_CLICKED,
    ]

    _MOUSE_DOUBLE_CLICKED = [
        curses.BUTTON1_DOUBLE_CLICKED,
        curses.BUTTON2_DOUBLE_CLICKED,
        curses.BUTTON3_DOUBLE_CLICKED,
        curses.BUTTON4_DOUBLE_CLICKED,
    ]

    _MOUSE = [
        (events.MousePressed, _MOUSE_PRESSED),
        (events.MouseReleased, _MOUSE_RELEASED),
        (events.MouseClicked, _MOUSE_CLICKED),
        (events.MouseDoubleClicked, _MOUSE_DOUBLE_CLICKED),
    ]

    def __init__(self, console: "Console", target: "MessageTarget") -> None:
        super().__init__(console, target)
        self._stdscr = None
        self._exit_event = Event()
        self._key_thread: Optional[Thread] = None

    def _get_terminal_size(self) -> Tuple[int, int]:
        width: Optional[int] = 80
        height: Optional[int] = 25
        if WINDOWS:  # pragma: no cover
            width, height = shutil.get_terminal_size()
        else:
            try:
                width, height = os.get_terminal_size(sys.stdin.fileno())
            except (AttributeError, ValueError, OSError):
                try:
                    width, height = os.get_terminal_size(sys.stdout.fileno())
                except (AttributeError, ValueError, OSError):
                    pass
        width = width or 80
        height = height or 25
        return width, height

    def start_application_mode(self):
        loop = asyncio.get_event_loop()

        def on_terminal_resize(signum, stack) -> None:
            terminal_size = self.console.size = self._get_terminal_size()
            width, height = terminal_size
            event = events.Resize(self._target, width, height)
            self.console.size = terminal_size
            asyncio.run_coroutine_threadsafe(
                self._target.post_message(event),
                loop=loop,
            )

        signal.signal(signal.SIGWINCH, on_terminal_resize)
        self._stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.halfdelay(1)
        curses.mousemask(curses.REPORT_MOUSE_POSITION | curses.ALL_MOUSE_EVENTS)
        # curses.mousemask(-1)

        self._stdscr.keypad(True)
        self.console.show_cursor(False)
        self.console.file.write("\033[?1003h\n")
        self._key_thread = Thread(
            target=self.run_key_thread, args=(asyncio.get_event_loop(),)
        )

        self.console.size = self._get_terminal_size()

        self._key_thread.start()

    def stop_application_mode(self):

        signal.signal(signal.SIGWINCH, signal.SIG_DFL)

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

        def send_event(event: events.Event) -> None:
            asyncio.run_coroutine_threadsafe(
                self._target.post_message(event),
                loop=loop,
            )

        while not exit_event.is_set():
            code = stdscr.getch()
            if code == -1:
                continue

            if code == curses.KEY_MOUSE:

                try:
                    _id, x, y, _z, button_state = curses.getmouse()
                except Exception:
                    log.exception("error in curses.getmouse")
                else:
                    if button_state & curses.REPORT_MOUSE_POSITION:
                        send_event(events.MouseMove(self._target, x, y))
                    alt = bool(button_state & curses.BUTTON_ALT)
                    ctrl = bool(button_state & curses.BUTTON_CTRL)
                    shift = bool(button_state & curses.BUTTON_SHIFT)
                    for event_type, masks in self._MOUSE:
                        for button, mask in enumerate(masks, 1):
                            if button_state & mask:
                                send_event(
                                    event_type(
                                        self._target,
                                        x,
                                        y,
                                        button,
                                        alt=alt,
                                        ctrl=ctrl,
                                        shift=shift,
                                    )
                                )
            else:
                send_event(events.Key(self._target, code=code))
