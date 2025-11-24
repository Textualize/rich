"""Demo: behavior AFTER adding explicit markup validation.

This script validates the same broken markup string using
`rich.markup_validator.MarkupValidator`. If validation fails a
`rich.errors.MarkupError` is caught and a clear alert is printed.

Run with: python demo_after.py
"""
from rich.console import Console
from rich.markup_validator import MarkupValidator
from rich.errors import MarkupError


broken_text = "[bold]Hello[/dim]"


def main() -> None:
    console = Console()
    validator = MarkupValidator()

    try:
        # Validate markup first. This will raise MarkupError for mismatches.
        validator.validate(broken_text)
    except MarkupError as exc:
        console.print("[bold red]🚨 Validation Failed![/]")
        console.print(f"[red]{exc}[/]")
    else:
        # Only print if validation passes
        console.print("-- Validation passed; now printing --")
        console.print(broken_text)


if __name__ == "__main__":
    main()
