# encoding=utf-8


import io

from rich.console import Console

from .render import replace_link_ids


test_data = [1, 2, 3]


def render_log():
    console = Console(
        file=io.StringIO(),
        width=80,
        force_terminal=True,
        log_time_format="[TIME]",
        color_system="truecolor",
        legacy_windows=False,
    )
    console.log()
    console.log("Hello from", console, "!")
    console.log(test_data, log_locals=True)
    return replace_link_ids(console.file.getvalue())


def test_log():
    expected = "\n\x1b[2;36m[TIME]\x1b[0m\x1b[2;36m \x1b[0mHello from \x1b[1m<\x1b[0m\x1b[1;95mconsole\x1b[0m\x1b[39m \x1b[0m\x1b[3;33mwidth\x1b[0m\x1b[39m=\x1b[0m\x1b[1;34m80\x1b[0m\x1b[39m ColorSystem.TRUECOLOR\x1b[0m\x1b[1m>\x1b[0m !      \x1b]8;id=0;foo\x1b\\\x1b[2mtest_log.py\x1b[0m\x1b]8;;\x1b\\\x1b[2m:24\x1b[0m\n\x1b[2;36m      \x1b[0m\x1b[2;36m \x1b[0m\x1b[1m[\x1b[0m\x1b[1;34m1\x1b[0m, \x1b[1;34m2\x1b[0m, \x1b[1;34m3\x1b[0m\x1b[1m]\x1b[0m                                                  \x1b]8;id=0;foo\x1b\\\x1b[2mtest_log.py\x1b[0m\x1b]8;;\x1b\\\x1b[2m:25\x1b[0m\n       \x1b[34m╭─\x1b[0m\x1b[34m───────────────────── \x1b[0m\x1b[3;34mlocals\x1b[0m\x1b[34m ─────────────────────\x1b[0m\x1b[34m─╮\x1b[0m                   \n       \x1b[34m│\x1b[0m \x1b[3;33;44mconsole\x1b[0m\x1b[31;44m =\x1b[0m\x1b[44m \x1b[0m\x1b[1;44m<\x1b[0m\x1b[1;95;44mconsole\x1b[0m\x1b[39;44m \x1b[0m\x1b[3;33;44mwidth\x1b[0m\x1b[39;44m=\x1b[0m\x1b[1;34;44m80\x1b[0m\x1b[39;44m ColorSystem.TRUECOLOR\x1b[0m\x1b[1;44m>\x1b[0m \x1b[34m│\x1b[0m                   \n       \x1b[34m╰────────────────────────────────────────────────────╯\x1b[0m                   \n"
    rendered = render_log()
    print(repr(rendered))
    assert rendered == expected


if __name__ == "__main__":
    render = render_log()
    print(render)
    print(repr(render))
