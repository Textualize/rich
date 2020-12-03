import io
from rich.console import Console
from rich.measure import Measurement
from rich.panel import Panel

import pytest

tests = [
    Panel("Hello, World", padding=0),
    Panel("Hello, World", expand=False, padding=0),
    Panel.fit("Hello, World", padding=0),
    Panel("Hello, World", width=8, padding=0),
    Panel(Panel("Hello, World", padding=0), padding=0),
    Panel("Hello, World", title="FOO", padding=0),
]

expected = [
    "╭────────────────────────────────────────────────╮\n│Hello, World                                    │\n╰────────────────────────────────────────────────╯\n",
    "╭────────────╮\n│Hello, World│\n╰────────────╯\n",
    "╭────────────╮\n│Hello, World│\n╰────────────╯\n",
    "╭──────╮\n│Hello,│\n│World │\n╰──────╯\n",
    "╭────────────────────────────────────────────────╮\n│╭──────────────────────────────────────────────╮│\n││Hello, World                                  ││\n│╰──────────────────────────────────────────────╯│\n╰────────────────────────────────────────────────╯\n",
    "╭───────────────────── FOO ──────────────────────╮\n│Hello, World                                    │\n╰────────────────────────────────────────────────╯\n",
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
    min_width, max_width = panel.__rich_measure__(console, 50)
    assert min_width == 16
    assert max_width == 16


def test_fixed_width():
    console = Console(file=io.StringIO(), width=50, legacy_windows=False)
    panel = Panel("Hello World", width=20)
    min_width, max_width = panel.__rich_measure__(console, 100)
    assert min_width == 20
    assert max_width == 20


if __name__ == "__main__":
    expected = []
    for panel in tests:
        result = render(panel)
        print(result)
        expected.append(result)
    print("--")
    print()
    print(f"expected={repr(expected)}")
