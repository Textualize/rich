"""
This example shows how to display content in columns.

The data is pulled from https://randomuser.me
"""

import json
from urllib.request import urlopen

from rich import print
from rich.columns import Columns
from rich.panel import Panel


def get_content(user):
    """Extract text from user dict."""
    country = user["location"]["country"]
    name = f"{user['name']['first']} {user['name']['last']}"
    return f"[b]{name}[/b]\n[yellow]{country}"


users = json.loads(urlopen("https://randomuser.me/api/?results=30").read())["results"]
print(users)
user_renderables = [Panel(get_content(user), expand=False) for user in users]
print(Columns(user_renderables))
