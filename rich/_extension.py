from typing import Any

from rich.pretty import install
from rich.traceback import install as tr_install


def load_ipython_extension(ip: Any) -> None:

    install()
    tr_install()
