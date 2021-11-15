from rich.console import Console
from rich.screen import Screen


def test_screen():
    console = Console(color_system=None, width=20, height=5, legacy_windows=False)
    with console.capture() as capture:
        console.print(Screen("foo\nbar\nbaz\nfoo\nbar\nbaz\foo"))
    result = capture.get()
    print(repr(result))
    expected = "foo                 \nbar                 \nbaz                 \nfoo                 \nbar                 "
    assert result == expected
