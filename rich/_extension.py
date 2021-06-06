from typing import Any


def load_ipython_extension(ip: Any) -> None:
    # prevent circular import
    from rich.pretty import install
    from rich.traceback import install as tr_install

    install()
    tr_install()
