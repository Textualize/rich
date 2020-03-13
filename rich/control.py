from typing import NamedTuple


class Control(NamedTuple):
    """Control codes that are not printable."""

    # May define pre and post control codes eventually
    codes: str
