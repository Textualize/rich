[！[PyPI版本]（https://badge.fury.io/py/rich.svg）]（https://badge.fury.io/py/rich）
[！[PyPI]（https://img.shields.io/pypi/pyversions/rich.svg）]（https://pypi.org/project/rich/）
[！[下载]（https://pepy.tech/badge/rich/month）]（https://pepy.tech/project/rich/month）
[！[Awesome]（https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg）]（https://awesome-python.com/#command-line-interface-development）

[！[Rich 博客]（https://img.shields.io/badge/blog-rich%20news-yellowgreen）]（https://www.willmcgugan.com/tag/rich/）
[！[推特关注]（https://img.shields.io/twitter/follow/willmcgugan.svg?style=social）]（https://twitter.com/willmcgugan）

＃Rich

Rich是一个Python库，可以为您在终端中提供富文本和精美格式。

[Rich API]（https://rich.readthedocs.io/en/latest/）可以很容易的在终端输出添加各种颜色和不同风格。Rich还可以绘制漂亮的表格，进度条，markdown，突出显示语法的源代码及回溯等等，不胜枚举。

！[功能纵览]（https://github.com/willmcgugan/rich/raw/master/imgs/features.png）

有关Rich的视频介绍，请参见
[@ fishnets88]（https://twitter.com/fishnets88）录制的
[calmcode.io]（https://calmcode.io/rich/introduction.html）。

##兼容性

Rich适用于Linux，OSX和Windows。真彩色/表情符号可与新的Windows终端一起使用，Windows的经典终端仅限8种颜色。

Rich还可以与[Jupyter笔记本]（https://jupyter.org/）一起使用，而无需其他配置。

##安装说明

使用`pip`或其他PyPi软件包管理器进行安装。


```
pip install rich
```

##Rich的打印功能

想毫不费力地将Rich的输出功能添加到您的应用程序中，您只需导入[rich 打印]（https://rich.readthedocs.io/en/latest/introduction.html#quick-start）方法，该方法和其他Python的自带功能的参数类似。
您可以试试：

```python
from rich import print

print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())
```

！[Hello World]（https://github.com/willmcgugan/rich/raw/master/imgs/print.png）

##使用控制台

想要对Rich终端内容进行更多控制，请您导入并构造一个[控制台]（https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console）对象。

```python
from rich.console import Console

console = Console()
```
Console对象含有一个`print` 方法，它的界面与python内置的`print`功能界面相似。

您可以试试：

```python
console.print("Hello", "World!")
```

您可能已经料到，这时终端上会显示“ Hello World！”。请注意，与内置的“打印”功能不同，Rich会将文字自动换行以适合终端宽度。

有几种方法可以为输出添加颜色和样式。您可以通过添加`style`关键字参数来为整个输出设置样式。例子如下：

```python
console.print("Hello", "World!", style="bold red")
```

输出如下图：

！[Hello World]（https://github.com/willmcgugan/rich/raw/master/imgs/hello_world.png）

这个范例一次只设置了一行文字的样式。如果想获得更细腻更复杂的样式，Rich可以渲染一个特殊的标记，其语法类似于[bbcode]（https://en.wikipedia.org/wiki/BBCode）。示例如下：

```python
console.print("Where there is a [bold cyan]Will[/bold cyan] there [u]is[/u] a [i]way[/i].")
```

！[控制台标记]（https://github.com/willmcgugan/rich/raw/master/imgs/where_there_is_a_will.png）

###控制台记录

Console对象具有一个`log()`方法，该方法具有与`print()`类似的界面，除此之外，还能成列显示当前时间以及被调用的文件和行。默认情况下，Rich将针对Python结构和repr字符串进行语法突出显示。如果您记录一个集合（如字典或列表），Rich会把它漂亮地打印出来，使其切合可用空间。下面是其中一些功能的示例：

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

以上范例的输出如下：

！[日志]（https://github.com/willmcgugan/rich/raw/master/imgs/log.png）

注意其中的`log_locals`参数会输出一个表格，该表格包含调用log方法的局部变量。

log方法既可用于将长时间运行应用程序（例如服务器）的日志记录到终端，也可用于辅助调试。

###记录处理程序

您还可以使用内置的[处理类]（https://rich.readthedocs.io/en/latest/logging.html）来对Python日志记录模块的输出进行格式化和着色。下面是输出示例：

！[记录]（https://github.com/willmcgugan/rich/raw/master/imgs/logging.png）

##表情符号
将名称放在两个冒号之间即可在控制台输出中插入表情符号。示例如下：

```python
>>> console.print(":smiley: :vampire: :pile_of_poo: :thumbs_up: :raccoon:")
😃 🧛 💩 👍 🦝
```

请谨慎地使用此功能。

##表格

Rich可以使用Unicode框字符来呈现多变的[表格]（https://rich.readthedocs.io/en/latest/tables.html）。Rich包含多种边框，样式，单元格对齐等格式设置的选项。下面是一个简单的示例：

```python
from rich.console import Console
from rich.table import Column, Table

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

该示例的输出如下：

！[表格]（https://github.com/willmcgugan/rich/raw/master/imgs/table.png）

请注意，控制台标记的呈现方式与`print（）`和`log（）`相同。实际上，由Rich渲染的任何内容都可以添加到标题/行（甚至其他表格）中。

`Table`类很聪明，可以调整列的大小以适合终端的可用宽度，并能根据需要环绕文本。下面是相同的示例，输出与比上表小的终端上：

！[表格2]（https://github.com/willmcgugan/rich/raw/master/imgs/table2.png）

##进度条

Rich可以渲染多个不闪烁的[进度]（https://rich.readthedocs.io/en/latest/progress.html）条形图，以跟踪长时间运行的任务。

基本用法：用`track`函数调用任何程序并迭代结果。下面是一个例子：

```python
from rich.progress import track

for step in track(range(100)):
    do_step(step)
```

添加多个进度条并不难。以下是从文档中获取的示例：

！[进度]（https://github.com/willmcgugan/rich/raw/master/imgs/progress.gif）

这些列可以配置为显示您所需的任何详细信息。内置列包括完成百分比，文件大小，文件速度和剩余时间。下面是显示正在进行的下载的示例：

！[进度]（https://github.com/willmcgugan/rich/raw/master/imgs/downloader.gif）

要自己尝试一下，请参阅[examples/downloader.py]（https://github.com/willmcgugan/rich/blob/master/examples/downloader.py），它可以在显示进度的同时下载多个URL。

＃＃ 列

Rich可以将内容通过排列整齐的，具有相等或最佳的宽度的[列]（https://rich.readthedocs.io/en/latest/columns.html）来呈现。下面是（macOS / Linux）`ls`命令的一个非常基本的克隆，用于用列来显示目录列表：

```python
import os

from rich import print
from rich.columns import Columns

directory = os.listdir(sys.argv[1])
print(Columns(directory))
```

以下屏幕截图是[列示例]（https://github.com/willmcgugan/rich/blob/master/examples/columns.py）的输出，该列显示了从API提取的数据：

！[列]（https://github.com/willmcgugan/rich/raw/master/imgs/columns.png）

## Markdown

Rich可以呈现[markdown]（https://rich.readthedocs.io/en/latest/markdown.html），并可相当不错的将其格式转移到终端。

为了渲染markdown，请导入`Markdown` 类，并使用包含markdown代码的字符串来构造它，然后将其打印到控制台。例子如下：

```python
from rich.console import Console
from rich.markdown import Markdown

console = Console()
with open("README.md") as readme:
    markdown = Markdown(readme.read())
console.print(markdown)
```

该例子的输出如下图：

！[markdown]（https://github.com/willmcgugan/rich/raw/master/imgs/markdown.png）

##语法突出显示

Rich使用[pygments]（https://pygments.org/）库来实现[语法高亮显示]（https://rich.readthedocs.io/en/latest/syntax.html）。用法类似于渲染markdown。构造一个`Syntax`对象并将其打印到控制台。下面是一个例子：

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

输出如下：

！[语法]（https://github.com/willmcgugan/rich/raw/master/imgs/syntax.png）

##回溯

Rich可以渲染漂亮的回溯，比标准Python回溯更容易阅读，并能显示更多代码。您可以将Rich设置为默认的回溯处理程序，这样所有难以捕获的异常都将由Rich为您呈现。

下面是在OSX（与Linux类似）上的外观：

！[回溯]（https://github.com/willmcgugan/rich/raw/master/imgs/traceback.png）

下面是Windows上的外观：

！[回溯_windows]（https://github.com/willmcgugan/rich/raw/master/imgs/traceback_windows.png）

有关详细信息，请参见[rich 回溯]（https://rich.readthedocs.io/en/latest/traceback.html）文档记述。
