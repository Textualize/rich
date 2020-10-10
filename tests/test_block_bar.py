from rich.block_bar import BlockBar

from .render import render


expected = [
    "\x1b[39;49m     ▐█████████████████████████                   \x1b[0m",
    "\x1b[39;49m      ██████████████████████                      \x1b[0m",
    "\x1b[39;49m                                                  \x1b[0m",
]


def test_repr():
    bar = BlockBar(size=100, begin=11, end=62, width=50)
    assert repr(bar) == "<BlockBar 11..62 of 100>"


def test_render():
    bar = BlockBar(size=100, begin=11, end=62, width=50)
    bar_render = render(bar)
    assert bar_render == expected[0]
    bar = BlockBar(size=100, begin=12, end=57, width=50)
    bar_render = render(bar)
    assert bar_render == expected[1]
    # begin after end
    bar = BlockBar(size=100, begin=60, end=40, width=50)
    bar_render = render(bar)
    assert bar_render == expected[2]


def test_measure():
    bar = BlockBar(size=100, begin=11, end=62)
    measurement = bar.__rich_measure__(None, 120)
    assert measurement.minimum == 4
    assert measurement.maximum == 120


def test_zero_total():
    # Shouldn't throw zero division error
    bar = BlockBar(size=0, begin=0, end=0)
    render(bar)


if __name__ == "__main__":
    bar = BlockBar(size=100, begin=11, end=62, width=50)
    bar_render = render(bar)
    print(repr(bar_render))
    bar = BlockBar(size=100, begin=12, end=57, width=50)
    bar_render = render(bar)
    print(repr(bar_render))
    bar = BlockBar(size=100, begin=60, end=40, width=50)
    bar_render = render(bar)
    print(repr(bar_render))
