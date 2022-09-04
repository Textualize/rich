"""
A simulation of Rich console logging.
"""

import time

from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.style import Style
from rich.theme import Theme


class RequestHighlighter(RegexHighlighter):
    base_style = "req."
    highlights = [
        r"^(?P<protocol>\w+) (?P<method>\w+) (?P<path>\S+) (?P<result>\w+) (?P<stats>\[.+\])$",
        r"\/(?P<filename>\w+\..{3,4})",
    ]


theme = Theme(
    {
        "req.protocol": Style.parse("dim bold green"),
        "req.method": Style.parse("bold cyan"),
        "req.path": Style.parse("magenta"),
        "req.filename": Style.parse("bright_magenta"),
        "req.result": Style.parse("yellow"),
        "req.stats": Style.parse("dim"),
    }
)
console = Console(theme=theme)

console.log("Server starting...")
console.log("Serving on http://127.0.0.1:8000")

time.sleep(1)

request_highlighter = RequestHighlighter()

console.log(
    request_highlighter("HTTP GET /foo/bar/baz/egg.html 200 [0.57, 127.0.0.1:59076]"),
)

console.log(
    request_highlighter(
        "HTTP GET /foo/bar/baz/background.jpg 200 [0.57, 127.0.0.1:59076]"
    ),
)


time.sleep(1)


def test_locals():
    foo = (1, 2, 3)
    movies = ["Deadpool", "Rise of the Skywalker"]
    console = Console()

    console.log(
        "[b]JSON[/b] RPC [i]batch[/i]",
        [
            {"jsonrpc": "2.0", "method": "sum", "params": [1, 2, 4], "id": "1"},
            {"jsonrpc": "2.0", "method": "notify_hello", "params": [7]},
            {"jsonrpc": "2.0", "method": "subtract", "params": [42, 23], "id": "2"},
            {"foo": "boo"},
            {
                "jsonrpc": "2.0",
                "method": "foo.get",
                "params": {"name": "myself", "enable": False, "grommits": None},
                "id": "5",
            },
            {"jsonrpc": "2.0", "method": "get_data", "id": "9"},
        ],
        log_locals=True,
    )


test_locals()
