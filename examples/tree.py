import os
from operator import attrgetter
import pathlib
import sys

from rich import print
from rich.filesize import decimal
from rich.markup import escape
from rich.text import Text
from rich.tree import Tree


def walk_directory(directory, tree):
    paths = sorted(
        pathlib.Path(directory).iterdir(),
        key=lambda path: (path.name.lower(), path.is_file()),
    )
    for path in paths:
        if path.name.startswith("."):
            continue
        if path.is_dir():
            style = "dim not bold" if path.name.startswith("__") else ""
            branch = tree.add(
                f"[bold magenta]:open_file_folder: {escape(path.name)}",
                style=style,
                guide_style=style,
            )
            walk_directory(path, branch)
        else:
            text_filename = Text(path.name, "green")
            text_filename.highlight_regex(r"\..*$", "bold red")
            file_size = path.stat().st_size
            text_filename.append(f" ({decimal(file_size)})", "blue")
            tree.add(Text("🐍 " if path.suffix == ".py" else "📄 ") + text_filename)


try:
    directory = os.path.abspath(sys.argv[1])
except IndexError:
    print("[b]Usage:[/] python tree.py <DIRECTORY>")
else:
    tree = Tree(directory, guide_style="bold cyan")
    walk_directory(directory, tree)
    print(tree)