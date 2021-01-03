import os
import sys

from rich import print
from rich.text import Text
from rich.tree import Tree


def walk_directory(directory, tree):
    for filename in os.listdir(directory):

        path = os.path.join(directory, filename)
        if os.path.isdir(path):
            branch = tree.add(Text(filename, "bold magenta"))
            walk_directory(path, branch)
        else:
            filename = Text(filename)
            filename.highlight_regex("\..*$", "bold green")
            tree.add(filename)


try:
    directory = os.path.abspath(sys.argv[1])
except IndexError:
    print("[b]Usage:[/] python tree.py <DIRECTORY>")
else:
    tree = Tree(directory, line_style="cyan")
    walk_directory(directory, tree)
    print(tree)