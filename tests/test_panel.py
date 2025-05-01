import io

import pytest

from rich.console import Console
from rich.panel import Panel
from rich.segment import Segment
from rich.style import Style
from rich.text import Text

tests = [
    Panel("Hello, World", padding=0),
    Panel("Hello, World", expand=False, padding=0),
    Panel.fit("Hello, World", padding=0),
    Panel("Hello, World", width=8, padding=0),
    Panel(Panel("Hello, World", padding=0), padding=0),
    Panel("Hello, World", title="FOO", padding=0),
    Panel("Hello, World", subtitle="FOO", padding=0),
]

expected = [
    "╭────────────────────────────────────────────────╮\n│Hello, World                                    │\n╰────────────────────────────────────────────────╯\n",
    "╭────────────╮\n│Hello, World│\n╰────────────╯\n",
    "╭────────────╮\n│Hello, World│\n╰────────────╯\n",
    "╭──────╮\n│Hello,│\n│World │\n╰──────╯\n",
    "╭────────────────────────────────────────────────╮\n│╭──────────────────────────────────────────────╮│\n││Hello, World                                  ││\n│╰──────────────────────────────────────────────╯│\n╰────────────────────────────────────────────────╯\n",
    "╭───────────────────── FOO ──────────────────────╮\n│Hello, World                                    │\n╰────────────────────────────────────────────────╯\n",
    "╭────────────────────────────────────────────────╮\n│Hello, World                                    │\n╰───────────────────── FOO ──────────────────────╯\n",
]


def render(panel, width=50) -> str:
    console = Console(file=io.StringIO(), width=50, legacy_windows=False)
    console.print(panel)
    result = console.file.getvalue()
    print(result)
    return result


@pytest.mark.parametrize("panel,expected", zip(tests, expected))
def test_render_panel(panel, expected) -> None:
    assert render(panel) == expected


def test_console_width() -> None:
    console = Console(file=io.StringIO(), width=50, legacy_windows=False)
    panel = Panel("Hello, World", expand=False)
    min_width, max_width = panel.__rich_measure__(console, console.options)
    assert min_width == 16
    assert max_width == 16


def test_fixed_width() -> None:
    console = Console(file=io.StringIO(), width=50, legacy_windows=False)
    panel = Panel("Hello World", width=20)
    min_width, max_width = panel.__rich_measure__(console, console.options)
    assert min_width == 20
    assert max_width == 20


def test_render_size() -> None:
    console = Console(width=63, height=46, legacy_windows=False)
    options = console.options.update_dimensions(80, 4)
    lines = console.render_lines(Panel("foo", title="Hello"), options=options)
    print(repr(lines))
    expected = [
        [
            Segment("╭─", Style()),
            Segment(
                "────────────────────────────────── Hello ───────────────────────────────────"
            ),
            Segment("─╮", Style()),
        ],
        [
            Segment("│", Style()),
            Segment(" ", Style()),
            Segment("foo"),
            Segment(
                "                                                                         ",
                Style(),
            ),
            Segment(" ", Style()),
            Segment("│", Style()),
        ],
        [
            Segment("│", Style()),
            Segment(" ", Style()),
            Segment(
                "                                                                            ",
                Style(),
            ),
            Segment(" ", Style()),
            Segment("│", Style()),
        ],
        [
            Segment(
                "╰──────────────────────────────────────────────────────────────────────────────╯",
                Style(),
            )
        ],
    ]
    assert lines == expected


def test_title_text() -> None:
    panel = Panel(
        "Hello, World",
        title=Text("title", style="red"),
        subtitle=Text("subtitle", style="magenta bold"),
    )
    console = Console(
        file=io.StringIO(),
        width=50,
        height=20,
        legacy_windows=False,
        force_terminal=True,
        color_system="truecolor",
    )
    console.print(panel)

    result = console.file.getvalue()
    print(repr(result))
    expected = "╭────────────────────\x1b[31m title \x1b[0m─────────────────────╮\n│ Hello, World                                   │\n╰───────────────────\x1b[1;35m subtitle \x1b[0m───────────────────╯\n"
    assert result == expected


def test_title_text_with_border_color() -> None:
    """Regression test for https://github.com/Textualize/rich/issues/2745"""
    panel = Panel(
        "Hello, World",
        border_style="blue",
        title=Text("title", style="red"),
        subtitle=Text("subtitle", style="magenta bold"),
    )
    console = Console(
        file=io.StringIO(),
        width=50,
        height=20,
        legacy_windows=False,
        force_terminal=True,
        color_system="truecolor",
    )
    console.print(panel)

    result = console.file.getvalue()
    print(repr(result))
    expected = "\x1b[34m╭─\x1b[0m\x1b[34m───────────────────\x1b[0m\x1b[31m title \x1b[0m\x1b[34m────────────────────\x1b[0m\x1b[34m─╮\x1b[0m\n\x1b[34m│\x1b[0m Hello, World                                   \x1b[34m│\x1b[0m\n\x1b[34m╰─\x1b[0m\x1b[34m──────────────────\x1b[0m\x1b[1;35m subtitle \x1b[0m\x1b[34m──────────────────\x1b[0m\x1b[34m─╯\x1b[0m\n"
    assert result == expected


def test_title_text_with_panel_background() -> None:
    """Regression test for https://github.com/Textualize/rich/issues/3569"""
    panel = Panel(
        "Hello, World",
        style="on blue",
        title=Text("title", style="red"),
        subtitle=Text("subtitle", style="magenta bold"),
    )
    console = Console(
        file=io.StringIO(),
        width=50,
        height=20,
        legacy_windows=False,
        force_terminal=True,
        color_system="truecolor",
    )
    console.print(panel)

    result = console.file.getvalue()
    print(repr(result))
    expected = "\x1b[44m╭─\x1b[0m\x1b[44m───────────────────\x1b[0m\x1b[31;44m title \x1b[0m\x1b[44m────────────────────\x1b[0m\x1b[44m─╮\x1b[0m\n\x1b[44m│\x1b[0m\x1b[44m \x1b[0m\x1b[44mHello, World\x1b[0m\x1b[44m                                  \x1b[0m\x1b[44m \x1b[0m\x1b[44m│\x1b[0m\n\x1b[44m╰─\x1b[0m\x1b[44m──────────────────\x1b[0m\x1b[1;35;44m subtitle \x1b[0m\x1b[44m──────────────────\x1b[0m\x1b[44m─╯\x1b[0m\n"
    assert result == expected


if __name__ == "__main__":
    expected = []
    for panel in tests:
        result = render(panel)
        print(result)
        expected.append(result)
    print("--")
    print()
    print(f"expected={repr(expected)}")
