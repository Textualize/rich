Layout
======

Rich offers a :class:`~rich.layout.Layout` renderable which can be used to divide the screen area in to parts where each part may contain another renderable. It is most often used with :ref:`Live` to create full-screen "applications", but may be used standalone.

To see an example of a Layout, run the following from the command line::

    python -m rich.layout

To define a layout, construct a Layout object and print it::

    from rich import print
    from rich.layout import Layout

    layout  = Layout()
    print(layout)

This will draw a box the size of the terminal with some information regarding the layout. The box is a "placeholder" because we have yet to add any content to it. Before we do that, we can call the :meth:`~rich.layout.Layout.split` method to divide the layout in to two parts::

    layout.split(name="upper")
    layout.split(name="lower", direction="horizontal")
    print(layout)

This will divide the terminal screen in to two equal sized portions one on top of the other. The ``direction="horizontal"`` argument tells the Layout class that further splits should be stacked left-to-right rather than top-to-bottom. The `name` attribute is an internal identifier we can use to look up the sub-layout later. Let's use that to create another split::

    layout["lower"].split(name="left")
    layout["lower"].split(name="right")
    print(layout)

You should now see the screen area divided in to 3 portions; An upper half and a lower half that is split in to two left and right quarter portions. You can continue to call split() create as many parts to the screen as you wish.

Setting renderables
-------------------

The Layout class would not be that useful if it only displayed placeholders. Fortunately we can tell the layout (or sub-layout) to display text or any other Rich renderable in it's portion of the screen area. To set a renderable, call :meth:`~rich.layout.Layout.update` with your renderable. Here is an example::

    layout["left"].update("The mystery of life isn't a problem to solve, but a reality to experience.")
    print(layout)

Fixed size
----------

You can set a sub-layout to use a fixed size by setting the ``size`` argument on :meth:`~rich.layout.Layout.split` or by setting the attribute layout. Here's an example::

    layout["upper"].size = 10
    print(layout)

This will set the upper portion to be exactly 10 rows, no matter the size of the terminal.

Ratio
-----

In addition to a fixed size, you can also assign a ratio* to a Layout which defines how much of the screen the layout should occupy in relation to other layouts. For example, lets reset the size and set the ratio of the upper layout to 2::

    layout["upper"].size = None
    layout["upper"].ratio = 2
    print(layout)

This makes the top layout take up two thirds of the space and the two lower layouts the remaining third. This is because the default ratio is 1, giving the upper and lower layouts a combined total of 3.

Visibility
----------

By default layouts are visible, but you can make a layout invisible by setting the ``visible`` attribute to False. Here's an example::

    layout["upper"].visible = False
    print(layout)

This has made the top layout invisible, and the "lower" layout expands to fill the available space. Set ``visible`` to True to bring it back::

    layout["upper"].visible = True
    print(layout)

Tree
----

To help visualize complex layouts you can print the ``tree`` attribute which will display a summary of the layout with a tree::

    print(layout.tree)

