import io
from time import process_time

from rich.console import Console, ConsoleOptions, RenderGroup, RenderResult
from rich.markdown import Markdown
from rich.measure import Measurement
from rich.padding import Padding
from rich.panel import Panel
from rich.style import Style
from rich.table import Table
from rich.syntax import Syntax
from rich.text import Text
from rich import box


class ColorBox:
    def __init__(self, start: int = 16):
        self.start = start

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        start = self.start
        for color_start in range(start, start + 36, 6):
            text = Text()
            for color_no in range(color_start, color_start + 6):
                text.append("  ", Style(bgcolor=f"color({color_no})"))
            yield text

    def __rich_measure__(self, console: "Console", max_width: int) -> Measurement:
        return Measurement(12, 12)


def make_test_card() -> Table:
    """Get a renderable that demonstrates a number of features."""
    table = Table.grid(padding=1, pad_edge=True)
    table.title = "Rich features"
    table.add_column("Feature", no_wrap=True, justify="right", style="bold red")
    table.add_column("Demonstration")

    color_table = Table(
        box=None,
        expand=False,
        show_header=False,
        show_edge=False,
        pad_edge=False,
        padding=0,
    )

    color_table.add_row(*(ColorBox(16 + color * 36) for color in range(6)))

    table.add_row(
        "Colors",
        RenderGroup(
            "[bold yellow]256[/] colors or [bold green]16.7 million[/] colors [blue](if supported by your terminal)[/].",
            Padding(color_table, (1, 0, 0, 0)),
        ),
    )

    table.add_row(
        "Styles",
        "All ansi styles: [bold]bold[/], [dim]dim[/], [italic]italic[/italic], [underline]underline[/], [strike]strikethrough[/], [reverse]reverse[/], and even [blink]blink[/].",
    )

    lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque in metus sed sapien ultricies pretium a at justo. Maecenas luctus velit et auctor maximus. Donec faucibus vel arcu id pretium."
    lorem_table = Table.grid(padding=1, collapse_padding=True)
    lorem_table.pad_edge = False
    lorem_table.add_row(
        Text(lorem, justify="left", style="green"),
        Text(lorem, justify="center", style="yellow"),
        Text(lorem, justify="right", style="blue"),
        Text(lorem, justify="full", style="red"),
    )
    table.add_row(
        "Text",
        RenderGroup(
            Text.from_markup(
                """Word wrap text. Justify [green]left[/], [yellow]center[/], [blue]right[/] or [red]full[/].\n"""
            ),
            lorem_table,
        ),
    )

    def comparison(renderable1, renderable2) -> Table:
        table = Table(show_header=False, pad_edge=False, box=None, expand=True)
        table.add_column("1", ratio=1)
        table.add_column("2", ratio=1)
        table.add_row(renderable1, renderable2)
        return table

    table.add_row(
        "CJK support",
        Panel(
            "该库支持中文，日文和韩文文本！",
            expand=False,
            border_style="red",
            box=box.DOUBLE_EDGE,
        ),
    )

    emoji_example = (
        "Render emoji code: :+1: :apple: :ant: :bear: :baguette_bread: :bus: "
    )
    table.add_row("Emoji", comparison(Text(emoji_example), emoji_example))

    markup_example = "[bold magenta]Rich[/] supports a simple [i]bbcode[/i] like [b]markup[/b], you can use to insert [yellow]color[/] and [underline]style[/]."
    table.add_row(
        "Console markup",
        comparison(Text(markup_example), markup_example),
    )

    example_table = Table(
        title="Star Wars box office", show_header=True, header_style="bold magenta"
    )
    example_table.add_column("Date", style="dim", no_wrap=True)
    example_table.add_column("Title")
    example_table.add_column("Production Budget", justify="right", no_wrap=True)
    example_table.add_column("Box Office", justify="right", no_wrap=True)
    example_table.add_row(
        "Dec 20, 2019",
        "Star Wars: The Rise of Skywalker",
        "$275,000,000",
        "$375,126,118",
    )
    example_table.add_row(
        "May 25, 2018",
        "[red]Solo[/red]: A Star Wars Story",
        "$275,000,000",
        "$393,151,347",
    )
    example_table.add_row(
        "Dec 15, 2017",
        "Star Wars Ep. VIII: The Last Jedi",
        "$262,000,000",
        "[bold]$1,332,539,889[/bold]",
    )

    table.add_row("Tables", example_table)

    code = '''\
def iter_last(values: Iterable[T]) -> Iterable[Tuple[bool, T]]:
    """Iterate and generate a tuple with a flag for last value."""
    iter_values = iter(values)
    try:
        previous_value = next(iter_values)
    except StopIteration:
        return
    for value in iter_values:
        yield False, previous_value
        previous_value = value
    yield True, previous_value'''

    table.add_row("Syntax highlighting", Syntax(code, "python3", line_numbers=True))

    markdown_example = """\
# Markdown

Supports much of the *markdown*, __syntax__!

- Headers
- Basic formatting: **bold**, *italic*, `code`
- Block quotes
- Lists, and more...
    """
    table.add_row("Markdown", comparison(markdown_example, Markdown(markdown_example)))

    table.add_row(
        "And more", """Progress bars, styled logging handler, tracebacks, etc..."""
    )
    return table


if __name__ == "__main__":  # pragma: no cover
    console = Console(file=io.StringIO(), force_terminal=True)
    test_card = make_test_card()

    # Print once to warm cache
    console.print(test_card)
    console.file = io.StringIO()

    start = process_time()
    console.print(test_card)
    taken = round((process_time() - start) * 1000.0, 1)

    text = console.file.getvalue()
    # https://bugs.python.org/issue37871
    for line in text.splitlines():
        print(line)

    print(f"rendered in {taken}ms")
