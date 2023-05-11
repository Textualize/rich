# coding: utf-8
"""Functions for reporting filesizes. Borrowed from https://github.com/PyFilesystem/pyfilesystem2

The functions declared in this module should cover the different
use cases needed to generate a string representation of a file size
using several different units. Since there are many standards regarding
file size units, three different functions have been implemented.

See Also:
    * `Wikipedia: Binary prefix <https://en.wikipedia.org/wiki/Binary_prefix>`_

"""

__all__ = ["decimal"]

from typing import Iterable, Tuple, Union


def _to_str(
    size: Union[float, int],
    suffixes: Iterable[str],
    base: int,
    *,
    precision: int = 1,
    separator: str = " "
) -> str:
    for i, suffix in enumerate(suffixes, 1):  # noqa: B007
        unit = base**i
        if size < unit:
            break

    size = base * size / unit
    if size == int(size):
        precision = 0

    return "{:,.{precision}f}{separator}{}".format(
        size,
        suffix,
        precision=precision,
        separator=separator
    )


def pick_unit_and_suffix(size: int, suffixes: Iterable[str], base: int) -> Tuple[int, str]:
    """Pick a suffix and base for the given size."""
    for i, suffix in enumerate(suffixes):
        unit = base**i
        if size < unit * base:
            break
    return unit, suffix


def decimal(
    size: Union[float, int],
    *,
    precision: int = 1,
    separator: str = " "
) -> str:
    """Convert a filesize in to a string (powers of 1000, SI prefixes).

    In this convention, ``1000 B = 1 kB``.

    This is typically the format used to advertise the storage
    capacity of USB flash drives and the like (*256 MB* meaning
    actually a storage capacity of more than *256 000 000 B*),
    or used by **Mac OS X** since v10.6 to report file sizes.

    Arguments:
        float/int (size): A file size.
        int (precision): The number of decimal places to include (default = 1).
        str (separator): The string to separate the value from the units (default = " ").

    Returns:
        `str`: A string containing a abbreviated file size and units.

    Example:
        >>> filesize.decimal(30000)
        '30.0 kB'
        >>> filesize.decimal(30000, separator="")
        '30.0kB'
        >>> filesize.decimal(361.3816634069428, precision=1)
        '361.3 bytes'

    """
    return _to_str(
        size,
        ("bytes", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"),
        1000,
        precision=precision,
        separator=separator
    )
