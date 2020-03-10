.. _console_markup:

Console Markup
==============

Rich supports a simple markup which you can use to insert color and styles virtually everywhere Rich would accept a string (e.g. :meth:`~rich.console.Console.print` and :meth:`~rich.console.Console.log`).


Syntax
------

Console markup uses a syntax inspired by [bbcode](https://en.wikipedia.org/wiki/BBCode). If you write the style (see :ref:`styles`) in square brackets, i.e. ``[bold red]``, that style will apply until it is *closed* with a corresponding ``[/bold red]``.

Here's a simple example::

    from rich import print
    print("[bold red]alert![/bold red] *Something happened*")

If you don't close a style, it will apply until the end of the string. Which is sometimes convenient if you want to style a single line. For example::

    print("[bold italic yellow on red blink]This text is impossible to read")

There is a shorthand for closing a style. If you omit the style name from the closing tag, Rich will close the last style. For example::

    print("[bold red]Bold and red[/] not bold or red")

