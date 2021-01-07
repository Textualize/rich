import os
import pathlib
import sys

from rich import print
from rich.filesize import decimal
from rich.markup import escape
from rich.style import Style
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
            style = "dim" if path.name.startswith("__") else ""
            branch = tree.add(
                f"[bold magenta]:open_file_folder: [link file://{path}]{escape(path.name)}",
                style=style,
                guide_style=style,
            )
            walk_directory(path, branch)
        else:
            text_filename = Text(path.name, "green")
            text_filename.highlight_regex(r"\..*$", "bold red")
            text_filename.stylize(f"link file://{ path }")
            file_size = path.stat().st_size
            text_filename.append(f" ({decimal(file_size)})", "blue")
            tree.add(Text("🐍 " if path.suffix == ".py" else "📄 ") + text_filename)


try:
    directory = os.path.abspath(sys.argv[1])
except IndexError:
    print("[b]Usage:[/] python tree.py <DIRECTORY>")
else:
    tree = Tree(
        f":open_file_folder: [link file://{directory}]{directory}",
        guide_style="bold bright_blue",
    )
    walk_directory(directory, tree)
    print(tree)
