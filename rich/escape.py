ESC = "\x1b"
CSI = f"{ESC}["

BOLD = f"{CSI}21m"

import sys

sys.stdout.write(BOLD)

sys.stdout.write("hello world")
