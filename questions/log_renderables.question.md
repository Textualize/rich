---
title: "How do I log a renderable?"
alt_titles:
  - "Cannot log Tree() output to file"
  - "Log a Panel or Table to a RichHandler"
---

Python's logging module is designed to work with strings. Consequently you won't be able to log Rich renderables (Table, Tree, etc) by calling `logger.debug` or other similar method.

You could use the [capture](https://rich.readthedocs.io/en/latest/console.html#capturing-output) API to convert the renderable to a string and log that. However I would advise against it.

Logging supports configurable back-ends, which means that a log message could go somewhere other than the terminal -- which may not correctly render the formatting and style produced by Rich.

If you are only logging with a file-handler to stdout, then you probably don't need to use the logging module at all. Consider using [Console.log](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console.log) which will render anything that you can print with Rich, with a timestamp.
