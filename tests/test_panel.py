import io

import pytest

from rich.console import Console
from rich.panel import Panel
from rich.segment import Segment
from rich.style import Style

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
    return console.file.getvalue()


@pytest.mark.parametrize("panel,expected", zip(tests, expected))
def test_render_panel(panel, expected):
    assert render(panel) == expected


def test_console_width():
    console = Console(file=io.StringIO(), width=50, legacy_windows=False)
    panel = Panel("Hello, World", expand=False)
    min_width, max_width = panel.__rich_measure__(console, console.options)
    assert min_width == 16
    assert max_width == 16


def test_fixed_width():
    console = Console(file=io.StringIO(), width=50, legacy_windows=False)
    panel = Panel("Hello World", width=20)
    min_width, max_width = panel.__rich_measure__(console, console.options)
    assert min_width == 20
    assert max_width == 20


def test_render_size():
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


if __name__ == "__main__":
    expected = []
    for panel in tests:
        result = render(panel)
        print(result)
        expected.append(result)
    print("--")
    print()
    print(f"expected={repr(expected)}")
