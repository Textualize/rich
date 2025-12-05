"""Adapter install/uninstall coverage for the Rich tqdm shim."""

import sys
import types
from typing import cast

from rich.tqdm import _TqdmWrapper, install_tqdm, uninstall_tqdm


def test_install_replaces_imported_reference() -> None:
    """Replacing imported tqdm symbols should affect existing aliases."""
    saved = sys.modules.pop("tqdm", None)
    try:
        fake = types.ModuleType("tqdm")

        def orig_tqdm(iterable=None, **kwargs):
            del kwargs
            if iterable is None:
                return None
            return ("orig", list(iterable))

        def orig_trange(*args, **kwargs):
            del kwargs
            return range(*args)

        fake.tqdm = orig_tqdm
        fake.trange = orig_trange
        sys.modules["tqdm"] = fake

        third = types.ModuleType("thirdparty")
        third.tqdm_alias = fake.tqdm
        sys.modules["thirdparty"] = third

        try:
            assert third.tqdm_alias is orig_tqdm
            install_tqdm()
            assert third.tqdm_alias is not orig_tqdm
            it = third.tqdm_alias(range(3))
            assert list(it) == [0, 1, 2]
        finally:
            uninstall_tqdm()
            assert third.tqdm_alias is orig_tqdm
    finally:
        sys.modules.pop("thirdparty", None)
        if saved is not None:
            sys.modules["tqdm"] = saved
        else:
            sys.modules.pop("tqdm", None)


def test_install_replaces_hidden_reference_and_postfix_support() -> None:
    """Hidden tqdm references should update and still format postfix values."""
    saved = sys.modules.pop("tqdm", None)
    try:
        fake = types.ModuleType("tqdm")

        def orig_tqdm(iterable=None, **kwargs):
            del kwargs
            if iterable is None:
                return None
            return ("orig", list(iterable))

        fake.tqdm = orig_tqdm
        fake._hidden_tqdm = orig_tqdm  # pylint: disable=protected-access
        sys.modules["tqdm"] = fake

        try:
            install_tqdm()
            patched = fake.tqdm
            assert patched is not orig_tqdm
            assert fake._hidden_tqdm is patched  # pylint: disable=protected-access

            progress = cast(_TqdmWrapper, patched(range(2)))
            progress.update(postfix={"loss": 1.23})  # pylint: disable=no-member
            assert progress.postfix == {"loss": "1.23"}  # pylint: disable=no-member
        finally:
            uninstall_tqdm()
    finally:
        if saved is not None:
            sys.modules["tqdm"] = saved
        else:
            sys.modules.pop("tqdm", None)
