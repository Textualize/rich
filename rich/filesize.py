# coding: utf-8
"""Functions for reporting filesizes. Borrowed from https://github.com/PyFilesystem/pyfilesystem2

The functions declared in this module should cover the different
usecases needed to generate a string representation of a file size
using several different units. Since there are many standards regarding
file size units, three different functions have been implemented.

See Also:
    * `Wikipedia: Binary prefix <https://en.wikipedia.org/wiki/Binary_prefix>`_

"""

__all__ = ["traditional", "decimal", "binary"]

from typing import Iterable, List, Tuple


def _to_str(size: int, suffixes: Iterable[str], base: int) -> str:
    if size == 1:
        return "1 byte"
    elif size < base:
        return "{:,} bytes".format(size)

    for i, suffix in enumerate(suffixes, 2):  # noqa: B007
        unit = base ** i
        if size < unit:
            break
    return "{:,.1f} {}".format((base * size / unit), suffix)


def pick_unit_and_suffix(size: int, suffixes: List[str], base: int) -> Tuple[int, str]:
    """Pick a suffix and base for the given size."""
    unit = 1
    suffix = "bytes"
    if size < base:
        return 1, suffix
    for i, suffix in enumerate(suffixes, 2):
        unit = base ** i
        if size < unit:
            break
    return unit, suffix


def traditional(size: int) -> str:
    """Convert a filesize in to a string (powers of 1024, JDEC prefixes).

    In this convention, ``1024 B = 1 KB``.

    This is the format that was used to display the size of DVDs
    (*700 MB* meaning actually about *734 003 200 bytes*) before
    standardisation of IEC units among manufacturers, and still
    used by **Windows** to report the storage capacity of hard
    drives (*279.4 GB* meaning *279.4 × 1024³ bytes*).

    Arguments:
        size (int): A file size.

    Returns:
        `str`: A string containing an abbreviated file size and units.

    Example:
        >>> filesize.traditional(30000)
        '29.3 KB'

    """
    return _to_str(size, ("KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"), 1024)


def binary(size: int) -> str:
    """Convert a filesize in to a string (powers of 1024, IEC prefixes).

    In this convention, ``1024 B = 1 KiB``.

    This is the format that has gained adoption among manufacturers
    to avoid ambiguity regarding size units, since it explicitly states
    using a binary base (*KiB = kibi bytes = kilo binary bytes*).
    This format is notably being used by the **Linux** kernel (see
    ``man 7 units``).

    Arguments:
        int (size): A file size.

    Returns:
        `str`: A string containing a abbreviated file size and units.

    Example:
        >>> filesize.binary(30000)
        '29.3 KiB'

    """
    return _to_str(size, ("KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"), 1024)


def decimal(size: int) -> str:
    """Convert a filesize in to a string (powers of 1000, SI prefixes).

    In this convention, ``1000 B = 1 kB``.

    This is typically the format used to advertise the storage
    capacity of USB flash drives and the like (*256 MB* meaning
    actually a storage capacity of more than *256 000 000 B*),
    or used by **Mac OS X** since v10.6 to report file sizes.

    Arguments:
        int (size): A file size.

    Returns:
        `str`: A string containing a abbreviated file size and units.

    Example:
        >>> filesize.decimal(30000)
        '30.0 kB'

    """
    return _to_str(size, ("kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"), 1000)
