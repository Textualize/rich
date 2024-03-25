Padding
=======

The :class:`~rich.padding.Padding` class may be used to add whitespace around text or other renderable. The following example will print the word "Hello" with a padding of 1 character, so there will be a blank line above and below, and a space on the left and right edges::

    from rich import print
    from rich.padding import Padding
    test = Padding("Hello", 1)
    print(test)

You can specify the padding on a more granular level by using a tuple of values rather than a single value. A tuple of 2 values sets the top/bottom and left/right padding, whereas a tuple of 4 values sets the padding for top, right, bottom, and left sides. You may recognize this scheme if you are familiar with CSS.

For example, the following displays 2 blank lines above and below the text, and a padding of 4 spaces on the left and right sides::

    from rich import print
    from rich.padding import Padding
    test = Padding("Hello", (2, 4))
    print(test)

The Padding class can also accept a ``style`` argument which applies a style to the padding and contents, and an ``expand`` switch which can be set to False to prevent the padding from extending to the full width of the terminal. Here's an example which demonstrates both these arguments::

    from rich import print
    from rich.padding import Padding
    test = Padding("Hello", (2, 4), style="on blue", expand=False)
    print(test)

Note that, as with all Rich renderables, you can use Padding in any context. For instance, if you want to emphasize an item in a :class:`~rich.table.Table` you could add a Padding object to a row with a padding of 1 and a style of "on red".
