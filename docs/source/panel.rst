Panel
=====

To draw a border around any content, construct a :class:`~rich.panel.Panel` with any *renderable* as the first positional argument. Here's an example::

    from rich import print
    from rich.panel import Panel
    print(Panel("Hello, [red]World!"))

You can change the style of the panel by setting the ``box`` argument to the Panel constructor. See :ref:`appendix-box` for a list of available box styles.