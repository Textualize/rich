"""
Demonstrates emoji, grapheme clusters, complex language text
"""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

def main():
    console = Console()

    table = Table(title="Emoji & Grapheme Clusters")
    table.add_column("Type", style="cyan")
    table.add_column("Example", justify="center")
    table.add_column("Codepoints", style="dim")
    # all emojis are written with \uEscapes because editors also have a hard time
    table.add_row(
        "ZWJ Family",
        "\U0001F468\u200D\U0001F469\u200D\U0001F467\u200D\U0001F466",
        "4 emoji + 3 ZWJ",
    )
    table.add_row("Skin Tone", "\U0001F44B\U0001F3FD", "wave + modifier")
    table.add_row(
        "Flags",
        "\U0001F1E8\U0001F1E6 \U0001F1EC\U0001F1E7 \U0001F1EF\U0001F1F5",
        "regional indicators",
    )
    table.add_row(
        "VS16 Emoji", "\u2764\uFE0F \u2728 \u267B\uFE0F \u2615", "with variation selectors"
    )
    table.add_row(
        "Keycap", "1\uFE0F\u20E3 2\uFE0F\u20E3 #\uFE0F\u20E3", "digit + VS16 + combining"
    )
    table.add_row("Combining", "e\u0301 n\u0303 u\u0308", "base + combining accent")
    table.add_row("CJK", "\u5bcc\u58eb\u5c71 \u6771\u4eac", "wide characters")
    table.add_row(
        "Standalone Skin Tone", "\U0001F3FB \U0001F3FD \U0001F3FF", "modifiers without base"
    )
    table.add_row(
        "Standalone Regional", "\U0001F1E8 \U0001F1E6", "unpaired indicators"
    )


    console.print(table, justify="center")
    console.print()

    # Complex scripts with combining marks, zero-width characters, or stacking
    # (first lines from UDHR Article 1) https://github.com/eric-muller/udhr
    text = (
        "[bold]Complex Scripts (UDHR Article 1)[/]\n\n"
        # Arabic: RTL, combining vowel marks (harakat)
        "[cyan]Arabic:[/]    \u064A\u0648\u0644\u062F \u062C\u0645\u064A\u0639"
        " \u0627\u0644\u0646\u0627\u0633 \u0623\u062D\u0631\u0627\u0631\u0627\n"
        # Hindi (Devanagari): combining vowel signs, virama conjuncts
        "[cyan]Hindi:[/]     \u0938\u092D\u0940 \u092E\u0928\u0941\u0937\u094D\u092F\u094B\u0902"
        " \u0915\u094B \u0917\u094C\u0930\u0935 \u0914\u0930"
        " \u0905\u0927\u093F\u0915\u093E\u0930\u094B\u0902\n"
        # Thai: above/below combining vowels and tone marks
        "[cyan]Thai:[/]      \u0E21\u0E19\u0E38\u0E29\u0E22\u0E4C\u0E17\u0E31\u0E49\u0E07"
        "\u0E2B\u0E25\u0E32\u0E22\u0E40\u0E01\u0E34\u0E14\u0E21\u0E32\n"
        # Tibetan: stacked consonants, subjoined letters
        "[cyan]Tibetan:[/]   \u0F66\u0F90\u0FB1\u0F7A\u0F0B\u0F56\u0F7C\u0F0B"
        "\u0F58\u0F72\u0F0B\u0F62\u0F72\u0F42\u0F66\u0F0B\u0F40\u0F72\n"
        # Sinhala: round/curvy script, virama conjuncts
        "[cyan]Sinhala:[/]   \u0DC3\u0DD2\u0DBA\u0DBD\u0DD4 \u0DB8\u0DB1\u0DD4"
        "\u0DC2\u0DCA\u200D\u0DBA\u0DBA\u0DB1\u0DCA\n"
        # Hebrew: RTL, combining niqqud vowel points
        "[cyan]Hebrew:[/]    \u05DB\u05BC\u05B8\u05DC\u05BE\u05D1\u05B0\u05E0\u05B5\u05D9"
        " \u05D4\u05B8\u05D0\u05B8\u05D3\u05B8\u05DD\n"
        # French: decomposed combining accents (ê é)
        "[cyan]French:[/]    Tous les e\u0302tres humains naissent e\u0301gaux\n"
        # Polish: combining ogonek and acute (ą ę ó)
        "[cyan]Polish:[/]    Wszyscy ludzie rodza\u0328 sie\u0328 ro\u0301wni\n"
        # Yoruba: combining tone marks (à é í ò)
        "[cyan]Yoruba:[/]    Gbogbo e\u0300ni\u0301ya\u0301n la\u0301 a bi ni\u0301"
    )
    console.print(Panel(text, title="\U0001F30D Languages", border_style="blue"))


if __name__ == "__main__":
    main()
