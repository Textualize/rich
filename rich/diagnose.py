import os
import platform

from rich import inspect
from rich.console import Console, get_windows_console_features
from rich.panel import Panel
from rich.text import Text


def report() -> None:  # pragma: no cover
    """Print a report to the terminal with debugging information"""
    console = Console()
    inspect(console)
    features = get_windows_console_features()
    inspect(features)

    if console.is_jupyter:
        jpy_parent_pid = os.getenv("JPY_PARENT_PID")
        vs_code_verbose = os.getenv("VSCODE_VERBOSE_LOGGING")
        console.print(
            Panel(
                title="Jupyter Environment Hints",
                renderable=Text(
                    f"JPY_PARENT_PID = {jpy_parent_pid}\n"
                    f"VSCODE_VERBOSE_LOGGING = {vs_code_verbose}"
                ),
            ),
        )

    console.print(f'platform="{platform.system()}"')


if __name__ == "__main__":  # pragma: no cover
    console = Console()
    inspect(console)
