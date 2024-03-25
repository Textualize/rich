from time import sleep
from urllib.request import urlopen

from rich.progress import wrap_file

# Read a URL with urlopen
response = urlopen("https://www.textualize.io")
# Get the size from the headers
size = int(response.headers["Content-Length"])

# Wrap the response so that it update progress

with wrap_file(response, size) as file:
    for line in file:
        print(line.decode("utf-8"), end="")
        sleep(0.1)
