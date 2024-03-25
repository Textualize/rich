[![Downloads](https://pepy.tech/badge/rich/month)](https://pepy.tech/project/rich)
[![PyPI version](https://badge.fury.io/py/rich.svg)](https://badge.fury.io/py/rich)
[![codecov](https://codecov.io/gh/Textualize/rich/branch/master/graph/badge.svg)](https://codecov.io/gh/Textualize/rich)
[![Rich blog](https://img.shields.io/badge/blog-rich%20news-yellowgreen)](https://www.willmcgugan.com/tag/rich/)
[![Twitter Follow](https://img.shields.io/twitter/follow/willmcgugan.svg?style=social)](https://twitter.com/willmcgugan)

![Logo](https://github.com/textualize/rich/raw/master/imgs/logo.svg)

[English readme](https://github.com/textualize/rich/blob/master/README.md)
 • [简体中文 readme](https://github.com/textualize/rich/blob/master/README.cn.md)
 • [正體中文 readme](https://github.com/textualize/rich/blob/master/README.zh-tw.md)
 • [Lengua española readme](https://github.com/textualize/rich/blob/master/README.es.md)
 • [Deutsche readme](https://github.com/textualize/rich/blob/master/README.de.md)
 • [Läs på svenska](https://github.com/textualize/rich/blob/master/README.sv.md)
 • [日本語 readme](https://github.com/textualize/rich/blob/master/README.ja.md)
 • [한국어 readme](https://github.com/textualize/rich/blob/master/README.kr.md)
 • [Français readme](https://github.com/textualize/rich/blob/master/README.fr.md)
 • [Schwizerdütsch readme](https://github.com/textualize/rich/blob/master/README.de-ch.md)
 • [हिन्दी readme](https://github.com/textualize/rich/blob/master/README.hi.md)
 • [Português brasileiro readme](https://github.com/textualize/rich/blob/master/README.pt-br.md)
 • [Italian readme](https://github.com/textualize/rich/blob/master/README.it.md)
 • [Русский readme](https://github.com/textualize/rich/blob/master/README.ru.md)
  • [فارسی readme](https://github.com/textualize/rich/blob/master/README.fa.md)
 • [Türkçe readme](https://github.com/textualize/rich/blob/master/README.tr.md)
 • [Polskie readme](https://github.com/textualize/rich/blob/master/README.pl.md)

Rich 是一款提供終端機介面中 _豐富的_ 文字效果及精美的格式設定的 Python 函式庫。

[Rich API](https://rich.readthedocs.io/en/latest/) 讓終端機介面加上色彩及樣式變得易如反掌。Rich 也可以繪製漂亮的表格、進度條、Markdown、語法醒目標示的程式碼、Traceback（追溯）……。

![Features](https://github.com/textualize/rich/raw/master/imgs/features.png)

關於 Rich 的介紹，請參見 [@fishnets88](https://twitter.com/fishnets88) 在 [calmcode.io](https://calmcode.io/rich/introduction.html) 錄製的影片。

[看看其他人對於 Rich 的討論](https://www.willmcgugan.com/blog/pages/post/rich-tweets/)。

## 相容性

Rich 可在 Linux、macOS、Windows 上運作。在新的 Windows Terminal 中可支援顯示全彩及 Emoji，但傳統的終端機中僅支援 16 色。Rich 最低需要的 Python 版本為 3.6.3。

Rich 可在 [Jupyter notebooks](https://jupyter.org/) 上使用，無須額外設定。

## 安裝

以 `pip` 或 PyPI 套件管理器安裝。

```sh
python -m pip install rich
```

以此命令測試 Rich 在終端機的輸出效果：

```sh
python -m rich
```

## Rich Print

匯入 [rich print](https://rich.readthedocs.io/en/latest/introduction.html#quick-start) 方法就可以輕鬆地讓程式進行 rich 輸出，rich print 與 Python 內建的函式用法相似。試試：

```python
from rich import print

print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())
```

![Hello World](https://github.com/textualize/rich/raw/master/imgs/print.png)

## Rich REPL

Rich 可以安裝在 Python REPL 中，如此一來就可以漂亮的輸出與突顯標示任何資料結構。

```python
>>> from rich import pretty
>>> pretty.install()
```

![REPL](https://github.com/textualize/rich/raw/master/imgs/repl.png)

## 使用 Console

匯入並建構 [Console](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console) 物件，以更全面地控制 rich 終端機內容。

```python
from rich.console import Console

console = Console()
```

Console 物件有個 `print` 方法，且刻意設計的與內建 `print` 函式相似。參考此範例：

```python
console.print("Hello", "World!")
```

如同預期的，這會將 `"Hello World!"` 印在終端機。須注意不同於內建的 `print` 函式，Rich 會自動將過長的文字換行，以符合終端機的寬度。

有幾種加上顏色及樣式的方式。您可以用 `style` 引數設定輸出內容的樣式，參考此範例：

```python
console.print("Hello", "World!", style="bold red")
```

輸出結果如下圖：

![Hello World](https://github.com/textualize/rich/raw/master/imgs/hello_world.png)

介紹完了如何對整行文字設定樣式，接著來看看更細部的使用。Rich 可以接受類似 [bbcode](https://en.wikipedia.org/wiki/BBCode) 的語法，對個別文字設定樣式。參考此範例：

```python
console.print("Where there is a [bold cyan]Will[/bold cyan] there [u]is[/u] a [i]way[/i].")
```

![Console Markup](https://github.com/textualize/rich/raw/master/imgs/where_there_is_a_will.png)

您可以用 Console 物件不費吹灰之力地達成細膩的輸出效果。參閱 [Console API](https://rich.readthedocs.io/en/latest/console.html) 說明文件以了解細節。

## Rich Inspect

Rich 提供了 [inspect](https://rich.readthedocs.io/en/latest/reference/init.html?highlight=inspect#rich.inspect) 函式，可以對任何 Python 物件，如 class、instance 或 builtin ，為其產生一份報告。

```python
>>> my_list = ["foo", "bar"]
>>> from rich import inspect
>>> inspect(my_list, methods=True)
```

![Log](https://github.com/textualize/rich/raw/master/imgs/inspect.png)

參閱 [inspect 說明文件](https://rich.readthedocs.io/en/latest/reference/init.html#rich.inspect) 以了解細節。

# Rich 函式庫

Rich 包含了一系列可繪製的物件，您可以使用它們來印出精美的畫面，或者協助偵錯程式碼。

按一下子標題以了解細節：

<details>
<summary>Log</summary>

Console 物件提供了 `log()` 方法，使用方式與 `print()` 類似，但還多了一欄來顯示目前時間、進行呼叫的檔案及行號。預設情況下 Rich 會語法醒目標示 Python 的結構及 repr 字串。若使用於字典或串列這類集合性物件，Rich 會將其漂亮地印出來，以符合可用空間。此範例示範了這些功能。

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

上面的程式碼會產生下圖結果：

![Log](https://github.com/textualize/rich/raw/master/imgs/log.png)

注意到 `log_locals` 引數，可用來輸出一張表格，用來顯示 log 方法被呼叫時，區域變數的內容。

log 方法可用於伺服器上長時間運作的程式，也很適合一般程式偵錯用途。

</details>
<details>
<summary>Logging Handler</summary>

您也可以使用內建的 [Handler 類別](https://rich.readthedocs.io/en/latest/logging.html) 來將 Python logging 模組的輸出內容格式化並賦予色彩：

![Logging](https://github.com/textualize/rich/raw/master/imgs/logging.png)

</details>

<details>
<summary>Emoji</summary>

以一對冒號包住表情符號的名稱，來透過 console 插入 Emoji。參考範例：

```python
>>> console.print(":smiley: :vampire: :pile_of_poo: :thumbs_up: :raccoon:")
😃 🧛 💩 👍 🦝
```

請謹慎使用此功能。

</details>

<details>
<summary>表格</summary>

Rich 可以用 unicode box 字元繪製彈性的 [表格](https://rich.readthedocs.io/en/latest/tables.html)。格式設定十分多元，包含框線、樣式、儲存格對齊……。

![table movie](https://github.com/textualize/rich/raw/master/imgs/table_movie.gif)

上圖的動畫效果是以 [table_movie.py](https://github.com/textualize/rich/blob/master/examples/table_movie.py) 產生的，該檔案位於 examples 資料夾。

參考這個簡單的表格範例：

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
    "Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$275,000,000", "$375,126,118"
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

執行結果如圖：

![table](https://github.com/textualize/rich/raw/master/imgs/table.png)

請留意，主控台標記的呈現方式與 `print()`、`log()` 相同。事實上，由 Rich 繪製的任何東西都可以被放在任何標題、列，甚至其他表格裡。

`Table` 類別很聰明，能夠自動調整欄寬來配合終端機的大小，也會在需要時自動將文字換行。此範例的程式碼與上一個相同，然而終端機變小了一點：

![table2](https://github.com/textualize/rich/raw/master/imgs/table2.png)

</details>

<details>
<summary>進度條</summary>

Rich 可繪製多個不閃爍的 [進度條](https://rich.readthedocs.io/en/latest/progress.html)，以追蹤需時較久的工作。

基本的使用方式，是將序列放在 `track` 函式中，再對其結果疊代。參考此範例：

```python
from rich.progress import track

for step in track(range(100)):
    do_step(step)
```

新增多個進度條也不是難事，來看看說明文件中的範例：

![progress](https://github.com/textualize/rich/raw/master/imgs/progress.gif)

您可以調整要顯示的狀態欄位。內建的欄位包含完成百分比、檔案大小、讀寫速度及剩餘時間。來看看另一個用來顯示下載進度的範例：

![progress](https://github.com/textualize/rich/raw/master/imgs/downloader.gif)

想嘗試看看嗎？您可以在 [examples/downloader.py](https://github.com/textualize/rich/blob/master/examples/downloader.py) 取得此範例程式。此程式可以在下載多個檔案時顯示各自的進度。

</details>

<details>
<summary>狀態</summary>

有些狀況下很難估計進度，就可以使用 [status](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console.status) 方法，此方法會顯示「spinner」動畫及訊息。該動畫播放時，仍可正常操作主控台。參考此範例：

```python
from time import sleep
from rich.console import Console

console = Console()
tasks = [f"task {n}" for n in range(1, 11)]

with console.status("[bold green]Working on tasks...") as status:
    while tasks:
        task = tasks.pop(0)
        sleep(1)
        console.log(f"{task} complete")
```

終端機的顯示效果如下：

![status](https://github.com/textualize/rich/raw/master/imgs/status.gif)

該 spinner 動畫乃借用自 [cli-spinners](https://www.npmjs.com/package/cli-spinners)。可以用 `spinner` 參數指定 spinner 樣式。執行此命令以顯示可用的值：

```
python -m rich.spinner
```

此命令在終端機的輸出結果如下圖：

![spinners](https://github.com/textualize/rich/raw/master/imgs/spinners.gif)

</details>

<details>
<summary>樹</summary>

Rich 可以用導引線繪製一棵 [樹](https://rich.readthedocs.io/en/latest/tree.html)。樹很適合用來顯示檔案結構，或其他繼承性的資料。

可以用文字或其他 Rich 能繪製的元素作為樹的標籤。執行下列程式碼來看看效果：

```
python -m rich.tree
```

這會產生下圖的結果：

![markdown](https://github.com/textualize/rich/raw/master/imgs/tree.png)

您可以參考 [tree.py](https://github.com/textualize/rich/blob/master/examples/tree.py) 範例程式，此程式可以樹狀圖展示目錄結構，如同 Linux 的 `tree` 命令。

</details>

<details>
<summary>資料欄</summary>

Rich 可以將內容呈現於整齊的 [資料欄](https://rich.readthedocs.io/en/latest/columns.html) 中，其欄寬可為等寬或最適寬度。此範例仿作了 macOS / Linux 系統中 `ls` 命令的基本功能，可以用資料欄列出目錄：

```python
import os
import sys

from rich import print
from rich.columns import Columns

directory = os.listdir(sys.argv[1])
print(Columns(directory))
```

此螢幕截圖為 [資料欄範例](https://github.com/textualize/rich/blob/master/examples/columns.py) 的輸出結果。此程式從某 API 取得資料，並以資料欄呈現：

![columns](https://github.com/textualize/rich/raw/master/imgs/columns.png)

</details>

<details>
<summary>Markdown</summary>

Rich 可以繪製 [Markdown](https://rich.readthedocs.io/en/latest/markdown.html) 並處理了將其轉換為終端機格式的大量工作。

先匯入 `Markdown` 類別，再以內容為 Markdown 語言的字串建構一個物件，接著將其印到 console。參考此範例：

```python
from rich.console import Console
from rich.markdown import Markdown

console = Console()
with open("README.md") as readme:
    markdown = Markdown(readme.read())
console.print(markdown)
```

執行結果如下圖：

![markdown](https://github.com/textualize/rich/raw/master/imgs/markdown.png)

</details>

<details>
<summary>語法醒目標示</summary>

Rich 使用了 [pygments](https://pygments.org/) 函式庫來實作 [語法醒目標示](https://rich.readthedocs.io/en/latest/syntax.html) 功能。使用方式與繪製 Markdown 相似，先建構 `Syntax` 物件並將其印到 console。參考此範例：

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

執行結果如下圖：

![syntax](https://github.com/textualize/rich/raw/master/imgs/syntax.png)

</details>

<details>
<summary>Tracebacks（追溯）</summary>

Rich 可以繪製 [漂亮的 tracebacks](https://rich.readthedocs.io/en/latest/traceback.html)，相較標準的 Python traceback 顯示了更多程式碼且更好懂。您可以將 Rich 設為預設的 traceback handler（處理常式），如此一來所有未接住的例外都由 Rich 呈現。

它在 macOS 上執行的效果如圖（Linux 上差異不大）：

![traceback](https://github.com/textualize/rich/raw/master/imgs/traceback.png)

</details>

所有可由 Rich 繪製的物件都用到了 [Console 協定](https://rich.readthedocs.io/en/latest/protocol.html)，您也可以依此實作自訂的 Rich 內容。

# Rich 企業版

可在 Tidelift 訂閱方案取得。

Rich 及其他數以千計的套件維護者正與 Tidelift 合作，以提供開放原始碼套件的商業性支援。此計畫能協助您節省時間、避開風險，同時也讓套件的維護者獲得報酬。[了解更多。](https://tidelift.com/subscription/pkg/pypi-rich?utm_source=pypi-rich&utm_medium=referral&utm_campaign=enterprise&utm_term=repo)

# 使用 Rich 的專案

以下列出幾個使用 Rich 的專案：

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
- [nf-core/tools](https://github.com/nf-core/tools)
  Python package with helper tools for the nf-core community.
- [cansarigol/pdbr](https://github.com/cansarigol/pdbr)
  pdb + Rich library for enhanced debugging
- [plant99/felicette](https://github.com/plant99/felicette)
  Satellite imagery for dummies.
- [seleniumbase/SeleniumBase](https://github.com/seleniumbase/SeleniumBase)
  Automate & test 10x faster with Selenium & pytest. Batteries included.
- [smacke/ffsubsync](https://github.com/smacke/ffsubsync)
  Automagically synchronize subtitles with video.
- [tryolabs/norfair](https://github.com/tryolabs/norfair)
  Lightweight Python library for adding real-time 2D object tracking to any detector.
- [ansible/ansible-lint](https://github.com/ansible/ansible-lint) Ansible-lint checks playbooks for practices and behaviour that could potentially be improved
- [ansible-community/molecule](https://github.com/ansible-community/molecule) Ansible Molecule testing framework
- +[Many more](https://github.com/textualize/rich/network/dependents)!

<!-- This is a test, no need to translate -->
