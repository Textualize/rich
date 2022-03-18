try:
    import emoji
except ImportError:
    print("pip install emoji")
    raise

from tkinter import W
from emoji.unicode_codes import EMOJI_ALIAS_UNICODE_ENGLISH

emoji_dict = {k.lower().strip(":"): v for k, v in EMOJI_ALIAS_UNICODE_ENGLISH.items()}

with open("_emoji_codes.py", "wt") as f:
    f.write("EMOJI=" + str(emoji_dict))
