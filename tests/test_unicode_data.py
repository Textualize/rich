from __future__ import annotations

import pytest

from rich._unicode_data import VERSIONS, _parse_version, load


def test_load():
    """Test all versions may be loaded."""
    for version in VERSIONS:
        load(version)


@pytest.mark.parametrize(
    "version_str,version_tuple",
    [
        ("1", (1, 0, 0)),
        ("1.0", (1, 0, 0)),
        ("1.2", (1, 2, 0)),
        ("1.2.3", (1, 2, 3)),
    ],
)
def test_parse_version(version_str: str, version_tuple: tuple[str, ...]) -> None:
    assert _parse_version(version_str) == version_tuple


@pytest.mark.parametrize(
    "version_in,version_selected",
    [
        # Lower versions will pick the first (4.1.0)
        ("0", "4.1.0"),
        ("1", "4.1.0"),
        ("1.0", "4.1.0"),
        ("1.0.0", "4.1.0"),
        ("4.0.0", "4.1.0"),
        ("4.0.2", "4.1.0"),
        ("4.1.0", "4.1.0"),
        ("4.1.1", "4.1.0"),
        ("4.2.1", "4.1.0"),
        # Nearest version lower
        ("5", "5.0.0"),
        ("5.0", "5.0.0"),
        ("5.0.0", "5.0.0"),
        ("5.0.1", "5.0.0"),
        ("5.1.0", "5.1.0"),
        ("5.1.1", "5.1.0"),
        # Maximum version if greater than the maximum
        ("17.0.0", "17.0.0"),
        ("17.0.1", "17.0.0"),
        ("17.1.0", "17.0.0"),
        # Greater than the maximum
        ("18.0.0", "17.0.0"),
    ],
)
def test_load_version(version_in: str, version_selected: str) -> None:
    """Test that load will pick the nearest lower version if it exists, or the lowest version if below the first available version."""
    assert load(version_in).unicode_version == version_selected


def test_load_version_invalid() -> None:
    """Check that invalid versions load the latest unicode data."""
    assert load("foo").unicode_version == "17.0.0"
    assert load("a.b.c").unicode_version == "17.0.0"
    assert load("1.2.3a").unicode_version == "17.0.0"
