from audioop import cross
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
""".strip().split("\n\n")


def test_crosshairs():
    console = Console(width=4, height=3)
    console.begin_capture()
    console.print(Crosshairs(1, 1))
    assert console.end_capture() == " │  \n─┼──\n │  "


def test_crosshairs_edge_cases():
    console = Console(width=3, height=3)
    for diagram in CROSSHAIRS_DIAGRAMS:
        # Parse the diagram,
        coords, output = diagram.split("\n", maxsplit=1)
        x, y = map(int, coords.split(","))

        # and feed it to the test.
        console.begin_capture()
        console.print(Crosshairs(x, y))
        assert console.end_capture() == output
