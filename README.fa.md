[![Supported Python Versions](https://img.shields.io/pypi/pyversions/rich/10.11.0)](https://pypi.org/project/rich/) [![PyPI version](https://badge.fury.io/py/rich.svg)](https://badge.fury.io/py/rich)

[![Downloads](https://pepy.tech/badge/rich/month)](https://pepy.tech/project/rich)
[![codecov](https://img.shields.io/codecov/c/github/Textualize/rich?label=codecov&logo=codecov)](https://codecov.io/gh/willmcgugan/rich)
[![Rich blog](https://img.shields.io/badge/blog-rich%20news-yellowgreen)](https://www.willmcgugan.com/tag/rich/)
[![Twitter Follow](https://img.shields.io/twitter/follow/willmcgugan.svg?style=social)](https://twitter.com/willmcgugan)

![Logo](https://github.com/willmcgugan/rich/raw/master/imgs/logo.svg)

[English readme](https://github.com/willmcgugan/rich/blob/master/README.md)
 • [简体中文 readme](https://github.com/willmcgugan/rich/blob/master/README.cn.md)
 • [正體中文 readme](https://github.com/willmcgugan/rich/blob/master/README.zh-tw.md)
 • [Lengua española readme](https://github.com/willmcgugan/rich/blob/master/README.es.md)
 • [Deutsche readme](https://github.com/willmcgugan/rich/blob/master/README.de.md)
 • [Läs på svenska](https://github.com/willmcgugan/rich/blob/master/README.sv.md)
 • [日本語 readme](https://github.com/willmcgugan/rich/blob/master/README.ja.md)
 • [한국어 readme](https://github.com/willmcgugan/rich/blob/master/README.kr.md)
 • [Français readme](https://github.com/willmcgugan/rich/blob/master/README.fr.md)
 • [Schwizerdütsch readme](https://github.com/willmcgugan/rich/blob/master/README.de-ch.md)
 • [हिन्दी readme](https://github.com/willmcgugan/rich/blob/master/README.hi.md)
 • [Português brasileiro readme](https://github.com/willmcgugan/rich/blob/master/README.pt-br.md)
 • [Italian readme](https://github.com/willmcgugan/rich/blob/master/README.it.md)
 • [Русский readme](https://github.com/willmcgugan/rich/blob/master/README.ru.md)
 • [فارسی readme](https://github.com/willmcgugan/rich/blob/master/README.fa.md)

ریچ یک کتاب خانه پایتون برای متن های _باشکوه_ و قالب بندی زیبا در ترمینال است.

[ریچ](https://rich.readthedocs.io/en/latest/) افزودن رنگ و سبک به خروجی ترمینال را آسان می‌کند.
ریچ همچنین می‌تواند جدول های زیبا، نوار های پیشرفت
(progress bars),
مارک داون
(MarkDown),
ترکیب سورس کد های برجسته شده,
ردیاب ها
(Tracebacks),
و غیره را به صورت خودکار در ترمینال نمایش دهد.


![قابلیت ها](https://github.com/willmcgugan/rich/raw/master/imgs/features.png)

برای معرفی ویدئویی ریچ این ویدئو را ببینید [calmcode.io](https://calmcode.io/rich/introduction.html) توسط [@fishnets88](https://twitter.com/fishnets88).

ببینید [مردم در مورد ریچ چه میگویند](https://www.willmcgugan.com/blog/pages/post/rich-tweets/).

## سازگاری

ریچ با لینوکس، مک او اس و ویندوز کار می کند.
رنگ واقعی / ایموجی با ترمینال جدید ویندوز کار می کند، ترمینال کلاسیک به 16 رنگ محدود شده است.
ریچ به پایتون
3.6.3
یا جدیدتر نیاز دارد.

ریچ با  [ژوپیتر نوت بوک (Jupyter notebooks)](https://jupyter.org/)
بدون نیازمندی اضافه ای کار می کند.

## نصب کردن

با `pip`
یا با مدیر بسته (package manager)
مورد علاقه خودتان نصب کنید.

```sh
python -m pip install rich
```

برای آزمایش ریچ در ترمینال خودتان، این را اجرا کنید:

```sh
python -m rich
```

## Rich Print

برای اضافه کردن راحت خروجی ریچ به برنامه خودتان، شما می توانید اضافه (Import)
کنید [rich print](https://rich.readthedocs.io/en/latest/introduction.html#quick-start)
را به پروژه خودتان.
که اثر یکسانی به عنوان تابع داخلی پایتون دارد.
این را امتحان کنید:

```python
from rich import print

print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())
```

![Hello World](https://github.com/willmcgugan/rich/raw/master/imgs/print.png)

## Rich REPL

ریچ می تواند در Python REPL,
نصب شود.
که هر نوعی از اطلاعات را به زیبایی چاپ می کند و به زیبایی برجسته می کند.

```python
>>> from rich import pretty
>>> pretty.install()
```

![REPL](https://github.com/willmcgugan/rich/raw/master/imgs/repl.png)

## استفاده از Console

برای پایش بیشتر از محتوای ترمینال ریچ،
[Console](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console)
را اضافه (Import)
کنید و یک شیء (Object) بسازید.

```python
from rich.console import Console

console = Console()
```

شی Console
یک تابع با نام `print`
دارد که مشابه تابع `print`
داخلی پایتون است.
این یک مثال از استفاده Console است:

```python
console.print("Hello", "World!")
```

همانطور که انتظار داشتید، این باید در ترمینال `"Hello World!"`
چاپ کند.
توجه کنید که این شبیه به تابع `print`
داخلی پایتون نیست.
ریچ متن شما را به صورت کلمه‌ای در عرض ترمینال قرار می دهد.
اما تابع `print`
داخلی پایتون به شکل کلمه‌ای نیست.

اینها تعدادی راه برای افزودن رنگ و سبک (Style)
به خروجی خودتان است.
شما می توانید برای ورودی های خود سبک قرار دهید با اضافه کردن کلمه کلیدی `style`.
اینجا یک مثال هست:

```python
console.print("Hello", "World!", style="bold red")
```

خروجی چیزی شبیه به این است:

![Hello World](https://github.com/willmcgugan/rich/raw/master/imgs/hello_world.png)

این برای سبک دادن به یک خط در زمان کمی خوب است.
برای سبکی با دانه بندی (Finely Grained Styling)،
ریچ یک نشانه گذاری خاص ارائه می دهند که چیزی شبیه به [bbcode](https://en.wikipedia.org/wiki/BBCode) است.
اینجا یک مثال هست:

```python
console.print("Where there is a [bold cyan]Will[/bold cyan] there [u]is[/u] a [i]way[/i].")
```

![Console Markup](https://github.com/willmcgugan/rich/raw/master/imgs/where_there_is_a_will.png)

You can use a Console object to generate sophisticated output with minimal effort. See the [Console API](https://rich.readthedocs.io/en/latest/console.html) docs for details.

شما می توانید از یک شیء Console
برای تولید خروجی استفاده کنید.
برای جزئیات بیشتر به [Console API](https://rich.readthedocs.io/en/latest/console.html) مراجعه کنید.

## Rich Inspect

ریچ دارای یک تابع `inspect`
است که می تواند یک گزارش از هر شیء از پایتون ، مثل کلاس (Class)،
نمونه (Instance)
یا تابع (Builtin)
را تولید کند.

```python
>>> my_list = ["foo", "bar"]
>>> from rich import inspect
>>> inspect(my_list, methods=True)
```

![Log](https://github.com/willmcgugan/rich/raw/master/imgs/inspect.png)

برای جزئیات بیشتر به [inspect docs](https://rich.readthedocs.io/en/latest/reference/init.html#rich.inspect) مراجعه کنید.

# Rich Library

ریچ شامل تعدادی از 
_رندر پزیر_
داخلی است که شما می توانید برای ایجاد خروجی ظریف در CLI
خودتان استفاده کنید.
و به شما برای تصحیح
(Debug)
کد خودتان کمک می کند.

برای جزییات بیشتز کلیک کنید:

<details>
<summary>Log</summary>

شیء Console دارای یک تابع `log()`
است که به شکلی از `print()` است،
اما همچنان یک ستون برای الان رندر می کند و فایل و خط که کد را تولید کرده است.
به صورت عادی ریچ  برجسته می کند علامت ها را برای ساختار های پایتون و برای رشته
(String)
های
repr.
اگر شما یک مجموعه
(دیکشنری یا لیست)
را چاپ کنید، ریچ به زیبایی آن را در فضای موجود چاپ می کند.
این یک مثال از برخی ویژگی های آن است:


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

در بالا خروجی زیر را دریافت می کنید:

![Log](https://github.com/willmcgugan/rich/raw/master/imgs/log.png)

به
`log_locals`
ها توجه کنید،
که یک جدول که شامل متغیر های محلی است خروجی می دهد.
جایی که تابع log
صدا زده می شود.

تابع log
باید استفاده شود برای گزارش در ترمینال برای برنامه های بلند مدت مانند سرور،
اما یک کمک برای تصحیح برخی از خطاهای برنامه است.

</details>
<details>
<summary>Logging Handler</summary>

شما می توانید از
[Handler class](https://rich.readthedocs.io/en/latest/logging.html)
های داخلی برای اصلاح و رنگی کردن خروجی از ماژول گزارش پایتون
(Python's logging module) استفاده کنید.
این یک مثال از خروجی را نشان می دهد:

![Logging](https://github.com/willmcgugan/rich/raw/master/imgs/logging.png)

</details>

<details>
<summary>Emoji</summary>

برای افزودن یک ایموجی به خروجی ترمینال، اسم را بین دو نقطه
(colon)
قرار دهید.
این یک مثال است:

```python
>>> console.print(":smiley: :vampire: :pile_of_poo: :thumbs_up: :raccoon:")
😃 🧛 💩 👍 🦝
```

Please use this feature wisely.

</details>

<details>
<summary>Tables</summary>

ریچمی تواند 
[جدول های انعطاف پذیر](https://rich.readthedocs.io/en/latest/tables.html)
با کارکتر های یونیکد بسازد.

![table movie](https://github.com/willmcgugan/rich/raw/master/imgs/table_movie.gif)

انیمشن بالا با استفاده از
[table_movie.py](https://github.com/willmcgugan/rich/blob/master/examples/table_movie.py)
در دایرکتوری تست ساخته شده است.

این یک مثال ساده از جدول است:

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

این کد خروجی زیر را تولید می کند:

![table](https://github.com/willmcgugan/rich/raw/master/imgs/table.png)

توجه داشته باشید که نشانه گذاری کنسول به همان روش 
`print()` و `log()`
ارائه می شود.
در واقع، هر چیزی که توسط
Rich
قابل رندر است در هدرها / ردیف ها (حتی جداول دیگر) ممکن است گنجانده شود.

کلاس
`Table`
به اندازه کافی هوشمند است که اندازه ستون ها را متناسب با عرض موجود ترمینال تغییر دهد و متن را در صورت لزوم بسته بندی کند.
این همان مثال با ترمینال کوچکتر است:

![table2](https://github.com/willmcgugan/rich/raw/master/imgs/table2.png)

</details>

<details>
<summary>Progress Bars</summary>

ریچ
می تواند چندین نوار پیشرفت بدون نا هماهنگی برای پیگیری وظایف طولانی مدت ارائه دهد.


For basic usage, wrap any sequence in the `track` function and iterate over the result. Here's an example:

برای استفاده اولیه، هر دنباله ای را در تابع
`track`
روی نتیجه تکرار کنید. در اینجا یک مثال است:

```python
from rich.progress import track

for step in track(range(100)):
    do_step(step)
```

اضافه کردن چندین نوار پیشرفت خیلی سخت نیست. در اینجا یک مثال آورده شده است:



![progress](https://github.com/willmcgugan/rich/raw/master/imgs/progress.gif)

ستون ها ممکن است به گونه ای پیکربندی شوند که جزئیاتی را که می خواهید نشان دهند. ستون های داخلی شامل درصد کامل، اندازه فایل، سرعت فایل و زمان باقی مانده است. در اینجا مثال دیگری وجود دارد که دانلود در حال انجام را نشان می دهد:

![progress](https://github.com/willmcgugan/rich/raw/master/imgs/downloader.gif)

برای اینکه خودتان این را امتحان کنید،
[examples/downloader.py](https://github.com/willmcgugan/rich/blob/master/examples/downloader.py)
را ببینید که می‌تواند چندین
URL
را به طور همزمان بارگیری کند و پیشرفت را نشان دهد.

</details>

<details>
<summary>Status</summary>

برای موقعیت هایی که محاسبه پیشرفت دشوار است، می توانید از روش [status](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console.status)
استفاده کنید که یک انیمیشن و پیام چرخنده
(spinner)
را نمایش می‌دهد. این انیمیشن شما را از استفاده عادی از کنسول باز نمی دارد. در اینجا یک مثال است:

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

این کد خروجی زیر را در ترمینال ایجاد می کند.

![status](https://github.com/willmcgugan/rich/raw/master/imgs/status.gif)

در انیمیشن های چرخنده از
[cli-spinners](https://www.npmjs.com/package/cli-spinners)
استفاده شده است.
می توانید با تعیین پارامتر
`spinner`
یک چرخنده را انتخاب کنید. برای مشاهده دستور زیر را اجرا کنید:

```
python -m rich.spinner
```

دستور بالا خروجی زیر را در ترمینال ایجاد می کند:

![spinners](https://github.com/willmcgugan/rich/raw/master/imgs/spinners.gif)

</details>

<details>
<summary>Tree</summary>

ریچ می تواند یک
[tree](https://rich.readthedocs.io/en/latest/tree.html)
را با خطوط راهنما نمایش دهد. درخت
`tree`
برای نمایش ساختار فایل یا هر داده سلسله مراتبی دیگر خوب است.

برچسب های
`labels`
درخت می توانند متن ساده یا هر چیز دیگری که ریچ می تواند نمایش دهد باشد. برای نمایش موارد دستور زیر را اجرا کنید:

```
python -m rich.tree
```

این کد خروجی زیر را ایجاد می کند:

![markdown](https://github.com/willmcgugan/rich/raw/master/imgs/tree.png)

See the [tree.py](https://github.com/willmcgugan/rich/blob/master/examples/tree.py) example for a script that displays a tree view of any directory, similar to the linux `tree` command.

مثال
[این]
را برای اسکریپتی ببینید که نمایش درختی از هر دایرکتوری را نمایش می دهد، شبیه به فرمان 
`tree`
در لینوکس است.

</details>

<details>
<summary>Columns</summary>

ریچ می تواند محتوا را به صورت 
[منظم](https://rich.readthedocs.io/en/latest/columns.html)
با عرض مساوی یا بهینه ارائه دهد.
در اینجا یک کلون بسیار ابتدایی از دستور
ls
در
(مک او اس / لینوکس)
وجود دارد که فهرست دایرکتوری را در ستون ها نمایش می دهد:

```python
import os
import sys

from rich import print
from rich.columns import Columns

directory = os.listdir(sys.argv[1])
print(Columns(directory))
```

تصویر زیر خروجی از
[columns example](https://github.com/willmcgugan/rich/blob/master/examples/columns.py)
است که داده های استخراج شده از یک
API
را در ستون ها نمایش می دهد:

![columns](https://github.com/willmcgugan/rich/raw/master/imgs/columns.png)

</details>

<details>
<summary>Markdown</summary>

ریچ می تواند
[markdown](https://rich.readthedocs.io/en/latest/markdown.html)
را رندر کند و کار خوبی برای ترجمه آن در ترمینال انجام دهد.

برای رندر کردن مارک دون، کلاس
`Markdown`
را وارد کنید و آن را با رشته ای
`Str`
حاوی کد مارک دون است بسازید.
سپس آن را در کنسول چاپ کنید.
در اینجا یک مثال است:

```python
from rich.console import Console
from rich.markdown import Markdown

console = Console()
with open("README.md") as readme:
    markdown = Markdown(readme.read())
console.print(markdown)
```

خروجی اند کد چیزی شبیه به این را تولید می کند:

![markdown](https://github.com/willmcgugan/rich/raw/master/imgs/markdown.png)

</details>

<details>
<summary>Syntax Highlighting</summary>

ریچ از کتابخانه
[pygments](https://pygments.org/)
برای پیاده سازی
[syntax](https://rich.readthedocs.io/en/latest/syntax.html)
استفاده می کند.
استفاده
`syntax`
مشابه استفاده مارک دون است.
یک شی
`Syntax`
بسازید و آن را در کنسول چاپ کنید.
در اینجا یک مثال است:

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

این کد خروجی زیر را ایجاد می کند:

![syntax](https://github.com/willmcgugan/rich/raw/master/imgs/syntax.png)

</details>

<details>
<summary>Tracebacks</summary>

ریچ می تواند
[tracebacks](https://rich.readthedocs.io/en/latest/traceback.html)
های زیبا را نمایش دهد که خواندن آن آسان تر است و کد بیشتری را نسبت به 
`traceback`
های استاندارد پایتون نشان می دهد.
می توانید ریچ را به عنوان کنترل کننده اصلی 
`tracebacks`
تنظیم کنید تا همه استثناهای کشف نشده توسط ریچ ارائه شوند.

در اینجا این را در مک او اس نمایش می دهد (در لینوکس مشابه این است):

![traceback](https://github.com/willmcgugan/rich/raw/master/imgs/traceback.png)

</details>

All Rich renderables make use of the [Console Protocol](https://rich.readthedocs.io/en/latest/protocol.html), which you can also use to implement your own Rich content.

همه ریچ های قابل نمایش از
[Console Protocol](https://rich.readthedocs.io/en/latest/protocol.html)
استفاده می کنند،
که شما می توانید برای پیاده سازی محتوای ریچ خود نیز از آن استفاده کنید.