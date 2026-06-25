`_guess_lexer` uses `str.index()` to find the first newline in source code, but `index()` raises `ValueError` when the substring isn't found. The subsequent check `if new_line_index != -1` only makes sense with `str.find()`, which returns `-1` on miss.

When a traceback includes a frame from a single-line source file (no trailing newline), `_guess_lexer` crashes with an unhandled `ValueError` instead of rendering the traceback.

Changed `code.index("\n")` → `code.find("\n")` so the existing `-1` guard works as intended.
