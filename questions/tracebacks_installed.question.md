---
title: "Rich is automatically installing traceback handler."
alt_titles:
  - "Can you stop overriding traceback message formatting by default?"
---

Rich will never install the traceback handler automatically.

If you are getting Rich tracebacks and you don't want them, then some other piece of software is calling `rich.traceback.install()`.
