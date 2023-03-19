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


Lexers support
--------------

In most cases, the second argument in the :class:`~rich.syntax.Syntax` constructor is the name of a lexer recognized as a `Pygments lexer <https://pygments.org/docs/api/#lexers>`_.
While this interface is usually enough and provides support for all languages covered by Pygments, developers may want to create a custom lexer, although this can be done with a pygments entry point, it can be rather slow.
The better approach is to create a custom lexer and supply an instance of it directly, any valid class inheriting from `The Pygments lexer <https://pygments.org/docs/api/#pygments.lexer>`_ should suffice.


Syntax CLI
----------

You can use this class from the command line. Here's how you would syntax highlight a file called "syntax.py"::

    python -m rich.syntax syntax.py

For the full list of arguments, run the following::

    python -m rich.syntax -h
    
