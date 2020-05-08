Syntax
======

Rich can syntax highlight various programming languages with line numbers.

To syntax highlight code, construct a :class:`~rich.syntax.Syntax` object and print it to the console. Here's an example::


    from rich.console import console
    from rich.syntax import Syntax

    console = Console()
    syntax = Syntax.from_path("syntax.py", line_numbers=True)
    console.print(syntax)

The Syntax constructor (and :meth:`~rich.syntax.Syntax.from_path`) accept a ``theme`` attribute which should be the name of a `Pygments theme <https://pygments.org/demo/>`_.