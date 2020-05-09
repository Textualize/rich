from rich.__main__ import make_test_card

from .render import render

try:
    from ._card_render import expected
except ImportError:
    expected = None


def test_card_render():
    card = make_test_card()
    result = render(card)
    assert result == expected


if __name__ == "__main__":
    card = make_test_card()
    with open("_card_render.py", "wt") as fh:
        card_render = render(card)
        print(card_render)
        fh.write(f"expected={card_render!r}")
