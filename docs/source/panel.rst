Panel
=====

To draw a border around any content construct a :class:`~rich.panel.Panel` object, with any *renderable* as the first positional argument. Here's an example::

    from rich import print
    from rich.panel import Panel
    print(Panel("Hello, [red]World!"))

You can draw a panel around anything that Rich knows how to render.