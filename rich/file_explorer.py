"""FileExplorer renderable: display a directory tree using Rich's Tree.

Usage:
    from rich.console import Console
    from rich.file_explorer import FileExplorer

    console = Console()
    console.print(FileExplorer("."))
"""
from __future__ import annotations

import pathlib
from typing import Iterable, List, Optional

from rich.filesize import decimal
from rich.markup import escape
from rich.text import Text
from rich.tree import Tree


class FileExplorer:
    """Renderable that shows a filesystem tree for a given path.

    Parameters
    - path: root directory as str or pathlib.Path
    - ignore: optional iterable of filenames to ignore
    """

    def __init__(self, path: str | pathlib.Path, ignore: Optional[Iterable[str]] = None) -> None:
        self.path = pathlib.Path(path)
        self.ignore: List[str] = list(ignore) if ignore is not None else []

    def __rich_console__(self, console, options):
        """Yield a single Tree representing the directory structure."""
        root_name = escape(str(self.path))
        tree = Tree(f"📁 [bold blue]{root_name}", guide_style="bold bright_blue")

        def _add_children(directory: pathlib.Path, node: Tree) -> None:
            try:
                entries = sorted(
                    directory.iterdir(),
                    key=lambda p: (p.is_file(), p.name.lower()),
                )
            except PermissionError:
                node.add("[red]Permission denied[/]")
                return

            for entry in entries:
                if entry.name in self.ignore:
                    continue
                # skip hidden files? keep as-is (user can add to ignore)
                if entry.is_dir():
                    label = f"📁 [bold blue]{escape(entry.name)}"
                    branch = node.add(label)
                    _add_children(entry, branch)
                else:
                    try:
                        size = entry.stat().st_size
                        size_text = f" ({decimal(size)})"
                    except Exception:
                        size_text = ""
                    file_text = Text("📄 ")
                    file_text.append(escape(entry.name))
                    if size_text:
                        file_text.append(size_text, style="dim")
                    node.add(file_text)

        if self.path.exists() and self.path.is_dir():
            _add_children(self.path, tree)
        else:
            tree.add("[red]Path does not exist or is not a directory[/]")

        yield tree
