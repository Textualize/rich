from rich import print
from rich.columns import Columns
from rich.panel import Panel

import json
from urllib.request import urlopen


users = json.loads(urlopen("https://randomuser.me/api/?results=30").read())["results"]
print(users)


def get_content(user):
    country = user["location"]["country"]
    name = f"{user['name']['first']} {user['name']['last']}"

    return f"[b]{name}[/b]\n[yellow]{country}"


user_renderables = [Panel(get_content(user), expand=False,) for user in users]

print(Columns(user_renderables))
