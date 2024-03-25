from io import StringIO

from benchmarks import snippets
from rich.color import Color, ColorSystem
from rich.console import Console
from rich.pretty import Pretty
from rich.segment import Segment
from rich.style import Style
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text


class TextSuite:
    def setup(self):
        self.console = Console(
            file=StringIO(), color_system="truecolor", legacy_windows=False
        )
        self.len_lorem_ipsum = len(snippets.LOREM_IPSUM)
        self.text = Text.from_markup(snippets.MARKUP)

    def time_wrapping(self):
        self.text.wrap(self.console, 12, overflow="fold")

    def time_indent_guides(self):
        Text(snippets.PYTHON_SNIPPET).with_indent_guides()

    def time_fit(self):
        Text(snippets.LOREM_IPSUM).fit(12)

    def time_split(self):
        self.text.split()

    def time_divide(self):
        Text(snippets.LOREM_IPSUM).divide(range(20, 100, 4))

    def time_align_center(self):
        Text(snippets.LOREM_IPSUM).align("center", width=self.len_lorem_ipsum * 3)

    def time_render(self):
        list(self.text.render(self.console))

    def time_wrapping_unicode_heavy(self):
        Text(snippets.UNICODE_HEAVY_TEXT).wrap(self.console, 12, overflow="fold")

    def time_fit_unicode_heavy(self):
        Text(snippets.UNICODE_HEAVY_TEXT).fit(12)

    def time_split_unicode_heavy(self):
        Text(snippets.UNICODE_HEAVY_TEXT).split()

    def time_divide_unicode_heavy(self):
        self.text.divide(range(20, 100, 4))

    def time_align_center_unicode_heavy(self):
        Text(snippets.UNICODE_HEAVY_TEXT).align(
            "center", width=self.len_lorem_ipsum * 3
        )

    def time_render_unicode_heavy(self):
        list(Text(snippets.UNICODE_HEAVY_TEXT).render(self.console))


class TextHotCacheSuite:
    def setup(self):
        self.console = Console(
            file=StringIO(), color_system="truecolor", legacy_windows=False
        )

    def time_wrapping_unicode_heavy_warm_cache(self):
        for _ in range(20):
            Text(snippets.UNICODE_HEAVY_TEXT).wrap(self.console, 12, overflow="fold")


class SyntaxWrappingSuite:
    def setup(self):
        self.console = Console(
            file=StringIO(), color_system="truecolor", legacy_windows=False
        )
        self.syntax = Syntax(
            code=snippets.PYTHON_SNIPPET, lexer="python", word_wrap=True
        )

    def time_text_thin_terminal_heavy_wrapping(self):
        self._print_with_width(20)

    def time_text_thin_terminal_medium_wrapping(self):
        self._print_with_width(60)

    def time_text_wide_terminal_no_wrapping(self):
        self._print_with_width(100)

    def _print_with_width(self, width):
        self.console.print(self.syntax, width)


class TableSuite:
    def time_table_no_wrapping(self):
        self._print_table(width=100)

    def time_table_heavy_wrapping(self):
        self._print_table(width=30)

    def _print_table(self, width):
        table = Table(title="Star Wars Movies")
        console = Console(
            file=StringIO(), color_system="truecolor", legacy_windows=False, width=width
        )
        table.add_column("Released", justify="right", style="cyan", no_wrap=True)
        table.add_column("Title", style="magenta")
        table.add_column("Box Office", justify="right", style="green")
        table.add_row(
            "Dec 20, 2019", "[b]Star Wars[/]: The Rise of Skywalker", "$952,110,690"
        )
        table.add_row(
            "May 25, 2018", "Solo: A [red][b]Star Wars[/] Story[/]", "$393,151,347"
        )
        table.add_row(
            "Dec 15, 2017",
            "[b red]Star Wars[/] Ep. V111: The Last Jedi",
            "$1,332,539,889",
        )
        table.add_row(
            "Dec 16, 2016", "Rogue One: A [blue]Star Wars[/] Story", "$1,332,439,889"
        )
        console.print(table)


class PrettySuite:
    def setup(self):
        self.console = Console(
            file=StringIO(), color_system="truecolor", legacy_windows=False, width=100
        )

    def time_pretty(self):
        pretty = Pretty(snippets.PYTHON_DICT)
        self.console.print(pretty)

    def time_pretty_indent_guides(self):
        pretty = Pretty(snippets.PYTHON_DICT, indent_guides=True)
        self.console.print(pretty)

    def time_pretty_justify_center(self):
        pretty = Pretty(snippets.PYTHON_DICT, justify="center")
        self.console.print(pretty)


class StyleSuite:
    def setup(self):
        self.console = Console(
            file=StringIO(), color_system="truecolor", legacy_windows=False, width=100
        )
        self.style1 = Style.parse("blue on red")
        self.style2 = Style.parse("green italic bold")

    def time_parse_ansi(self):
        Style.parse("red on blue")

    def time_parse_hex(self):
        Style.parse("#f0f0f0 on #e2e28a")

    def time_parse_mixed_complex_style(self):
        Style.parse("dim bold reverse #00ee00 on rgb(123,12,50)")

    def time_style_add(self):
        self.style1 + self.style2


class ColorSuite:
    def setup(self):
        self.console = Console(
            file=StringIO(), color_system="truecolor", legacy_windows=False, width=100
        )
        self.color = Color.parse("#0d1da0")

    def time_downgrade_to_eight_bit(self):
        self.color.downgrade(ColorSystem.EIGHT_BIT)

    def time_downgrade_to_standard(self):
        self.color.downgrade(ColorSystem.STANDARD)

    def time_downgrade_to_windows(self):
        self.color.downgrade(ColorSystem.WINDOWS)


class ColorSuiteCached:
    def setup(self):
        self.console = Console(
            file=StringIO(), color_system="truecolor", legacy_windows=False, width=100
        )
        self.color = Color.parse("#0d1da0")
        # Warm cache
        self.color.downgrade(ColorSystem.EIGHT_BIT)
        self.color.downgrade(ColorSystem.STANDARD)
        self.color.downgrade(ColorSystem.WINDOWS)

    def time_downgrade_to_eight_bit(self):
        self.color.downgrade(ColorSystem.EIGHT_BIT)

    def time_downgrade_to_standard(self):
        self.color.downgrade(ColorSystem.STANDARD)

    def time_downgrade_to_windows(self):
        self.color.downgrade(ColorSystem.WINDOWS)


class SegmentSuite:
    def setup(self):
        self.line = [
            Segment("foo"),
            Segment("bar"),
            Segment("egg"),
            Segment("Where there is a Will"),
            Segment("There is a way"),
        ] * 2

    def test_divide_complex(self):
        list(Segment.divide(self.line, [5, 10, 20, 50, 108, 110, 118]))
