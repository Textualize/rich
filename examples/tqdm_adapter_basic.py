"""Replace tqdm with rich.progress at runtime (basic example).

Run:
  PYTHONPATH=. python examples/tqdm_adapter_basic.py
"""

from time import sleep

from rich.tqdm import install_tqdm


def main() -> None:
    install_tqdm()

    from tqdm import tqdm  # resolved to the rich-backed shim after install

    for _ in tqdm(range(10), desc="basic"):
        sleep(0.05)


if __name__ == "__main__":
    main()
