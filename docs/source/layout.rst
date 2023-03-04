Layout
======

Rich offers a :class:`~rich.layout.Layout` class which can be used to divide the screen area in to parts, where each part may contain independent content. It can be used with :ref:`Live` to create full-screen "applications" but may be used standalone.

To see an example of a Layout, run the following from the command line::

    python -m rich.layout

Creating layouts
----------------

To define a layout, construct a Layout object and print it::

    from rich import print
    from rich.layout import Layout

    layout = Layout()
    print(layout)

This will draw a box the size of the terminal with some information regarding the layout. The box is a "placeholder" because we have yet to add any content to it. Before we do that, let's create a more interesting layout by calling the :meth:`~rich.layout.Layout.split_column` method to divide the layout in to two sub-layouts::

    layout.split_column(
        Layout(name="upper"),
        Layout(name="lower")
    )
    print(layout)

This will divide the terminal screen in to two equal sized portions, one on top of the other. The ``name`` attribute is an internal identifier we can use to look up the sub-layout later. Let's use that to create another split, this time we will call :meth:`~rich.layout.Layout.split_row` to split the lower layout in to a row of two sub-layouts::

    layout["lower"].split_row(
        Layout(name="left"),
        Layout(name="right"),
    )
    print(layout)

You should now see the screen area divided in to 3 portions; an upper half and a lower half that is split in to two quarters.

.. raw:: html

    <pre style="font-size:90%;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="color: #000080">╭─────────────────────────────── </span><span style="color: #008000">'upper'</span><span style="color: #000080"> </span><span style="color: #000080; font-weight: bold">(</span><span style="color: #000080; font-weight: bold">84</span><span style="color: #000080"> x </span><span style="color: #000080; font-weight: bold">13</span><span style="color: #000080; font-weight: bold">)</span><span style="color: #000080"> ────────────────────────────────╮</span>
    <span style="color: #000080">│</span>                                                                                  <span style="color: #000080">│</span>
    <span style="color: #000080">│</span>                                                                                  <span style="color: #000080">│</span>
    <span style="color: #000080">│</span>                                                                                  <span style="color: #000080">│</span>
    <span style="color: #000080">│</span>                                                                                  <span style="color: #000080">│</span>
    <span style="color: #000080">│</span>                                                                                  <span style="color: #000080">│</span>
    <span style="color: #000080">│</span>          <span style="font-weight: bold">{</span><span style="color: #008000">'size'</span>: <span style="color: #800080; font-style: italic">None</span>, <span style="color: #008000">'minimum_size'</span>: <span style="color: #000080; font-weight: bold">1</span>, <span style="color: #008000">'ratio'</span>: <span style="color: #000080; font-weight: bold">1</span>, <span style="color: #008000">'name'</span>: <span style="color: #008000">'upper'</span><span style="font-weight: bold">}</span>          <span style="color: #000080">│</span>
    <span style="color: #000080">│</span>                                                                                  <span style="color: #000080">│</span>
    <span style="color: #000080">│</span>                                                                                  <span style="color: #000080">│</span>
    <span style="color: #000080">│</span>                                                                                  <span style="color: #000080">│</span>
    <span style="color: #000080">│</span>                                                                                  <span style="color: #000080">│</span>
    <span style="color: #000080">│</span>                                                                                  <span style="color: #000080">│</span>
    <span style="color: #000080">╰──────────────────────────────────────────────────────────────────────────────────╯</span>
    <span style="color: #000080">╭─────────── </span><span style="color: #008000">'left'</span><span style="color: #000080"> </span><span style="color: #000080; font-weight: bold">(</span><span style="color: #000080; font-weight: bold">42</span><span style="color: #000080"> x </span><span style="color: #000080; font-weight: bold">14</span><span style="color: #000080; font-weight: bold">)</span><span style="color: #000080"> ───────────╮╭────────── </span><span style="color: #008000">'right'</span><span style="color: #000080"> </span><span style="color: #000080; font-weight: bold">(</span><span style="color: #000080; font-weight: bold">42</span><span style="color: #000080"> x </span><span style="color: #000080; font-weight: bold">14</span><span style="color: #000080; font-weight: bold">)</span><span style="color: #000080"> ───────────╮</span>
    <span style="color: #000080">│</span>                                        <span style="color: #000080">││</span>                                        <span style="color: #000080">│</span>
    <span style="color: #000080">│</span>                                        <span style="color: #000080">││</span>                                        <span style="color: #000080">│</span>
    <span style="color: #000080">│</span>                                        <span style="color: #000080">││</span>                                        <span style="color: #000080">│</span>
    <span style="color: #000080">│</span>         <span style="font-weight: bold">{</span>                              <span style="color: #000080">││</span>         <span style="font-weight: bold">{</span>                              <span style="color: #000080">│</span>
    <span style="color: #000080">│</span>             <span style="color: #008000">'size'</span>: <span style="color: #800080; font-style: italic">None</span>,              <span style="color: #000080">││</span>             <span style="color: #008000">'size'</span>: <span style="color: #800080; font-style: italic">None</span>,              <span style="color: #000080">│</span>
    <span style="color: #000080">│</span>             <span style="color: #008000">'minimum_size'</span>: <span style="color: #000080; font-weight: bold">1</span>,         <span style="color: #000080">││</span>             <span style="color: #008000">'minimum_size'</span>: <span style="color: #000080; font-weight: bold">1</span>,         <span style="color: #000080">│</span>
    <span style="color: #000080">│</span>             <span style="color: #008000">'ratio'</span>: <span style="color: #000080; font-weight: bold">1</span>,                <span style="color: #000080">││</span>             <span style="color: #008000">'ratio'</span>: <span style="color: #000080; font-weight: bold">1</span>,                <span style="color: #000080">│</span>
    <span style="color: #000080">│</span>             <span style="color: #008000">'name'</span>: <span style="color: #008000">'left'</span>             <span style="color: #000080">││</span>             <span style="color: #008000">'name'</span>: <span style="color: #008000">'right'</span>            <span style="color: #000080">│</span>
    <span style="color: #000080">│</span>         <span style="font-weight: bold">}</span>                              <span style="color: #000080">││</span>         <span style="font-weight: bold">}</span>                              <span style="color: #000080">│</span>
    <span style="color: #000080">│</span>                                        <span style="color: #000080">││</span>                                        <span style="color: #000080">│</span>
    <span style="color: #000080">│</span>                                        <span style="color: #000080">││</span>                                        <span style="color: #000080">│</span>
    <span style="color: #000080">│</span>                                        <span style="color: #000080">││</span>                                        <span style="color: #000080">│</span>
    <span style="color: #000080">╰────────────────────────────────────────╯╰────────────────────────────────────────╯</span>
    </pre>

