---
title: "Incorrect highlights in printed output"
alt_title:
    - "Highlighter not highlighting data"
---

Rich's default highlighter will highlight a number of common patterns, useful for debugging.
Occasionally you may find that it highlights text incorrectly.
This may be unavoidable, as Rich only sees text and can only make a best guess at what it means.

If this happens, consider disabling highlighting, or write a custom highlighter that better reflects the text you are writing. See the docs for details...

https://rich.readthedocs.io/en/latest/highlighting.html

Issues and PRs for highlighters will only be accepted for clearly broken regular expressions.
This is because a fix for your needs can break the highlighting for someone else.
