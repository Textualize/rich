from typing import NamedTuple


STRIP_CONTROL_CODES = [
    8,  # Backspace
    11,  # Vertical tab
    12,  # Form feed
    13,  # Carriage return
]
_CONTROL_TRANSLATE = {_codepoint: None for _codepoint in STRIP_CONTROL_CODES}


class Control(NamedTuple):
    """Control codes that are not printable."""

    # May define pre and post control codes eventually
    codes: str


def strip_control_codes(text: str, _translate_table=_CONTROL_TRANSLATE) -> str:
    """Remove control codes from text.

    Args:
        text (str): A string possibly contain control codes.        

    Returns:
        str: String with control codes removed.
    """
    return text.translate(_translate_table)


if __name__ == "__main__":  # pragma: no cover

    print(strip_control_codes("hello\rWorld"))
