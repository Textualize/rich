import io

from rich.console import Console

from render import render


test_data = [
    {
        "jsonrpc": "2.0",
        "method": "sum",
        "params": [None, 1, 2, 4, False, True],
        "id": "1",
    },
    {"jsonrpc": "2.0", "method": "notify_hello", "params": [7]},
    {"jsonrpc": "2.0", "method": "subtract", "params": [42, 23], "id": "2"},
]


def render_log():
    console = Console(
        file=io.StringIO(), width=80, force_terminal=True, log_time_format="[TIME] "
    )
    enabled = False
    context = {
        "foo": "bar",
    }
    movies = ["Deadpool", "Rise of the Skywalker"]
    console.log()
    console.log("Hello from", console, "!")
    console.log(test_data, log_locals=True)
    return console.file.getvalue()


def test_log():
    expected = "\n\x1b[2;36m[TIME] \x1b[0mHello from \x1b[1m<\x1b[0m\x1b[1;38;5;13mconsole\x1b[0m\x1b[39m \x1b[0m\x1b[3;33mwidth\x1b[0m\x1b[39m=\x1b[0m\x1b[1;34m80\x1b[0m\x1b[39m ColorSystem.TRUECOLOR\x1b[0m\x1b[1m>\x1b[0m !      \x1b[2mtest_log.py:30\x1b[0m\n\x1b[2;36m       \x1b[0m\x1b[1m[\x1b[0m                                                          \x1b[2mtest_log.py:31\x1b[0m\n           \x1b[1m{\x1b[0m                                                                    \n               \x1b[32m'id'\x1b[0m: \x1b[32m'\x1b[0m\x1b[32m1\x1b[0m\x1b[32m'\x1b[0m,                                                       \n               \x1b[32m'jsonrpc'\x1b[0m: \x1b[32m'\x1b[0m\x1b[32m2.0\x1b[0m\x1b[32m'\x1b[0m,                                                \n               \x1b[32m'method'\x1b[0m: \x1b[32m'sum'\x1b[0m,                                                 \n               \x1b[32m'params'\x1b[0m: \x1b[1m[\x1b[0m\x1b[3;35mNone\x1b[0m, \x1b[1;34m1\x1b[0m, \x1b[1;34m2\x1b[0m, \x1b[1;34m4\x1b[0m, \x1b[3;38;5;9mFalse\x1b[0m, \x1b[3;38;5;10mTrue\x1b[0m\x1b[1m]\x1b[0m,                          \n           \x1b[1m}\x1b[0m,                                                                   \n           \x1b[1m{\x1b[0m                                                                    \n               \x1b[32m'jsonrpc'\x1b[0m: \x1b[32m'\x1b[0m\x1b[32m2.0\x1b[0m\x1b[32m'\x1b[0m,                                                \n               \x1b[32m'method'\x1b[0m: \x1b[32m'notify_hello'\x1b[0m,                                        \n               \x1b[32m'params'\x1b[0m: \x1b[1m[\x1b[0m\x1b[1;34m7\x1b[0m\x1b[1m]\x1b[0m,                                                   \n           \x1b[1m}\x1b[0m,                                                                   \n           \x1b[1m{\x1b[0m                                                                    \n               \x1b[32m'id'\x1b[0m: \x1b[32m'\x1b[0m\x1b[32m2\x1b[0m\x1b[32m'\x1b[0m,                                                       \n               \x1b[32m'jsonrpc'\x1b[0m: \x1b[32m'\x1b[0m\x1b[32m2.0\x1b[0m\x1b[32m'\x1b[0m,                                                \n               \x1b[32m'method'\x1b[0m: \x1b[32m'subtract'\x1b[0m,                                            \n               \x1b[32m'params'\x1b[0m: \x1b[1m[\x1b[0m\x1b[1;34m42\x1b[0m, \x1b[1;34m23\x1b[0m\x1b[1m]\x1b[0m,                                              \n           \x1b[1m}\x1b[0m,                                                                   \n       \x1b[1m]\x1b[0m                                                                        \n       \x1b[3m                        Locals                             \x1b[0m              \n       \x1b[34m╭─────────┬────────────────────────────────────────╮\x1b[0m                     \n       \x1b[34m│\x1b[0m\x1b[32m'console'\x1b[0m\x1b[34m│\x1b[0m\x1b[1m<\x1b[0m\x1b[1;38;5;13mconsole\x1b[0m\x1b[39m \x1b[0m\x1b[3;33mwidth\x1b[0m\x1b[39m=\x1b[0m\x1b[1;34m80\x1b[0m\x1b[39m ColorSystem.TRUECOLOR\x1b[0m\x1b[1m>\x1b[0m\x1b[34m│\x1b[0m                     \n       \x1b[34m│\x1b[0m\x1b[32m'enabled'\x1b[0m\x1b[34m│\x1b[0m\x1b[3;38;5;9mFalse\x1b[0m                                   \x1b[34m│\x1b[0m                     \n       \x1b[34m│\x1b[0m\x1b[32m'context'\x1b[0m\x1b[34m│\x1b[0m\x1b[1m{\x1b[0m\x1b[32m'foo'\x1b[0m: \x1b[32m'bar'\x1b[0m\x1b[1m}\x1b[0m                          \x1b[34m│\x1b[0m                     \n       \x1b[34m│\x1b[0m\x1b[32m'movies'\x1b[0m \x1b[34m│\x1b[0m\x1b[1m[\x1b[0m\x1b[32m'Deadpool'\x1b[0m, \x1b[32m'Rise of the Skywalker'\x1b[0m\x1b[1m]\x1b[0m   \x1b[34m│\x1b[0m                     \n       \x1b[34m╰─────────┴────────────────────────────────────────╯\x1b[0m                     \n"
    assert render_log() == expected


if __name__ == "__main__":
    print(render_log())
    print(repr(render_log()))
