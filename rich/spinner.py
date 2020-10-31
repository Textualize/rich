from time import sleep
from threading import Thread

RECALL = "\033[2K\r"


class Spinner:
    SLASHES = "|/-\\"

    def loop(self):
        i = 0
        while self._run:
            print(
                "{r}{icon} {message}".format(
                    r=RECALL,
                    icon=self._icons[i % len(self._icons)],
                    message=self.message,
                ),
                end="",
            )
            i += 1
            sleep(self._delay)

    def start(self):
        self._run = True
        self._thread = Thread(target=self.loop)
        self._thread.start()

    def stop(self):
        self._run = False
        while self._thread.is_alive():
            pass
        print(RECALL, end="")

    def __init__(self, message="Loading...", delay=0.05, icons=SLASHES):
        self._run = False
        self.message = message
        self._thread: Thread = None
        self._delay = delay
        self._icons = icons

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, t, value, tb):
        self.stop()
