.. _styles:


Styles
======

In various places in the Rich API you can set a "style" which defines the color of the text and various attributes such as bold, italic etc. A style may be given as a string containing a *style definition* or as in instance of a :class:`~rich.style.Style` class.


Defining Styles
---------------

A style definition is a string containing one or more words to set colors and attributes.

To specify a foreground color use one of the 256 :ref:`appendix-colors`. For example, to print "Hello" in magenta::

    console.print("Hello", style="magenta")

You may also use the color's number (an integer between 0 and 255). The following will give the equivalent output::

    console.print("Hello", style="5")

Alteratively you can use a CSS-like syntax to specify a color with a "#" followed by three pairs of hex characters, or in RGB form with three decimal integers. The following two lines both print "Hello" in the same color (purple)::

    console.print("Hello", style="#af00ff")
    console.print("Hello", style="rgb(175,0,255)")

The hex and rgb forms allow you to select from the full *truecolor* set of 16.7 million colors.

.. note::
    Some terminals only support 256 colors. Rich will attempt to pick the closest color it can if your color isn't available.


By itself, a color will change the *foreground* color. To specify a *background* color precede the color with the word "on". For example, the following prints text in red on a white background::

    console.print("DANGER!", style="white on red")

You can set a style attribute by adding one or more of the following words:

* ``"bold"`` For bold text.
* ``"blink"`` For text that flashes (use this one sparingly).
* ``"conceal"`` For *concealed* text (not supported by many terminals).
* ``"italic"`` For italic text.
* ``"reverse"`` For text with foreground and background colors reversed.
* ``"strike"`` For text with a line through it.
* ``"underline"`` For underlined text.

Style attributes and colors may be used in combination with each other. For example::

    console.print("Danger, Will Robinson!", style="blink bold red underline on white")


Style Class
-----------

Ultimately the style definition is parsed and an instance of a :class:`~rich.style.Style` class is created. If you prefer, you can use the Style class in place of the style definition. Here's an example::

    from rich.style import Style
    console.print("Danger, Will Robinson!", style=Style(color="red", blink=True, bold=True)

It is slightly quicker to construct a Style class like this, since a style definition takes a little time to parse -- but only on the first call, as Rich will cache any style definitions it parses.

You can parse a style definition explicitly with the :meth:`~rich.style.Style.parse` method.

