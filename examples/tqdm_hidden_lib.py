"""Simulated third-party module that hides a tqdm reference internally.

Imported by tqdm_adapter_hidden.py to demonstrate aggressive replacement.
"""

import time

import tqdm as _tqdm

_hidden_tqdm = _tqdm.tqdm


def run_hidden_loop() -> None:
    for _ in _hidden_tqdm(range(5), desc="hidden-lib"):
        time.sleep(0.05)
