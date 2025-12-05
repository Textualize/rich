"""Parity checks between Rich's tqdm shim and vendored tqdm reference.

Note: this test relies on a vendored copy of tqdm under ``tests/tqdm`` to
provide a reference implementation. If that folder is absent, the test is
skipped. Keep the vendored copy lightweight and in sync with the targeted tqdm
version when you want to exercise parity; otherwise the skip is expected in
normal installs.
"""

# pylint: disable=import-error

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

from rich.tqdm import install_tqdm, uninstall_tqdm


SUBMODULE_ROOT = Path(__file__).parent / "tqdm"


def test_tqdm_adapter_len_and_disable_parity() -> None:
    """Use the vendored tqdm submodule as a baseline for adapter parity."""

    if not SUBMODULE_ROOT.exists():
        pytest.skip("vendored tqdm submodule missing")

    added_path = False
    submodule_path = str(SUBMODULE_ROOT)
    if submodule_path not in sys.path:
        sys.path.insert(0, submodule_path)
        added_path = True

    orig_mod = None
    try:
        orig_mod = importlib.import_module("tqdm")
        orig_tqdm = orig_mod.tqdm

        baseline_len = len(orig_tqdm(range(5)))

        install_tqdm()
        patched_tqdm = orig_mod.tqdm

        assert patched_tqdm is not orig_tqdm
        assert len(patched_tqdm(range(5))) == baseline_len
        assert list(patched_tqdm(range(3), disable=True)) == [0, 1, 2]
    finally:
        uninstall_tqdm()
        if orig_mod is not None:
            importlib.reload(orig_mod)
        sys.modules.pop("tqdm", None)
        if added_path:
            try:
                sys.path.remove(submodule_path)
            except ValueError:
                pass
