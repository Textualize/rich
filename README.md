# Rich

Rich is a Python library for _rich_ text and advanced formatting to the terminal. Rich provided an easy to use API for colored text (up to 16.7million colors) with bold / italic / underline etc. and a number of more sophisticated formatting options, such as syntax / regex highlighting, emoji, tables, and markdown rendering.

Rich is also a _framework_ in that it implements a simple protocol which you may use to make custom objects renderable with advanced terminal formatting.

## Installing

Rich may be installed with pip or your favorite PyPi package manager.

```
pip install rich
```

## Basic Usage

The first step to using the rich console is to import and construct the `Console` object.

```python
from rich.console import Console

console = Console()
```

Most applications will require one `Console` instance. The easiest way to manage your console instance would be to construct an instance at the module level and import it where needed.

The Console object has a `print` method which has an intentionally similar interface to the builtin `print` function. Here's an example of use:

```
console.print("Hello", "World!")
```

As you might expect, this will print `"Hello World!"` to the terminal. The only difference from the `print` function is that the output is word-wrapped by default (Rich auto-detects the width of the terminal).

There are a few ways of adding color and style to your output. You can set a style for the entire output, by adding a `style` keyword argument. Here's an example:

```
console.print("Hello", "World!", style="bold red")
```

The output will be something like the following:

<code>
        <pre style="font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="color: #800000; font-weight: bold">Hello World! 
</span></pre>
    </code>

That's fine for styling a line of text at a time. For more finely grained styling, Rich renders a special markup which is similar in syntax to [bbcode](https://en.wikipedia.org/wiki/BBCode). Here's an example:

```python
console.print("Where there is a [b]Will[/b] there is a [i]way[/i].")
```

<code>
        <pre style="font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">
Where there is a <span style="font-weight: bold">Will</span> there is a <span style="font-style: italic">way</span>. 
</pre>
    </code>

## Emoji

Rich supports a simple way of inserting emoji in to terminal output, by using the name of the emoji between two colons. Here's an example:

```python
console.print(":smiley: :vampire: :pile_of_poo: :thumbs_up: :raccoon:")
```

<code>
        <pre style="font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">😃 🧛 💩 👍 🦝 
</pre>
    </code>

Please use this feature wisely.
