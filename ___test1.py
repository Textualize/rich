import atexit
import logging
import logging.handlers
import queue

import rich.logging
import rich.console

logger = logging.getLogger(__name__)
console = rich.console.Console()

root_logger = logging.getLogger("")
rhandler = rich.logging.RichHandler(console=console)
que = queue.Queue()
queue_handler = logging.handlers.QueueHandler(que)
listener = logging.handlers.QueueListener(que, rhandler)
root_logger.addHandler(queue_handler)
listener.start()
atexit.register(lambda x: x.stop(), listener)

with console.status("testing"):
    for n in range(10):
        logger.error(n)
