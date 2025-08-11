Markdown
========

Rich can render Markdown to the console. To render markdown, construct a :class:`~rich.markdown.Markdown` object then print it to the console. Markdown is a great way of adding rich content to your command line applications. Here's an example of use::

    MARKDOWN = """
    # This is an h1

    Rich can do a pretty *decent* job of rendering markdown.

    1. This is a list item
    2. This is another list item
    """
    from rich.console import Console
    from rich.markdown import Markdown

    console = Console()
    md = Markdown(MARKDOWN)
    console.print(md)

Note that code blocks are rendered with full syntax highlighting!

Justification
-------------

You can control the alignment of both paragraphs and headers in Markdown using the ``justify`` and ``justify_headers`` parameters respectively.

Here's an example showing different justification options::

    from rich.console import Console
    from rich.markdown import Markdown

    console = Console(width=60)

    markdown_text = """
    # Left Justified Header

    This paragraph will be center justified, while the header above is left justified.

    ## Right Justified Subheader

    This paragraph will be right justified, while the subheader above is right justified.
    """

    # Left-justify headers, center-justify paragraphs
    md = Markdown(markdown_text, justify="center", justify_headers="left")
    console.print(md)

    # Right-justify headers, right-justify paragraphs
    md = Markdown(markdown_text, justify="right", justify_headers="right")
    console.print(md)

The ``justify`` parameter controls paragraph alignment and accepts ``"left"``, ``"center"``, or ``"right"``. The ``justify_headers`` parameter controls header alignment with the same options. If not specified, paragraphs default to left alignment and headers default to center alignment.

You can also use the Markdown class from the command line. The following example displays a readme in the terminal::

    python -m rich.markdown README.md

Run the following to see the full list of arguments for the markdown command::

    python -m rich.markdown -h
