import threading

import rich.console

console = rich.console.Console()


def count_to_n(n):
    for i in range(n):
        console.print(i)


with console.status("testing"):
    thread = threading.Thread(target=count_to_n, args=(10,))
    thread.start()