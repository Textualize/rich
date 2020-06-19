import logging
from datetime import datetime
from logging import Handler, LogRecord
from pathlib import Path
from typing import ClassVar, List, Optional, Type

from rich._log_render import LogRender
from rich.console import Console
from rich.highlighter import Highlighter, ReprHighlighter
from rich.text import Text
from . import get_console


class RichHandler(Handler):
    """A logging handler that renders output with Rich. The time / level / message and file are displayed in columns.
    The level is color coded, and the message is syntax highlighted.
        
    Args:
        level (int, optional): Log level. Defaults to logging.NOTSET.
        console (:class:`~rich.console.Console`, optional): Optional console instance to write logs.
            Default will create a new console writing to stderr.
        enable_link_path (bool, optional): Enable terminal link of path column to file. Defaults to True.
  
    """

    KEYWORDS: ClassVar[Optional[List[str]]] = [
        "GET",
        "POST",
        "HEAD",
        "PUT",
        "DELETE",
        "OPTIONS",
        "TRACE",
        "PATCH",
    ]
    HIGHLIGHTER_CLASS: ClassVar[Type[Highlighter]] = ReprHighlighter

    def __init__(
        self,
        level: int = logging.NOTSET,
        console: Console = None,
        *,
        enable_link_path: bool = True,
    ) -> None:
        super().__init__(level=level)
        self.console = console or get_console()
        self.highlighter = self.HIGHLIGHTER_CLASS()
        self._log_render = LogRender(show_level=True)
        self.enable_link_path = enable_link_path

    def emit(self, record: LogRecord) -> None:
        """Invoked by logging."""
        path = Path(record.pathname).name
        log_style = f"logging.level.{record.levelname.lower()}"
        message = self.format(record)
        time_format = None if self.formatter is None else self.formatter.datefmt
        log_time = datetime.fromtimestamp(record.created)

        level = Text()
        level.append(record.levelname, log_style)
        message_text = Text(message)
        if self.highlighter:
            message_text = self.highlighter(message_text)
        if self.KEYWORDS:
            message_text.highlight_words(self.KEYWORDS, "logging.keyword")

        self.console.print(
            self._log_render(
                self.console,
                [message_text],
                log_time=log_time,
                time_format=time_format,
                level=level,
                path=path,
                line_no=record.lineno,
                link_path=record.pathname if self.enable_link_path else None,
            )
        )


if __name__ == "__main__":  # pragma: no cover
    from time import sleep

    FORMAT = "%(message)s"
    # FORMAT = "%(asctime)-15s - %(level) - %(message)s"
    logging.basicConfig(
        level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )
    log = logging.getLogger("rich")

    log.info("Server starting...")
    log.info("Listening on http://127.0.0.1:8080")
    sleep(1)

    log.info("GET /index.html 200 1298")
    log.info("GET /imgs/backgrounds/back1.jpg 200 54386")
    log.info("GET /css/styles.css 200 54386")
    log.warning("GET /favicon.ico 404 242")
    sleep(1)

    log.debug(
        "JSONRPC request\n--> %r\n<-- %r",
        {
            "version": "1.1",
            "method": "confirmFruitPurchase",
            "params": [["apple", "orange", "mangoes", "pomelo"], 1.123],
            "id": "194521489",
        },
        {"version": "1.1", "result": True, "error": None, "id": "194521489"},
    )
    log.error("Unable to find 'pomelo' in database!")
    log.info("POST /jsonrpc/ 200 65532")
    log.info("POST /admin/ 401 42234")
    log.warning("password was rejected for admin site.")
    try:
        1 / 0
    except:
        log.exception("An error of some kind occurred!")
    sleep(1)
    log.critical("Out of memory!")
    log.info("Server exited with code=-1")
