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

header = layout.split(name="header", size=1)
body = layout.split(ratio=1, direction="horizontal")
footer = layout.split(size=10, name="footer")

side = body.split(name="side")
body.split(name="body", ratio=2)

side.split()
side.split()

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
        return Text(
            datetime.now().ctime(),
            style="bold magenta",
            justify="center"
        )


layout["header"].update(Clock())

with Live(layout, screen=True) as live:
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        pass
