import pytest

from rich.emoji import Emoji, NoEmoji


def test_no_emoji():
    with pytest.raises(NoEmoji):
        Emoji("ambivalent_bunny")


def test_str_repr():
    assert str(Emoji("pile_of_poo")) == "💩"
    assert repr(Emoji("pile_of_poo")) == "<emoji 'pile_of_poo'>"


def test_replace():
    assert Emoji.replace("my code is :pile_of_poo:") == "my code is 💩"
