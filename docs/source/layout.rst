Layout
======

Rich offers a :class:`~rich.layout.Layout` class which can be used to divide the screen area in to parts, where each part can contain its own content. It is typically used with :ref:`Live` to create full-screen "applications", but may be used standalone.

To see an example of a Layout, run the following from the command line::

    python -m rich.layout

Creating layouts
----------------

To define a layout, construct a Layout object and print it::

    from rich import print
    from rich.layout import Layout

    layout  = Layout()
    print(layout)

This will draw a box the size of the terminal with some information regarding the layout. The box is a "placeholder" because we have yet to add any content to it. Before we do that, we can call the :meth:`~rich.layout.Layout.split` method to divide the layout in to two sub-layouts::

    layout.split(
        Layout(name="upper"),
        Layout(name="lower")
    )    
    print(layout)

This will divide the terminal screen in to two equal sized portions, one on top of the other. The ``name`` attribute is an internal identifier we can use to look up the sub-layout later. Let's use that to create another split::

    layout["lower"].split(
        Layout(name="left"),
        Layout(name="right"),
        direction="horizontal"
    )    
    print(layout)

The addition of the ``direction="horizontal"`` tells the Layout class to split left-to-right, rather than the default of top-to-bottom.

You should now see the screen area divided in to 3 portions; An upper half and a lower half that is split in to two quarters. You can continue to call split() in this way to create as many parts to the screen as you wish.

Setting renderables
-------------------

The Layout class would not be that useful if it only displayed placeholders. Fortunately we can tell the layout (or sub-layout) to display text or any other renderable in it's area of the screen by calling  :meth:`~rich.layout.Layout.update`. Here is an example::

    layout["left"].update("The mystery of life isn't a problem to solve, but a reality to experience.")
    print(layout)

Fixed size
----------

You can set a sub-layout to use a fixed size by setting the ``size`` argument on the Layout constructor or by setting the attribute layout. Here's an example::

    layout["upper"].size = 10
    print(layout)

This will set the upper portion to be exactly 10 rows, no matter the size of the terminal. If the parent layout is horizontal rather than vertical, then the size applies to the number of characters rather that rows.

Ratio
-----

In addition to a fixed size, you can also assign a *ratio* to a Layout in the constructor or by assigning to the attribute. The ratio defines how much of the screen the layout should occupy in relation to other layouts. For example, lets reset the size and set the ratio of the upper layout to 2::

    layout["upper"].size = None
    layout["upper"].ratio = 2
    print(layout)

This makes the top layout take up two thirds of the space. This is because the default ratio is 1, giving the upper and lower layouts a combined total of 3. As the upper layout has a ratio of 2, it takes up two thirds of the space, leaving the remaining third for the lower layout.

A layout with a ratio set may also have a minimum size to prevent it from getting too small. For instance, here's how we could set the minimum size of the lower sub-layout so that it won't shrink beyond 10 rows::

    layout["lower"].minimum_size = 10

Visibility
----------

Sub-layouts are visible by default, but you can make a layout invisible by setting the ``visible`` attribute to False. Here's an example::

    layout["upper"].visible = False
    print(layout)

The top layout is now invisible, and the "lower" layout will expand to fill the available space. Set ``visible`` to True to bring it back::

    layout["upper"].visible = True
    print(layout)

Tree
----

To help visualize complex layouts you can print the ``tree`` attribute which will display a summary of the layout with a tree::

    print(layout.tree)

