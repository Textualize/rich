"""Overwrite hidden tqdm references (aggressive replacement example).

Simulates a third-party module (examples/tqdm_hidden_lib.py) that stashes
``tqdm`` in an internal variable at import time. The adapter should still
replace that hidden reference after install_tqdm().

Run:
  PYTHONPATH=. python examples/tqdm_adapter_hidden.py
"""

from rich.tqdm import install_tqdm

from examples import tqdm_hidden_lib


def main() -> None:
    # Import happens before install; hidden module already captured original tqdm
    install_tqdm()  # aggressive replacement updates hidden references
    tqdm_hidden_lib.run_hidden_loop()


if __name__ == "__main__":
    main()
