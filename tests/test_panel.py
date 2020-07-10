import io
from rich.console import Console
from rich.panel import Panel

import pytest

tests = [
    Panel("Hello, World"),
    Panel("Hello, World", expand=False),
    Panel.fit("Hello, World"),
    Panel("Hello, World", width=8),
    Panel(Panel("Hello, World")),
]

expected = [
    "╭────────────────────────────────────────────────╮\n│Hello, World                                    │\n╰────────────────────────────────────────────────╯\n",
    "╭────────────╮\n│Hello, World│\n╰────────────╯\n",
    "╭────────────╮\n│Hello, World│\n╰────────────╯\n",
    "╭──────╮\n│Hello,│\n│World │\n╰──────╯\n",
    "╭────────────────────────────────────────────────╮\n│╭──────────────────────────────────────────────╮│\n││Hello, World                                  ││\n│╰──────────────────────────────────────────────╯│\n╰────────────────────────────────────────────────╯\n",
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
    assert min_width == 14
    assert max_width == 14


if __name__ == "__main__":
    expected = []
    for panel in tests:
        result = render(panel)
        print(result)
        expected.append(result)
    print("--")
    print()
    print(f"expected={repr(expected)}")
