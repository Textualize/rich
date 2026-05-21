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

Style themes can make your code more semantic, for instance a style called ``"warning"`` better expresses intent than ``"italic magenta underline"``.

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


Default Styles
--------------

Rich ships with a comprehensive set of built-in styles used throughout its
various modules. These styles are stored in :class:`~rich.default_styles.DEFAULT_STYLES`
and can be used by passing the style name as a string to any Rich API that
accepts a ``style`` parameter (e.g., ``console.print("[warning]Text[/warning]")``).

The following table lists all available default style names grouped by their
area of use:

.. list-table::
    :header-rows: 1
    :widths: 30 70

    * - Style Name
      - Description
    * - **Basic**
      -
    * - ``"none"``
      - No styling (null style)
    * - ``"reset"``
      - Resets all color and style attributes to terminal defaults
    * - ``"dim"``
      - Reduced intensity (subtle/bright text)
    * - ``"bright"``
      - Full intensity (no dimming)
    * - ``"bold"``
      - Bold text weight
    * - ``"strong"``
      - Strong emphasis (bold)
    * - ``"code"``
      - Code-like appearance (bold + reverse)
    * - ``"italic"``
      - Italic text style
    * - ``"emphasize"``
      - Emphasis (italic)
    * - ``"underline"``
      - Underlined text
    * - ``"blink"``
      - Slow blinking text
    * - ``"blink2"``
      - Rapid blinking text
    * - ``"reverse"``
      - Reversed foreground/background colors
    * - ``"strike"``
      - Strikethrough text
    * - ``"black"`` / ``"red"`` / ``"green"`` / ``"yellow"`` / ``"magenta"`` / ``"cyan"`` / ``"white"``
      - Basic ANSI foreground colors
    * - **Inspect** (used by :func:`~rich.inspect.inspect`)
      -
    * - ``"inspect.attr"``
      - Regular attribute names
    * - ``"inspect.attr.dunder"``
      - Dunder (dunder) attribute names
    * - ``"inspect.callable"``
      - Callable/function names
    * - ``"inspect.async_def"``
      - Async function definitions
    * - ``"inspect.def"``
      - Regular function definitions
    * - ``"inspect.class"``
      - Class names
    * - ``"inspect.error"``
      - Error/exception types
    * - ``"inspect.equals"``
      - Equals sign in output
    * - ``"inspect.help"``
      - Help text / documentation
    * - ``"inspect.value.border"``
      - Border around inspect values
    * - **JSON Rendering**
      -
    * - ``"json.brace"``
      - JSON braces ``{`` and ``}``
    * - ``"json.bool_true"`` / ``"json.bool_false"``
      - Boolean literals
    * - ``"json.null"``
      - Null literal
    * - ``"json.number"``
      - Numeric values
    * - ``"json.str"``
      - String values
    * - ``"json.key"``
      - Object keys
    * - **Logging**
      -
    * - ``"logging.keyword"``
      - ``levelname`` in log records (e.g., "INFO", "DEBUG")
    * - ``"logging.level.notset"`` / ``"debug"`` / ``"info"`` / ``"warning"`` / ``"error"`` / ``"critical"``
      - Styles for each log level
    * - ``"log.level"``
      - Log level indicator (general)
    * - ``"log.time"``
      - Timestamp in log output
    * - ``"log.message"``
      - Log message text
    * - ``"log.path"``
      - File path in log output
    * - **Layout / Tree**
      -
    * - ``"layout.tree.row"``
      - Tree structure row styling
    * - ``"layout.tree.column"``
      - Tree column styling
    * - ``"tree"``
      - General tree styling
    * - ``"tree.line"``
      - Tree connecting lines
    * - **Live / Progress**
      -
    * - ``"live.ellipsis"``
      - Ellipsis shown during live updates
    * - ``"progress.description"``
      - Task description text
    * - ``"progress.filesize"`` / ``"progress.filesize.total"``
      - File size displays
    * - ``"progress.download"``
      - Download progress text
    * - ``"progress.elapsed"``
      - Elapsed time display
    * - ``"progress.percentage"``
      - Percentage complete
    * - ``"progress.remaining"``
      - Remaining time display
    * - ``"progress.data.speed"``
      - Data transfer speed
    * - ``"progress.spinner"``
      - Spinner character for progress
    * - ``"bar.back"`` / ``"bar.complete"`` / ``"bar.finished"`` / ``"bar.pulse"``
      - Progress bar segments
    * - ``"status.spinner"``
      - Spinner for status display
    * - **Repr / Inspect Output**
      -
    * - ``"repr.ellipsis"``
      - Truncation indicator ``...``
    * - ``"repr.indent"``
      - Indentation markers
    * - ``"repr.error"``
      - Error values
    * - ``"repr.str"``
      - String representations
    * - ``"repr.brace"`` / ``"repr.comma"``
      - Braces and commas in repr
    * - ``"repr.ipv4"`` / ``"repr.ipv6"`` / ``"repr.eui48"`` / ``"repr.eui64"``
      - Network address formats
    * - ``"repr.tag_start"`` / ``"repr.tag_name"`` / ``"repr.tag_contents"`` / ``"repr.tag_end"``
      - XML/HTML tag elements
    * - ``"repr.attrib_name"`` / ``"repr.attrib_equal"`` / ``"repr.attrib_value"``
      - Attribute name/value pairs in repr
    * - ``"repr.number"`` / ``"repr.number_complex"``
      - Numeric values in repr
    * - ``"repr.bool_true"`` / ``"repr.bool_false"``
      - Boolean literals in repr
    * - ``"repr.none"``
      - None value in repr
    * - ``"repr.url"``
      - URL strings in repr
    * - ``"repr.uuid"``
      - UUID strings in repr
    * - ``"repr.call"``
      - Callable invocation display
    * - ``"repr.path"`` / ``"repr.filename"``
      - File path display in repr
    * - **Markdown Rendering**
      -
    * - ``"markdown.paragraph"`` / ``"markdown.text"``
      - Paragraph and body text
    * - ``"markdown.em"`` / ``"markdown.emph"``
      - Emphasis/italic text
    * - ``"markdown.strong"``
      - Strong/bold text
    * - ``"markdown.code"`` / ``"markdown.code_block"``
      - Inline and block code
    * - ``"markdown.block_quote"``
      - Block quote text
    * - ``"markdown.list"`` / ``"markdown.item"`` / ``"markdown.item.bullet"`` / ``"markdown.item.number"``
      - List and list item rendering
    * - ``"markdown.h1"`` to ``"markdown.h7"`` / ``"markdown.h1.border"``
      - Heading styles (levels 1-7)
    * - ``"markdown.hr"``
      - Horizontal rule
    * - ``"markdown.link"`` / ``"markdown.link_url"``
      - Link text and URL styling
    * - ``"markdown.s"``
      - Strikethrough text
    * - ``"markdown.table.border"`` / ``"markdown.table.header"``
      - Table rendering styles
    * - ``"markdown.kbd"``
      - Keyboard input text
    * - **Rule / Separator**
      -
    * - ``"rule.line"``
      - Horizontal rule line
    * - ``"rule.text"``
      - Rule text content
    * - **Scope**
      -
    * - ``"scope.border"``
      - Scope border styling
    * - ``"scope.key"`` / ``"scope.key.special"``
      - Scope key names
    * - ``"scope.equals"``
      - Equals sign in scope display
    * - **Table**
      -
    * - ``"table.header"`` / ``"table.footer"``
      - Table header and footer rows
    * - ``"table.cell"``
      - General table cell content
    * - ``"table.title"``
      - Table caption/title
    * - ``"table.caption"``
      - Table caption (italic + dim)
    * - **Traceback**
      -
    * - ``"traceback.error"``
      - Error message text in tracebacks
    * - ``"traceback.border"`` / ``"traceback.border.syntax_error"``
      - Border styling for traceback boxes
    * - ``"traceback.text"``
      - General traceback text
    * - ``"traceback.title"``
      - Title of traceback block
    * - ``"traceback.exc_type"``
      - Exception type name
    * - ``"traceback.exc_value"``
      - Exception message value
    * - ``"traceback.offset"``
      - Line number offset display
    * - ``"traceback.error_range"``
      - Error range highlight
    * - ``"traceback.note"``
      - Note附加信息
    * - ``"traceback.group.border"``
      - Exception group border
    * - **Prompt**
      -
    * - ``"prompt"``
      - General prompt styling
    * - ``"prompt.choices"``
      - Choice options in prompts
    * - ``"prompt.default"``
      - Default selection in prompts
    * - ``"prompt.invalid"`` / ``"prompt.invalid.choice"``
      - Invalid input feedback
    * - **ISO 8601 Date/Time**
      -
    * - ``"iso8601.date"`` / ``"iso8601.time"`` / ``"iso8601.timezone"``
      - Date, time, and timezone formatting
    * - **Pretty Print**
      -
    * - ``"pretty"``
      - General pretty-printed output
    * - **Status**
      -
    * - ``"status.spinner"``
      - Spinner animation character

.. note::
    To preview all default styles rendered in your terminal, run::

        python -m rich.default_styles

    You can also override any default style by passing a custom :class:`~rich.theme.Theme`
    to the :class:`~rich.console.Console` constructor, or by modifying
    ``DEFAULT_STYLES`` directly (though this is discouraged — theme overrides
    via the ``Theme`` class are the intended extensibility point).

Loading Themes
~~~~~~~~~~~~~~

If you prefer, you can write your styles in an external config file rather than in Python. Here's an example of the format::

    [styles]
    info = dim cyan
    warning = magenta
    danger = bold red

You can read these files with the :meth:`~rich.theme.Theme.read` method.
