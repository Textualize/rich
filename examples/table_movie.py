"""Same as the table_movie.py but uses Live to update"""
import time
from contextlib import contextmanager

from rich import box
from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.text import Text

TABLE_DATA = [
    [
        "May 25, 1977",
        "Star Wars Ep. [b]IV[/]: [i]A New Hope",
        "$11,000,000",
        "$1,554,475",
        "$775,398,007",
    ],
    [
        "May 21, 1980",
        "Star Wars Ep. [b]V[/]: [i]The Empire Strikes Back",
        "$23,000,000",
        "$4,910,483",
        "$547,969,004",
    ],
    [
        "May 25, 1983",
        "Star Wars Ep. [b]VI[/b]: [i]Return of the Jedi",
        "$32,500,000",
        "$23,019,618",
        "$475,106,177",
    ],
    [
        "May 19, 1999",
        "Star Wars Ep. [b]I[/b]: [i]The phantom Menace",
        "$115,000,000",
        "$64,810,870",
        "$1,027,044,677",
    ],
    [
        "May 16, 2002",
        "Star Wars Ep. [b]II[/b]: [i]Attack of the Clones",
        "$115,000,000",
        "$80,027,814",
        "$656,695,615",
    ],
    [
        "May 19, 2005",
        "Star Wars Ep. [b]III[/b]: [i]Revenge of the Sith",
        "$115,500,000",
        "$380,270,577",
        "$848,998,877",
    ],
]

console = Console()

BEAT_TIME = 0.04


@contextmanager
def beat(length: int = 1) -> None:
    yield
    time.sleep(length * BEAT_TIME)


table = Table(show_footer=False)
table_centered = Align.center(table)

console.clear()

with Live(table_centered, console=console, screen=False, refresh_per_second=20):
    with beat(10):
        table.add_column("Release Date", no_wrap=True)

    with beat(10):
        table.add_column("Title", Text.from_markup("[b]Total", justify="right"))

    with beat(10):
        table.add_column("Budget", "[u]$412,000,000", no_wrap=True)

    with beat(10):
        table.add_column("Opening Weekend", "[u]$577,703,455", no_wrap=True)

    with beat(10):
        table.add_column("Box Office", "[u]$4,331,212,357", no_wrap=True)

    with beat(10):
        table.title = "Star Wars Box Office"

    with beat(10):
        table.title = (
            "[not italic]:popcorn:[/] Star Wars Box Office [not italic]:popcorn:[/]"
        )

    with beat(10):
        table.caption = "Made with Rich"

    with beat(10):
        table.caption = "Made with [b]Rich[/b]"

    with beat(10):
        table.caption = "Made with [b magenta not dim]Rich[/]"

    for row in TABLE_DATA:
        with beat(10):
            table.add_row(*row)

    with beat(10):
        table.show_footer = True

    table_width = console.measure(table).maximum

    with beat(10):
        table.columns[2].justify = "right"

    with beat(10):
        table.columns[3].justify = "right"

    with beat(10):
        table.columns[4].justify = "right"

    with beat(10):
        table.columns[2].header_style = "bold red"

    with beat(10):
        table.columns[3].header_style = "bold green"

    with beat(10):
        table.columns[4].header_style = "bold blue"

    with beat(10):
        table.columns[2].style = "red"

    with beat(10):
        table.columns[3].style = "green"

    with beat(10):
        table.columns[4].style = "blue"

    with beat(10):
        table.columns[0].style = "cyan"
        table.columns[0].header_style = "bold cyan"

    with beat(10):
        table.columns[1].style = "magenta"
        table.columns[1].header_style = "bold magenta"

    with beat(10):
        table.columns[2].footer_style = "bright_red"

    with beat(10):
        table.columns[3].footer_style = "bright_green"

    with beat(10):
        table.columns[4].footer_style = "bright_blue"

    with beat(10):
        table.row_styles = ["none", "dim"]

    with beat(10):
        table.border_style = "bright_yellow"

    for box_style in [
        box.SQUARE,
        box.MINIMAL,
        box.SIMPLE,
        box.SIMPLE_HEAD,
    ]:
        with beat(10):
            table.box = box_style

    with beat(10):
        table.pad_edge = False

    original_width = console.measure(table).maximum

    for width in range(original_width, console.width, 2):
        with beat(1):
            table.width = width

    for width in range(console.width, original_width, -2):
        with beat(1):
            table.width = width

    for width in range(original_width, 90, -2):
        with beat(1):
            table.width = width

    for width in range(90, original_width + 1, 2):
        with beat(1):
            table.width = width

    with beat(2):
        table.width = None
