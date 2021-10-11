import threading
import rich.console
import rich.live
import time
console = rich.console.Console()


x = 0

def count_to_n(n):
    global x
    x += 1
    while x != 2:
        ...
    console.print(str(time.time()) + " from thread")


with rich.live.Live("this text should disappear but doesn't", console=console, transient=True, redirect_stderr=False, refresh_per_second=1):
    thread = threading.Thread(target=count_to_n, args=(5,))
    thread.start()
    while x != 1:
     ...
    x += 1
thread.join()
