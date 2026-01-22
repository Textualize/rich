from __future__ import annotations

import bisect
import os
import sys

if sys.version_info[:2] >= (3, 9):
    from functools import cache
else:
    from functools import lru_cache as cache  # pragma: no cover

from importlib import import_module
from typing import TYPE_CHECKING, cast

from rich._unicode_data._versions import VERSIONS

if TYPE_CHECKING:
    from rich.cells import CellTable

VERSION_ORDER = sorted(
    [
        tuple(
            map(int, version.split(".")),
        )
        for version in VERSIONS
    ]
)
VERSION_SET = frozenset(VERSIONS)


def _parse_version(version: str) -> tuple[int, int, int]:
    """Parse a version string into a tuple of 3 integers.

    Args:
        version: A version string.

    Raises:
        ValueError: If the version string is invalid.

    Returns:
        A tuple of 3 integers.
    """
    version_integers: tuple[int, ...]
    try:
        version_integers = tuple(
            map(int, version.split(".")),
        )
    except ValueError:
        raise ValueError(
            f"unicode version string {version!r} is badly formatted"
        ) from None
    while len(version_integers) < 3:
        version_integers = version_integers + (0,)
    triple = cast("tuple[int, int, int]", version_integers[:3])
    return triple


@cache
def load(unicode_version: str = "auto") -> CellTable:
    """Load a cell table for the given unicode version.

    Args:
        unicode_version: Unicode version, or `None` to auto-detect.

    """
    if unicode_version == "auto":
        unicode_version = os.environ.get("UNICODE_VERSION", "latest")
        try:
            _parse_version(unicode_version)
        except ValueError:
            # The environment variable is invalid
            # Fallback to using the latest version seems reasonable
            unicode_version = "latest"

    if unicode_version == "latest":
        version = VERSIONS[-1]
    else:
        try:
            version_numbers = _parse_version(unicode_version)
        except ValueError:
            version_numbers = _parse_version(VERSIONS[-1])
        major, minor, patch = version_numbers
        version = f"{major}.{minor}.{patch}"
        if version not in VERSION_SET:
            insert_position = bisect.bisect_left(VERSION_ORDER, version_numbers)
            version = VERSIONS[max(0, insert_position - 1)]

    version_path_component = version.replace(".", "-")
    module_name = f".unicode{version_path_component}"
    module = import_module(module_name, "rich._unicode_data")
    if TYPE_CHECKING:
        assert isinstance(module.cell_table, CellTable)
    return module.cell_table
