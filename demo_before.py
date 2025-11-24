"""Demo: behavior BEFORE adding explicit markup validation.

This script prints a broken markup string directly with `rich.Console.print`.
It demonstrates the "silent failure" behavior where mismatched tags do not
raise an exception and the renderer may ignore or render them literally.

Run with: python demo_before.py
"""
from rich.console import Console


broken_text = "[bold]Hello[/dim]"


def main() -> None:
    console = Console()

    # Intentionally printing a string with mismatched tags WITHOUT validation.
    # In this demo we do not use MarkupValidator, so Console.print will not raise
    # an exception; it will either ignore the bad closing tag or render it
    # depending on the environment. This illustrates a silent failure.
    console.print("-- Printing without validation (silent failure expected) --")
    console.print(broken_text)

    # Also print a plain notification so the behavior is explicit when run
    print("Printed without validation — no exception thrown (silent failure).")


if __name__ == "__main__":
    main()
