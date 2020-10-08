from rich.bar import BlockBar

from .render import render


def test_init():
    bar = BlockBar(completed=50)
    repr(bar)
    assert bar.percentage_completed == 50.0


def test_update():
    bar = BlockBar()
    assert bar.completed == 0
    assert bar.total == 100
    bar.update(10, 20)
    assert bar.completed == 10
    assert bar.total == 20
    assert bar.percentage_completed == 50
    bar.update(100)
    assert bar.percentage_completed == 100


expected = [
    "\x1b[38;2;249;38;114m█████\x1b[0m\x1b[38;2;249;38;114m▌\x1b[0m\x1b[38;5;237m                                            \x1b[0m",
    "\x1b[38;2;249;38;114m██████\x1b[0m\x1b[38;5;237m                                            \x1b[0m",
]


def test_render():
    bar = BlockBar(completed=11, width=50)
    bar_render = render(bar)
    assert bar_render == expected[0]
    bar.update(completed=12)
    bar_render = render(bar)
    assert bar_render == expected[1]


def test_measure():
    bar = BlockBar()
    measurement = bar.__rich_measure__(None, 120)
    assert measurement.minimum == 4
    assert measurement.maximum == 120


def test_zero_total():
    # Shouldn't throw zero division error
    bar = BlockBar(total=0)
    render(bar)


def test_blend():
    bar = BlockBar(completed=11, width=50, blend_colors=True)
    bar_render = render(bar)
    print(repr(bar_render))
    expected = "\x1b[38;2;234;50;104m█████\x1b[0m\x1b[38;2;234;50;104m▌\x1b[0m\x1b[38;5;237m                                            \x1b[0m"
    assert bar_render == expected


if __name__ == "__main__":
    bar = BlockBar(completed=11, width=50)
    bar_render = render(bar)
    print(repr(bar_render))
    bar.update(completed=12)
    bar_render = render(bar)
    print(repr(bar_render))
    bar = BlockBar(completed=11, width=50, blend_colors=True)
    bar_render = render(bar)
    print(repr(bar_render))
