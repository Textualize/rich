---
title: "Natively inserted ANSI escape sequence characters break alignment of Panel."
alt_titles:
  - "Escape codes break alignment."
---

If you print ansi escape sequences for color and style you may find the output breaks your output.
You may find that border characters in Panel and Table are in the wrong place, for example.

As a general rule, you should allow Rich to generate all ansi escape sequences, so it can correctly account for these invisible characters.
If you can't avoid a string with escape codes, you can convert it to an equivalent `Text` instance with `Text.from_ansi`.
