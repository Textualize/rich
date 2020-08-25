# Rich

[![PyPI version](https://badge.fury.io/py/rich.svg)](https://badge.fury.io/py/rich)
[![codecov](https://codecov.io/gh/willmcgugan/rich/branch/master/graph/badge.svg)](https://codecov.io/gh/willmcgugan/rich)
[![Rich blog](https://img.shields.io/badge/blog-rich%20news-yellowgreen)](https://www.willmcgugan.com/tag/rich/)
[![Twitter Follow](https://img.shields.io/twitter/follow/willmcgugan.svg?style=social)](https://twitter.com/willmcgugan)

[中文 readme](https://github.com/willmcgugan/rich/blob/master/README.cn.md)

Rich is a Python library for _rich_ text and beautiful formatting in the terminal.

The [Rich API](https://rich.readthedocs.io/en/latest/) makes it easy to add color and style to terminal output. Rich can also render pretty tables, progress bars, markdown, syntax highlighted source code, tracebacks, and more — out of the box.

![Features](https://github.com/willmcgugan/rich/raw/master/imgs/features.png)

For a video introduction to Rich see [calmcode.io](https://calmcode.io/rich/introduction.html) by [@fishnets88](https://twitter.com/fishnets88).

See what [people are saying about Rich](https://www.willmcgugan.com/blog/pages/post/rich-tweets/).

## Compatibility

Rich works with Linux, OSX, and Windows. True color / emoji works with new Windows Terminal, classic terminal is limited to 8 colors. Rich requires Python 3.6.1 or later.

Rich works with [Jupyter notebooks](https://jupyter.org/) with no additional configuration required.

## Installing

Install with `pip` or your favorite PyPi package manager.

```
pip install rich
```

## Rich print function

To effortlessly add rich output to your application, you can import the [rich print](https://rich.readthedocs.io/en/latest/introduction.html#quick-start) method, which has the same signature as the builtin Python function. Try this:

```python
from rich import print

print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())
```

![Hello World](https://github.com/willmcgugan/rich/raw/master/imgs/print.png)

## Rich REPL

Rich can be installed in the Python REPL, so that any data structures will be pretty printed and highlighted.

```python
>>> from rich import pretty
>>> pretty.install()
```

![REPL](https://github.com/willmcgugan/rich/raw/master/imgs/repl.png)

## Using the Console

For more control over rich terminal content, import and construct a [Console](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console) object.

```python
from rich.console import Console

console = Console()
```

The Console object has a `print` method which has an intentionally similar interface to the builtin `print` function. Here's an example of use:

```python
console.print("Hello", "World!")
```

As you might expect, this will print `"Hello World!"` to the terminal. Note that unlike the builtin `print` function, Rich will word-wrap your text to fit within the terminal width.

There are a few ways of adding color and style to your output. You can set a style for the entire output by adding a `style` keyword argument. Here's an example:

```python
console.print("Hello", "World!", style="bold red")
```

The output will be something like the following:

![Hello World](https://github.com/willmcgugan/rich/raw/master/imgs/hello_world.png)

That's fine for styling a line of text at a time. For more finely grained styling, Rich renders a special markup which is similar in syntax to [bbcode](https://en.wikipedia.org/wiki/BBCode). Here's an example:

```python
console.print("Where there is a [bold cyan]Will[/bold cyan] there [u]is[/u] a [i]way[/i].")
```

![Console Markup](https://github.com/willmcgugan/rich/raw/master/imgs/where_there_is_a_will.png)

### Console logging

The Console object has a `log()` method which has a similar interface to `print()`, but also renders a column for the current time and the file and line which made the call. By default Rich will do syntax highlighting for Python structures and for repr strings. If you log a collection (i.e. a dict or a list) Rich will pretty print it so that it fits in the available space. Here's an example of some of these features.

```python
from rich.console import Console
console = Console()

test_data = [
    {"jsonrpc": "2.0", "method": "sum", "params": [None, 1, 2, 4, False, True], "id": "1",},
    {"jsonrpc": "2.0", "method": "notify_hello", "params": [7]},
    {"jsonrpc": "2.0", "method": "subtract", "params": [42, 23], "id": "2"},
]

def test_log():
    enabled = False
    context = {
        "foo": "bar",
    }
    movies = ["Deadpool", "Rise of the Skywalker"]
    console.log("Hello from", console, "!")
    console.log(test_data, log_locals=True)


test_log()
```

The above produces the following output:

![Log](https://github.com/willmcgugan/rich/raw/master/imgs/log.png)

Note the `log_locals` argument, which outputs a table containing the local variables where the log method was called.

The log method could be used for logging to the terminal for long running applications such as servers, but is also a very nice debugging aid.

### Logging Handler

You can also use the builtin [Handler class](https://rich.readthedocs.io/en/latest/logging.html) to format and colorize output from Python's logging module. Here's an example of the output:

![Logging](https://github.com/willmcgugan/rich/raw/master/imgs/logging.png)

## Emoji

To insert an emoji in to console output place the name between two colons. Here's an example:

```python
>>> console.print(":smiley: :vampire: :pile_of_poo: :thumbs_up: :raccoon:")
😃 🧛 💩 👍 🦝
```

Please use this feature wisely.

## Tables

Rich can render flexible [tables](https://rich.readthedocs.io/en/latest/tables.html) with unicode box characters. There is a large variety of formatting options for borders, styles, cell alignment etc.

![table movie](https://github.com/willmcgugan/rich/raw/master/imgs/table_movie.gif)

The animation above was generated with [table_movie.py](https://github.com/willmcgugan/rich/blob/master/examples/table_movie.py) in the examples directory.

Here's a simpler table example:

```python
from rich.console import Console
from rich.table import Table

console = Console()

table = Table(show_header=True, header_style="bold magenta")
table.add_column("Date", style="dim", width=12)
table.add_column("Title")
table.add_column("Production Budget", justify="right")
table.add_column("Box Office", justify="right")
table.add_row(
    "Dev 20, 2019", "Star Wars: The Rise of Skywalker", "$275,000,000", "$375,126,118"
)
table.add_row(
    "May 25, 2018",
    "[red]Solo[/red]: A Star Wars Story",
    "$275,000,000",
    "$393,151,347",
)
table.add_row(
    "Dec 15, 2017",
    "Star Wars Ep. VIII: The Last Jedi",
    "$262,000,000",
    "[bold]$1,332,539,889[/bold]",
)

console.print(table)
```

This produces the following output:

![table](https://github.com/willmcgugan/rich/raw/master/imgs/table.png)

Note that console markup is rendered in the same way as `print()` and `log()`. In fact, anything that is renderable by Rich may be included in the headers / rows (even other tables).

The `Table` class is smart enough to resize columns to fit the available width of the terminal, wrapping text as required. Here's the same example, with the terminal made smaller than the table above:

![table2](https://github.com/willmcgugan/rich/raw/master/imgs/table2.png)

## Progress Bars

Rich can render multiple flicker-free [progress](https://rich.readthedocs.io/en/latest/progress.html) bars to track long-running tasks.

For basic usage, wrap any sequence in the `track` function and iterate over the result. Here's an example:

```python
from rich.progress import track

for step in track(range(100)):
    do_step(step)
```

It's not much harder to add multiple progress bars. Here's an example taken from the docs:

![progress](https://github.com/willmcgugan/rich/raw/master/imgs/progress.gif)

The columns may be configured to show any details you want. Built-in columns include percentage complete, file size, file speed, and time remaining. Here's another example showing a download in progress:

![progress](https://github.com/willmcgugan/rich/raw/master/imgs/downloader.gif)

To try this out yourself, see [examples/downloader.py](https://github.com/willmcgugan/rich/blob/master/examples/downloader.py) which can download multiple URLs simultaneously while displaying progress.

## Columns

Rich can render content in neat [columns](https://rich.readthedocs.io/en/latest/columns.html) with equal or optimal width. Here's a very basic clone of the (MacOS / Linux) `ls` command which displays a directory listing in columns:

```python
import os

from rich import print
from rich.columns import Columns

directory = os.listdir(sys.argv[1])
print(Columns(directory))
```

The following screenshot is the output from the [columns example](https://github.com/willmcgugan/rich/blob/master/examples/columns.py) which displays data pulled from an API in columns:

![columns](https://github.com/willmcgugan/rich/raw/master/imgs/columns.png)

## Markdown

Rich can render [markdown](https://rich.readthedocs.io/en/latest/markdown.html) and does a reasonable job of translating the formatting to the terminal.

To render markdown import the `Markdown` class and construct it with a string containing markdown code. Then print it to the console. Here's an example:

```python
from rich.console import Console
from rich.markdown import Markdown

console = Console()
with open("README.md") as readme:
    markdown = Markdown(readme.read())
console.print(markdown)
```

This will produce output something like the following:

![markdown](https://github.com/willmcgugan/rich/raw/master/imgs/markdown.png)

## Syntax Highlighting

Rich uses the [pygments](https://pygments.org/) library to implement [syntax highlighting](https://rich.readthedocs.io/en/latest/syntax.html). Usage is similar to rendering markdown; construct a `Syntax` object and print it to the console. Here's an example:

```python
from rich.console import Console
from rich.syntax import Syntax

my_code = '''
def iter_first_last(values: Iterable[T]) -> Iterable[Tuple[bool, bool, T]]:
    """Iterate and generate a tuple with a flag for first and last value."""
    iter_values = iter(values)
    try:
        previous_value = next(iter_values)
    except StopIteration:
        return
    first = True
    for value in iter_values:
        yield first, False, previous_value
        first = False
        previous_value = value
    yield first, True, previous_value
'''
syntax = Syntax(my_code, "python", theme="monokai", line_numbers=True)
console = Console()
console.print(syntax)
```

This will produce the following output:

![syntax](https://github.com/willmcgugan/rich/raw/master/imgs/syntax.png)

## Tracebacks

Rich can render [beautiful tracebacks](https://rich.readthedocs.io/en/latest/traceback.html) which are easier to read and show more code than standard Python tracebacks. You can set Rich as the default traceback handler so all uncaught exceptions will be rendered by Rich.

Here's what it looks like on OSX (similar on Linux):

![traceback](https://github.com/willmcgugan/rich/raw/master/imgs/traceback.png)

## Project using Rich

Here are a few projects using Rich:

- [BrancoLab/BrainRender](https://github.com/BrancoLab/BrainRender)
  a python package for the visualization of three dimensional neuro-anatomical data
- [Ciphey/Ciphey](https://github.com/Ciphey/Ciphey)
  Automated decryption tool
- [emeryberger/scalene](https://github.com/emeryberger/scalene)
  a high-performance, high-precision CPU and memory profiler for Python
- [hedythedev/StarCli](https://github.com/hedythedev/starcli)
  Browse GitHub trending projects from your command line
- [intel/cve-bin-tool](https://github.com/intel/cve-bin-tool)
  This tool scans for a number of common, vulnerable components (openssl, libpng, libxml2, expat and a few others) to let you know if your system includes common libraries with known vulnerabilities.
- [nf-core/tools](https://github.com/nf)
  Python package with helper tools for the nf-core community.
- [cansarigol/pdbr](https://github.com/cansarigol/pdbr)
  pdb + Rich library for enhanced debugging
- [plant99/felicette](https://github.com/plant99/felicette)
  Satellite imagery for dummies.
- [seleniumbase/SeleniumBase](https://github.com/seleniumbase/SeleniumBase)
  Automate & test 10x faster with Selenium & pytest. Batteries included.
- [smacke/ffsubsync](https://github.com/smacke/ffsubsync)
  Automagically synchronize subtitles with video.
- +[Many more](https://github.com/willmcgugan/rich/network/dependents)!
