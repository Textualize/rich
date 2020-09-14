.. _console_markup:

Console Markup
==============

Rich supports a simple markup which you can use to insert color and styles virtually everywhere Rich would accept a string (e.g. :meth:`~rich.console.Console.print` and :meth:`~rich.console.Console.log`).


Syntax
------

Console markup uses a syntax inspired by `bbcode <https://en.wikipedia.org/wiki/BBCode>`_. If you write the style (see :ref:`styles`) in square brackets, e.g. ``[bold red]``, that style will apply until it is *closed* with a corresponding ``[/bold red]``.

Here's a simple example::

    from rich import print
    print("[bold red]alert![/bold red] Something happened")

If you don't close a style, it will apply until the end of the string. Which is sometimes convenient if you want to style a single line. For example::

    print("[bold italic yellow on red blink]This text is impossible to read")

There is a shorthand for closing a style. If you omit the style name from the closing tag, Rich will close the last style. For example::

    print("[bold red]Bold and red[/] not bold or red")


Links
~~~~~

Console markup can output hyperlinks with the following syntax: ``[link=URL]text[/link]``. Here's an example::

    print("Visit my [link=https://www.willmcgugan.com]blog[/link]!")

If your terminal software supports hyperlinks, you will be able to click the word "blog" which will typically open a browser. If your terminal doesn't support hyperlinks, you will see the text but it won't be clickable.


Escaping
~~~~~~~~

Occasionally you may want to print something that Rich would interpret as markup. You can *escape* a tag by preceding it with backslash. Here's an example::

    >>> from rich import print
    >>> print("foo\[bar]")
    foo[bar]

The function :func:`~rich.markup.escape` will handle escaping of text for you.

Rendering Markup
----------------

By default, Rich will render console markup when you explicitly pass a string to :meth:`~rich.console.Print.print` or implicitly when you embed a string in another renderable object such as :class:`~rich.table.Table` or :class:`~rich.panel.Panel`.

Console markup is convenient, but you may wish to disable it if the syntax clashes with the string you want to print. You can do this by setting ``markup=False`` on the :meth:`~rich.console.Print.print` method or on the :class:`~rich.console.Console` constructor.


Markup API
----------

You can convert a string to styled text by calling :meth:`~rich.text.Text.from_markup`, which returns a :class:`~rich.text.Text` instance you can print or add more styles to.
