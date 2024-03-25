Panel
=====

To draw a border around text or other renderable, construct a :class:`~rich.panel.Panel` with the renderable as the first positional argument. Here's an example::

    from rich import print
    from rich.panel import Panel
    print(Panel("Hello, [red]World!"))

You can change the style of the panel by setting the ``box`` argument to the Panel constructor. See :ref:`appendix_box` for a list of available box styles.

Panels will extend to the full width of the terminal. You can make panel *fit* the content by setting ``expand=False`` on the constructor, or by creating the Panel with :meth:`~rich.panel.Panel.fit`. For example::

    from rich import print
    from rich.panel import Panel
    print(Panel.fit("Hello, [red]World!"))

The Panel constructor accepts a ``title`` argument which will draw a title on the top of the panel, as well as a ``subtitle`` argument which will draw a subtitle on the bottom of the panel::

    from rich import print
    from rich.panel import Panel
    print(Panel("Hello, [red]World!", title="Welcome", subtitle="Thank you"))

See :class:`~rich.panel.Panel` for details how to customize Panels.
