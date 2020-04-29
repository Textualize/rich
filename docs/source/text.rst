.. _rich_text:

Rich Text
=========

Rich has a :class:`~rich.text.Text` class for text that may be marked up with color and style attributes. You can consider this class to be like a mutable string with additional style information. The methods on the Text() instance are similar to a Python ``str`` but are designed to preserve the styles.

One way to add a style to Text is the :meth:`~rich.text.Text.stylize` method which applies a style to a start and end offset. Here is an example::

    from rich.text import Text
    text = Text("Hello, World!")
    text.stylize(0, 6, "bold magenta")
    console.print(text)

This will print "Hello, World!" to the terminal, with the first word in bold magenta.

Alternatively, you can construct styled text by calling :meth:`~rich.text.Text.append` to add a string and style to the end of the Text. Here's an example::

    text = Text()
    text.append("Hello", style="bold magenta")
    text.append(" World!")
    console.print(text)

You can also apply a style to given words in the text with :meth:`~rich.text.Text.highlight_words` or for ultimate control call :meth:`~rich.text.Text.highlight_regex` to highlight text matching a *regular expression*.