You can continue to call split() in this way to create as many parts to the screen as you wish.

Setting renderables
-------------------

The first position argument to ``Layout`` can be any Rich renderable, which will be sized to fit within the layout's area. Here's how we might divide the "right" layout in to two panels::

    from rich.panel import Panel
    
    layout["right"].split(
        Layout(Panel("Hello")),
        Layout(Panel("World!"))
    )

You can also call :meth:`~rich.layout.Layout.update` to set or replace the current renderable::

    layout["left"].update(
        "The mystery of life isn't a problem to solve, but a reality to experience."
    )
    print(layout)

Fixed size
----------

You can set a layout to use a fixed size by setting the ``size`` argument on the Layout constructor or by setting the attribute. Here's an example::

    layout["upper"].size = 10
    print(layout)

This will set the upper portion to be exactly 10 rows, no matter the size of the terminal. If the parent layout is horizontal rather than vertical, then the size applies to the number of characters rather that rows.

Ratio
-----

In addition to a fixed size, you can also make a flexible layout setting the ``ratio`` argument on the constructor or by assigning to the attribute. The ratio defines how much of the screen the layout should occupy in relation to other layouts. For example, let's reset the size and set the ratio of the upper layout to 2::

    layout["upper"].size = None
    layout["upper"].ratio = 2
    print(layout)

This makes the top layout take up two thirds of the space. This is because the default ratio is 1, giving the upper and lower layouts a combined total of 3. As the upper layout has a ratio of 2, it takes up two thirds of the space, leaving the remaining third for the lower layout.

A layout with a ratio set may also have a minimum size to prevent it from getting too small. For instance, here's how we could set the minimum size of the lower sub-layout so that it won't shrink beyond 10 rows::

    layout["lower"].minimum_size = 10

Visibility
----------

You can make a layout invisible by setting the ``visible`` attribute to False. Here's an example::

    layout["upper"].visible = False
    print(layout)

The top layout is now invisible, and the "lower" layout will expand to fill the available space. Set ``visible`` to True to bring it back::

    layout["upper"].visible = True
    print(layout)

You could use this to toggle parts of your interface based on your application's configuration.

Tree
----

To help visualize complex layouts you can print the ``tree`` attribute which will display a summary of the layout as a tree::

    print(layout.tree)


Example
-------

See `fullscreen.py <https://github.com/willmcgugan/rich/blob/master/examples/fullscreen.py>`_ for an example that combines :class:`~rich.layout.Layout` and :class:`~rich.live.Live` to create a fullscreen "application".
