import io

import pytest

from rich.console import Console
from rich.crosshairs import Crosshairs


# Crosshairs edge cases in a 3 x 3 console, cross centre starts at the top left,
# moves clockwise around the output region.
CROSSHAIRS_DIAGRAMS = """
0,0
┌──
│  
│  

1,0
─┬─
 │ 
 │ 

2,0
──┐
  │
  │

2,1
  │
──┤
  │

2,2
  │
  │
──┘

1,2
 │ 
 │ 
─┴─

0,2
│  
│  
└──

0,1
│  
├──
│  
""".strip(
    "\n"
).split(
    "\n\n"
)


def test_crosshairs():
    console = Console(width=4, height=3, legacy_windows=False)
    console.begin_capture()
    console.print(Crosshairs(1, 1))
    assert console.end_capture() == " │  \n─┼──\n │  \n"


@pytest.mark.parametrize("diagram", CROSSHAIRS_DIAGRAMS)
def test_crosshairs_edge_cases(diagram):
    """Test crosshairs creation when cross centre is flush with edges or corners."""

    console = Console(width=3, height=3, legacy_windows=False)
    # Parse the diagram to build crosshairs arguments and expected output.
    coords, expected_output = diagram.split("\n", maxsplit=1)
    expected_output += "\n"
    x, y = map(int, coords.split(","))
    # ... and actually run the test.
    console.begin_capture()
    console.print(Crosshairs(x, y))
    assert console.end_capture() == expected_output


def test_crosshairs_styling():
    console = Console(
        file=io.StringIO(),
        force_terminal=True,
        width=3,
        height=3,
        color_system="truecolor",
        legacy_windows=False,
    )
    console.print(Crosshairs(1, 1, "black on red"))
    expected = "\x1b[30;41m │ \x1b[0m\n\x1b[30;41m─┼─\x1b[0m\n\x1b[30;41m │ \x1b[0m\n"
    result = console.file.getvalue()
    assert result == expected
