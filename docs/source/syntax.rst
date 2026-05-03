Syntax
======

Rich can syntax highlight various programming languages with line numbers.

To syntax highlight code, construct a :class:`~rich.syntax.Syntax` object and print it to the console. Here's an example::

    from rich.console import Console
    from rich.syntax import Syntax

    console = Console()
    with open("syntax.py", "rt") as code_file:
        syntax = Syntax(code_file.read(), "python")
    console.print(syntax)

You may also use the :meth:`~rich.syntax.Syntax.from_path` alternative constructor which will load the code from disk and auto-detect the file type. The example above could be re-written as follows::


    from rich.console import Console
    from rich.syntax import Syntax

    console = Console()
    syntax = Syntax.from_path("syntax.py")
    console.print(syntax)


Line numbers
------------

If you set ``line_numbers=True``, Rich will render a column for line numbers::

    syntax = Syntax.from_path("syntax.py", line_numbers=True)


Theme
-----

The Syntax constructor (and :meth:`~rich.syntax.Syntax.from_path`) accept a ``theme`` attribute which should be the name of a `Pygments theme <https://pygments.org/demo/>`_. It may also be one of the special case theme names "ansi_dark" or "ansi_light" which will use the color theme configured by the terminal.


Background color
----------------

You can override the background color from the theme by supplying a ``background_color`` argument to the constructor. This should be a string in the same format a style definition accepts, e.g. "red", "#ff0000", "rgb(255,0,0)" etc. You may also set the special value "default" which will use the default background color set in the terminal.


Highlighting ranges
-------------------

You can apply custom styles to specific portions of the code with :meth:`~rich.syntax.Syntax.stylize_range`. This is useful for highlighting search results, marking errors, or drawing attention to particular lines.

The method accepts a style and a *start* and *end* position, each given as ``(line, column)`` tuples. Line numbers are **1-based** (the first line is 1) and column offsets are **0-based** (the first column is 0).

Here is an example that highlights the word ``True`` in a snippet of Python code::

    from rich.console import Console
    from rich.style import Style
    from rich.syntax import Syntax

    code = "example = True"
    syntax = Syntax(code, "python")
    syntax.stylize_range(Style(bgcolor="red"), (1, 10), (1, 14))

    console = Console()
    console.print(syntax)

This renders the code with a red background behind ``True`` (columns 10–13, inclusive of the start and exclusive of the end).

For multi-line code, increment the line number accordingly. The following example highlights ``456`` on the second line::

    code = "123\n456\n789"
    syntax = Syntax(code, "python")
    syntax.stylize_range(Style(bgcolor="red"), (2, 0), (2, 3))

You can also style a range that spans multiple lines. To highlight the entire first two lines::

    syntax.stylize_range(Style(bgcolor="red"), (1, 0), (2, 11))

.. tip::

   ``stylize_range`` can be called multiple times on the same :class:`~rich.syntax.Syntax` object to apply different styles to different parts of the code.


Syntax CLI
----------

You can use this class from the command line. Here's how you would syntax highlight a file called "syntax.py"::

    python -m rich.syntax syntax.py

For the full list of arguments, run the following::

    python -m rich.syntax -h
    
