Console Markup
==============

Rich supports a simple markup which you can use to insert color and styles virtually everywhere Rich would accept a string (e.g. :meth:`~rich.console.Console.print` and :meth:`~rich.console.Console.log`).


Formatting
----------

for bold, italic, and strikethrough, Rich uses the same convention as Markdown::

For italics, wrap text in asterisks or underscores. e.g. ``*this is italics*`` or ``_this is also italics_``.

For bold, wrap the text in *two* asterisks or underscores. e.g. ``**this is bold**``or ``__this is also bold__``.

For strikethrough, wrap the text in tildes. e.g. ``~this has a line through it~``.

For code, wrap the text in backticks. e.g. ```import this```


Styles
------

For other styles and color, you can use a syntax similar to bbcode. If you write the style in square brackets, i.e. ``[bold red]``, that style will apply when it is *closed* with a corrensponding ``[/bold red]``.



Example
-------

Here's a simple example::

    from rich import print
    print("Hello, **World**!")
    print("[bold red]alert![/bold red] *Something happened*")
