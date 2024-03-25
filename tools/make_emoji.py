try:
    import emoji
except ImportError:
    print("pip install emoji")
    raise

from emoji.unicode_codes import EMOJI_ALIAS_UNICODE

emoji = {k.lower().strip(":"): v for k, v in EMOJI_ALIAS_UNICODE.items()}

with open("_emoji_codes.py", "wt") as f:
    f.write("EMOJI=" + str(emoji))
