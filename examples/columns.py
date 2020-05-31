from rich import print
from rich.columns import Columns
from rich.panel import Panel

import json
from urllib.request import urlopen


users = json.loads(urlopen("https://randomuser.me/api/?results=30").read())["results"]
print(users)

user_renderables = [
    Panel(
        f"[b]{user['name']['first']} {user['name']['last']}[/b]\n[yellow]{user['location']['country']}",
        expand=False,
    )
    for user in users
]

print(Columns(user_renderables))
