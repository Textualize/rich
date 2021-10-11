import rich.console
import rich.live
import time
console = rich.console.Console()

with rich.live.Live("this text should disappear but doesn't", console=console, transient=True, redirect_stderr=False, refresh_per_second=.0000001):
  print("a")
  time.sleep(.5)
  print("b")
