.. _rich_text:

Rich Text
=========

Rich has a :class:`~rich.text.Text` class you can use to mark up strings with color and style attributes. You can consider this class to be like a mutable string which also contains style information.

One way to add a style to Text is the :meth:`~rich.text.Text.stylize` method which applies a style to a start and end offset. Here is an example::

    from rich.text import Text
    text = Text("Hello, World!")
    text.stylize("bold magenta", 0, 6)
    console.print(text)

This will print "Hello, World!" to the terminal, with the first word in bold magenta.

Alternatively, you can construct styled text by calling :meth:`~rich.text.Text.append` to add a string and style to the end of the Text. Here's an example::

    text = Text()
    text.append("Hello", style="bold magenta")
    text.append(" World!")
    console.print(text)

Since building Text instances from parts is a common requirement, Rich offers :meth:`~rich.text.Text.assemble` which will combine strings or pairs of string and Style, and return a Text instance. The follow example is equivalent to the code above::

    text = Text.assemble(("Hello", "bold magenta"), " World!")
    console.print(text)

You can apply a style to given words in the text with :meth:`~rich.text.Text.highlight_words` or for ultimate control call :meth:`~rich.text.Text.highlight_regex` to highlight text matching a *regular expression*. 


Text attributes
~~~~~~~~~~~~~~~

The Text class has a number of parameters you can set on the constructor to modify how the text is displayed.

- ``justify`` should be "left", "center", "right", or "full", and will override default justify behavior.
- ``overflow`` should be "fold", "crop", or "ellipsis", and will override default overflow.
- ``no_wrap`` prevents wrapping if the text is longer then the available width.
- ``tab_size`` Sets the number of characters in a tab.

A Text instance may be used in place of a plain string virtually everywhere in the Rich API, which gives you a lot of control in how text renders within other Rich renderables. For instance, the following example right aligns text within a :class:`rich.panel.Panel`::

    from rich import print
    from rich.panel import Panel
    from rich.text import Text
    panel = Panel(Text("Hello", justify="right"))
    print(panel)


