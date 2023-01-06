---
title: "Why does content in square brackets disappear?"
alt_titles:
    - "Can not print a [string]"
---

Rich will treat text within square brackets as *markup tags*, for instance `"[bold]This is bold[/bold]"`.

If you are printing strings with literally square brackets you can either disable markup, or escape your strings.
See the docs on [console markup](https://rich.readthedocs.io/en/latest/markup.html) for how to do this.
