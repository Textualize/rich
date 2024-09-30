.. _styles:


Styles
======

In various places in the Rich API you can set a "style" which defines the color of the text and various attributes such as bold, italic etc. A style may be given as a string containing a *style definition* or as an instance of a :class:`~rich.style.Style` class.


Defining Styles
---------------

A style definition is a string containing one or more words to set colors and attributes.

To specify a foreground color use one of the 256 :ref:`appendix-colors`. For example, to print "Hello" in magenta::

    console.print("Hello", style="magenta")

You may also use the color's number (an integer between 0 and 255) with the syntax ``"color(<number>)"``. The following will give the equivalent output::

    console.print("Hello", style="color(5)")

Alternatively you can use a CSS-like syntax to specify a color with a "#" followed by three pairs of hex characters, or in RGB form with three decimal integers. The following two lines both print "Hello" in the same color (purple)::

    console.print("Hello", style="#af00ff")
    console.print("Hello", style="rgb(175,0,255)")

The hex and rgb forms allow you to select from the full *truecolor* set of 16.7 million colors.

.. note::
    Some terminals only support 256 colors. Rich will attempt to pick the closest color it can if your color isn't available.

By itself, a color will change the *foreground* color. To specify a *background* color, precede the color with the word "on". For example, the following prints text in red on a white background::

    console.print("DANGER!", style="red on white")

You can also set a color with the word ``"default"`` which will reset the color to a default managed by your terminal software. This works for backgrounds as well, so the style of ``"default on default"`` is what your terminal starts with.

You can set a style attribute by adding one or more of the following words:

* ``"bold"`` or ``"b"`` for bold text.
* ``"blink"`` for text that flashes (use this one sparingly).
* ``"blink2"`` for text that flashes rapidly (not supported by most terminals).
* ``"conceal"`` for *concealed* text (not supported by most terminals).
* ``"italic"`` or ``"i"`` for italic text (not supported on Windows).
* ``"reverse"`` or ``"r"`` for text with foreground and background colors reversed.
* ``"strike"`` or ``"s"`` for text with a line through it.
* ``"underline"`` or ``"u"`` for underlined text.

Rich also supports the following styles, which are not well supported and may not display in your terminal:

* ``"underline2"`` or ``"uu"`` for doubly underlined text.
* ``"frame"`` for framed text.
* ``"encircle"`` for encircled text.
* ``"overline"`` or ``"o"`` for overlined text.

Style attributes and colors may be used in combination with each other. For example::

    console.print("Danger, Will Robinson!", style="blink bold red underline on white")

Styles may be negated by prefixing the attribute with the word "not". This can be used to turn off styles if they overlap. For example::

    console.print("foo [not bold]bar[/not bold] baz", style="bold")

This will print "foo" and "baz" in bold, but "bar" will be in normal text.

Styles may also have a ``"link"`` attribute, which will turn any styled text in to a *hyperlink* (if supported by your terminal software).

To add a link to a style, the definition should contain the word ``"link"`` followed by a URL. The following example will make a clickable link::

    console.print("Google", style="link https://google.com")

.. note::
    If you are familiar with HTML you may find applying links in this way a little odd, but the terminal considers a link to be another attribute just like bold, italic etc. 
    


Style Class
-----------

Ultimately the style definition is parsed and an instance of a :class:`~rich.style.Style` class is created. If you prefer, you can use the Style class in place of the style definition. Here's an example::

    from rich.style import Style
    danger_style = Style(color="red", blink=True, bold=True)
    console.print("Danger, Will Robinson!", style=danger_style)

It is slightly quicker to construct a Style class like this, since a style definition takes a little time to parse -- but only on the first call, as Rich will cache parsed style definitions.

Styles may be combined by adding them together, which is useful if you want to modify attributes of an existing style. Here's an example::

    from rich.console import Console
    from rich.style import Style
    console = Console()

    base_style = Style.parse("cyan")
    console.print("Hello, World", style = base_style + Style(underline=True))

You can parse a style definition explicitly with the :meth:`~rich.style.Style.parse` method, which accepts the style definition and returns a Style instance. For example, the following two lines are equivalent::
    
    style = Style(color="magenta", bgcolor="yellow", italic=True)
    style = Style.parse("italic magenta on yellow")

.. _themes:


Style Themes
------------

If you reuse styles it can be a maintenance headache if you ever want to modify an attribute or color -- you would have to change every line where the style is used. Rich provides a :class:`~rich.theme.Theme` class which you can use to define custom styles that you can refer to by name. That way you only need to update your styles in one place.

Style themes can make your code more semantic, for instance a style called ``"warning"`` better expresses intent that ``"italic magenta underline"``.

To use a style theme, construct a :class:`~rich.theme.Theme` instance and pass it to the :class:`~rich.console.Console` constructor. Here's an example::

    from rich.console import Console
    from rich.theme import Theme
    custom_theme = Theme({
        "info": "dim cyan",
        "warning": "magenta",
        "danger": "bold red"
    })
    console = Console(theme=custom_theme)
    console.print("This is information", style="info")
    console.print("[warning]The pod bay doors are locked[/warning]")
    console.print("Something terrible happened!", style="danger")


.. note::
    style names must be lower case, start with a letter, and only contain letters or the characters ``"."``, ``"-"``, ``"_"``.


Customizing Defaults
~~~~~~~~~~~~~~~~~~~~

The Theme class will inherit the default styles built-in to Rich. If your custom theme contains the name of an existing style, it will replace it. This allows you to customize the defaults as easily as you can create your own styles. For instance, here's how you can change how Rich highlights numbers::

    from rich.console import Console
    from rich.theme import Theme
    console = Console(theme=Theme({"repr.number": "bold green blink"}))
    console.print("The total is 128")

You can disable inheriting the default theme by setting ``inherit=False`` on the :class:`rich.theme.Theme` constructor.

To see the default theme, run the following commands::

    python -m rich.theme
    python -m rich.default_styles


Loading Themes
~~~~~~~~~~~~~~

If you prefer, you can write your styles in an external config file rather than in Python. Here's an example of the format::

    [styles]
    info = dim cyan
    warning = magenta
    danger = bold red

You can read these files with the :meth:`~rich.theme.Theme.read` method.
