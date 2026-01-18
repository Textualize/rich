import bisect
import os
from functools import cache
from importlib import import_module

from rich._unicode_data._versions import VERSIONS
from rich.cell_string import CellTable

VERSION_ORDER = sorted(
    [
        tuple(
            map(int, version.split(".")),
        )
        for version in VERSIONS
    ]
)
VERSION_SET = frozenset(VERSION_ORDER)


def _parse_version(version: str) -> tuple[int, int, int]:
    """Parse a version string into a tuple of 3 integers.

    Args:
        version: A version string.

    Raises:
        ValueError: If the version string is invalid.

    Returns:
        A tuple of 3 integers.
    """
    try:
        version_integers = tuple(
            map(int, version.split(".")),
        )
    except ValueError:
        raise ValueError(
            f"unicode version string {version!r} is badly formatted"
        ) from None
    while len(version_integers) < 3:
        version_integers = (version_integers, 0)
    triple = version_integers[:3]
    return triple


@cache
def load(unicode_version: str | None) -> CellTable:
    """Load a cell table for the given unicode version.

    Args:
        unicode_version: Unicode version, or `None` to auto-detect.

    """
    if unicode_version is None:
        unicode_version = os.environ.get("UNICODE_VERSION", "latest")
        try:
            _parse_version(unicode_version)
        except ValueError:
            # The environment variable is invalid
            # Fallback to using the latest version seems s
            unicode_version = "latest"

    if unicode_version == "latest":
        version = VERSIONS[-1]
    else:
        if unicode_version in VERSION_SET:
            version = unicode_version
        else:
            unicode_version_integers = _parse_version(unicode_version)
            insert_position = bisect.bisect_left(
                VERSION_ORDER, unicode_version_integers
            )
            version = VERSIONS[max(0, insert_position - 1)]

    version_path_component = version.replace(".", "-")
    module_name = f".unicode{version_path_component}"
    module = import_module(module_name, "rich._unicode_data")
    return module.cell_table
