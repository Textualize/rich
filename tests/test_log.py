import io

from rich.console import Console

from .render import render


test_data = [1, 2, 3]


def render_log():
    console = Console(
        file=io.StringIO(),
        width=80,
        force_terminal=True,
        log_time_format="[TIME] ",
        color_system="truecolor",
    )
    console.log()
    console.log("Hello from", console, "!")
    console.log(test_data, log_locals=True)
    return console.file.getvalue()


def test_log():
    expected = "\n\x1b[2;36m[TIME] \x1b[0mHello from \x1b[1m<\x1b[0m\x1b[1;38;5;13mconsole\x1b[0m\x1b[39m \x1b[0m\x1b[3;33mwidth\x1b[0m\x1b[39m=\x1b[0m\x1b[1;34m80\x1b[0m\x1b[39m ColorSystem.TRUECOLOR\x1b[0m\x1b[1m>\x1b[0m !      \x1b[2mtest_log.py:20\x1b[0m\n\x1b[2;36m       \x1b[0m\x1b[1m[\x1b[0m\x1b[1;34m1\x1b[0m, \x1b[1;34m2\x1b[0m, \x1b[1;34m3\x1b[0m\x1b[1m]\x1b[0m                                                  \x1b[2mtest_log.py:21\x1b[0m\n       \x1b[3m                        Locals                             \x1b[0m              \n       \x1b[34m╭─────────┬────────────────────────────────────────╮\x1b[0m                     \n       \x1b[34m│\x1b[0m\x1b[32m'console'\x1b[0m\x1b[34m│\x1b[0m\x1b[1m<\x1b[0m\x1b[1;38;5;13mconsole\x1b[0m\x1b[39m \x1b[0m\x1b[3;33mwidth\x1b[0m\x1b[39m=\x1b[0m\x1b[1;34m80\x1b[0m\x1b[39m ColorSystem.TRUECOLOR\x1b[0m\x1b[1m>\x1b[0m\x1b[34m│\x1b[0m                     \n       \x1b[34m╰─────────┴────────────────────────────────────────╯\x1b[0m                     \n"
    assert render_log() == expected


if __name__ == "__main__":
    print(render_log())
    print(repr(render_log()))
