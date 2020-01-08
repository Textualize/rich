Console Protocol
================

Rich supports a simple protocol to add rich formatting capabilities to custom objects, so you can  :meth:`~rich.console.Console.print` your object with color, styles and formatting.

You can use this for presentation or to display additional debugging information that might be hard to parse from a ``__repr__`` output.


Console Str
-----------

The easiest way to add console output to your custom object is to implement a ``__console_str__`` method. This method accepts no arguments, and should return a :class:`~rich.text.Text` instance. Here's an example::

    class MyObject:
        def __console_str__(self) -> Text:
            return Text.from_markup("[bold]MyObject()[/bold]")

If you were to print or log an instance of ``MyObject`` it would render as ``MyObject()`` in bold. Naturally, you would want to put this to better use, perhaps by adding specialized syntax highlighting.


Console Render
--------------

The ``__console_str__`` method is limited to styled text. For more advanced rendering, Rich supports a ``__console__`` method which you can use to render custom output with other renderable objects. For instance, a complex data type might be best represented as a :class:`~rich.table.Table`.

The ``__console__`` method should accept a :class:`~rich.console.Console` and a :class:`~rich.console.ConsoleOptions` instance. It should return an iterable of other renderable objects. Although that means it *could* return a container such as a list, it is customary to ``yield`` output (making the method a generator)

Here's an example of a ``__console__`` method::

    class MyObject:
        def __console__(self, console: Console, options: ConsoleOptions) -> Iterable[Table]:
            my_table = Table("Key, "Value")
            my_table.add_row("foo", "bar")
            my_table.add_row("egg", "baz")
            yield my_table

If you were to print a ``MyObject`` instance, it would render a simple table to the terminal.
