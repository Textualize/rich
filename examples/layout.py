"""

Demonstrates a dynamic Layout

"""

from datetime import datetime
from time import sleep

from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.text import Text

console = Console()
layout = Layout()

layout.split(
    Layout(name="header", size=1),
    Layout(ratio=1, name="main"),
    Layout(size=10, name="footer"),
)

layout["main"].split_row(Layout(name="side"), Layout(name="body", ratio=2))

layout["side"].split(Layout(), Layout())

layout["body"].update(
    Align.center(
        Text(
            """This is a demonstration of rich.Layout\n\nHit Ctrl+C to exit""",
            justify="center",
        ),
        vertical="middle",
    )
)


class Clock:
    """Renders the time in the center of the screen."""

    def __rich__(self) -> Text:
        return Text(datetime.now().ctime(), style="bold magenta", justify="center")


layout["header"].update(Clock())

with Live(layout, screen=True, redirect_stderr=False) as live:
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        pass
