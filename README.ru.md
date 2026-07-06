[![Supported Python Versions](https://img.shields.io/pypi/pyversions/rich)](https://pypi.org/project/rich/) [![PyPI version](https://badge.fury.io/py/rich.svg)](https://badge.fury.io/py/rich)

[![Downloads](https://pepy.tech/badge/rich/month)](https://pepy.tech/project/rich)
[![codecov](https://img.shields.io/codecov/c/github/Textualize/rich?label=codecov&logo=codecov)](https://codecov.io/gh/Textualize/rich)
[![Rich blog](https://img.shields.io/badge/blog-rich%20news-yellowgreen)](https://www.willmcgugan.com/tag/rich/)
[![Twitter Follow](https://img.shields.io/twitter/follow/willmcgugan.svg?style=social)](https://twitter.com/willmcgugan)

![Logo](https://github.com/textualize/rich/raw/main/imgs/logo.svg)

[English readme](https://github.com/textualize/rich/blob/main/README.md)
 • [简体中文 readme](https://github.com/textualize/rich/blob/main/README.cn.md)
 • [正體中文 readme](https://github.com/textualize/rich/blob/main/README.zh-tw.md)
 • [Lengua española readme](https://github.com/textualize/rich/blob/main/README.es.md)
 • [Deutsche readme](https://github.com/textualize/rich/blob/main/README.de.md)
 • [Läs på svenska](https://github.com/textualize/rich/blob/main/README.sv.md)
 • [日本語 readme](https://github.com/textualize/rich/blob/main/README.ja.md)
 • [한국어 readme](https://github.com/textualize/rich/blob/main/README.kr.md)
 • [Français readme](https://github.com/textualize/rich/blob/main/README.fr.md)
 • [Schwizerdütsch readme](https://github.com/textualize/rich/blob/main/README.de-ch.md)
 • [हिन्दी readme](https://github.com/textualize/rich/blob/main/README.hi.md)
 • [Português brasileiro readme](https://github.com/textualize/rich/blob/main/README.pt-br.md)
 • [Italian readme](https://github.com/textualize/rich/blob/main/README.it.md)
 • [Русский readme](https://github.com/textualize/rich/blob/main/README.ru.md)
  • [فارسی readme](https://github.com/textualize/rich/blob/main/README.fa.md)
 • [Türkçe readme](https://github.com/textualize/rich/blob/main/README.tr.md)
 • [Polskie readme](https://github.com/textualize/rich/blob/main/README.pl.md)

Rich это Python библиотека, позволяющая отображать _красивый_ текст и форматировать терминал.

[Rich API](https://rich.readthedocs.io/en/latest/) упрощает добавление цветов и стилей к выводу терминала. Rich также позволяет отображать красивые таблицы, прогресс бары, markdown, код с подсветкой синтаксиса, ошибки, и т.д. — прямо после установки.

![Features](https://github.com/textualize/rich/raw/main/imgs/features.png)

Смотрите видеоинструкцию  [calmcode.io](https://calmcode.io/rich/introduction.html) от [@fishnets88](https://twitter.com/fishnets88).

Посмотрите [что люди думают о Rich](https://www.willmcgugan.com/blog/pages/post/rich-tweets/).

## Cовместимость

Rich работает с Linux, OSX и Windows. True color / эмоджи работают с новым терминалом Windows, классический терминал лимитирован 16 цветами. Rich требует Python 3.6.3 или более новый.

Rich работает с [Jupyter notebooks](https://jupyter.org/) без дополнительной конфигурации.

## Установка

Установите с помощью `pip` или вашего любимого PyPI менеджера пакетов.

```sh
python -m pip install rich
```

Запустите следующую команду, чтобы проверить Rich вывод в вашем терминале:

```sh
python -m rich
```

## Rich Print

Простейший способ получить красивый вывод это импортировать метод [rich print](https://rich.readthedocs.io/en/latest/introduction.html#quick-start), он принимает такие же аргументы что и стандартный метод `print`. Попробуйте:

```python
from rich import print

print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())
```

![Hello World](https://github.com/textualize/rich/raw/main/imgs/print.png)

## Rich REPL

Rich может быть установлен в Python REPL, так, все данные будут выведены через Rich.

```python
>>> from rich import pretty
>>> pretty.install()
```

![REPL](https://github.com/textualize/rich/raw/main/imgs/repl.png)

## Использование класса Console

Для большего контроля над терминалом Rich, импортируйте и инициализируйте класс [Console](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console).

```python
from rich.console import Console

console = Console()
```

У класса Сonsole есть метод `print` который имеет идентичный встроенной функции функционал `print`. Вот пример использования:

```python
console.print("Hello", "World!")
```

Как вы могли догадаться, это выведет `Hello World!` в терминал. Запомните что, в отличии от встроенной функции `print`, Rich настроит переносы слов так, чтобы ваш текст соответствовал ширине терминала.

Есть несколько способов добавить цвет и стиль к вашему выводу. Вы можете выбрать стиль для всего вывода добавив аргумент `style`. Вот пример:

```python
console.print("Hello", "World!", style="bold red")
```

Вывод будет выглядеть примерно так:

![Hello World](https://github.com/textualize/rich/raw/main/imgs/hello_world.png)

Этого достаточно чтобы стилизовать 1 строку. Для более детальной стилизации, Rich использует специальную разметку похожую по синтаксису на [bbcode](https://en.wikipedia.org/wiki/BBCode). Вот пример:

```python
console.print("Where there is a [bold cyan]Will[/bold cyan] there [u]is[/u] a [i]way[/i].")
```

![Console Markup](https://github.com/textualize/rich/raw/main/imgs/where_there_is_a_will.png)

Вы можете использовать класс Console чтобы генерировать красивый вывод с минимальными усилиями. Для получения детальной информации смотрите [документацию Console API](https://rich.readthedocs.io/en/latest/console.html).

## Rich Inspect

В Rich имеется функция [inspect](https://rich.readthedocs.io/en/latest/reference/init.html?highlight=inspect#rich.inspect) которая может украсить любой Python объект, например класс, переменную, или функцию.

```python
>>> my_list = ["foo", "bar"]
>>> from rich import inspect
>>> inspect(my_list, methods=True)
```

![Log](https://github.com/textualize/rich/raw/main/imgs/inspect.png)

Для получения детальной информации смотрите [документацию inspect](https://rich.readthedocs.io/en/latest/reference/init.html#rich.inspect).

# Библиотека Rich

Rich содержит несколько встроенных _визуализаций_ которые вы можете использовать чтобы сделать красивый вывод в вашем CLI, а также они помогают в отладке кода.

Вот несколько вещей которые может делать Rich (нажмите чтобы узнать больше):

<details>
<summary>Лог</summary>

В классе Сonsole есть метод `log()` который имеет интерфейс, аналогичный `print()`, но также отображает колонку текущим временем, именем файла и номером строки кода в которой был вызван метод. По умолчанию Rich будет подсвечивать синтаксис для структур Python и для строк repr. Если вы передадите в метод коллекцию (т.е. dict или list) Rich выведет её так, чтобы она разместилась в доступном пространстве. Вот пример использования этого метода.

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

Приведенный выше код выведет это:

![Log](https://github.com/textualize/rich/raw/main/imgs/log.png)


Обратите внимание на аргумент `log_locals`, который выводит таблицу, содержащую локальные переменные функции, в которой был вызван метод log.

Метод может быть использован для вывода данных в терминал в длительно работающих программ, таких как сервера, но он также может помочь в отладке.

</details>
<details>
<summary>Обработчик Логов</summary>

Вы также можете использовать встроенный [класс Handler](https://rich.readthedocs.io/en/latest/logging.html) чтобы форматировать и раскрашивать вывод из встроенной библиотеки logging. Вот пример вывода:

![Logging](https://github.com/textualize/rich/raw/main/imgs/logging.png)

</details>

<details>
<summary>Эмоджи</summary>

Чтобы вставить эмоджи в вывод консоли, поместите его название между двумя двоеточиями. Вот пример:

```python
>>> console.print(":smiley: :vampire: :pile_of_poo: :thumbs_up: :raccoon:")
😃 🧛 💩 👍 🦝
```

Пожалуйста, используйте эту функцию с умом.

</details>

<details>
<summary>Таблицы</summary>

Rich может отображать гибкие настраиваемые [таблицы](https://rich.readthedocs.io/en/latest/tables.html) с помощью символов unicode. Есть большое количество вариантов границ, стилей, выравниваний ячеек и т.п.

![table movie](https://github.com/textualize/rich/raw/main/imgs/table_movie.gif)

Эта анимация была сгенерирована с помощью [table_movie.py](https://github.com/textualize/rich/blob/main/examples/table_movie.py) в папке примеров.

Вот пример более простой таблицы:

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

Этот пример выводит:

![table](https://github.com/textualize/rich/raw/main/imgs/table.png)

Обратите внимание, что разметка осуществляется таким же способом, что и `print()` и `log()`. На самом деле, все, что может быть отображено Rich, может быть включено в заголовки / строки (даже в другие таблицы).

Класс `Table` достаточно умный чтобы менять размер столбцов, так, чтобы они заполняли доступную ширину терминала, обёртывая текст как нужно. Вот тот же самый пример с терминалом меньше таблицы:

![table2](https://github.com/textualize/rich/raw/main/imgs/table2.png)

</details>

<details>
<summary>Прогресс Бары</summary>

Rich может отображать несколько плавных [прогресс](https://rich.readthedocs.io/en/latest/progress.html) баров чтобы отслеживать долго-идущие задания.

Для базового использования, оберните любую последовательность в функцию `track` и выполните итерации по результату. Вот пример:

```python
from rich.progress import track

for step in track(range(100)):
    do_step(step)
```

Добавить несколько индикаторов выполнения не намного сложнее. Вот пример взятый из документации:

![progress](https://github.com/textualize/rich/raw/main/imgs/progress.gif)

Столбцы могут быть сконфигурированы таким образом, чтобы отображать любые сведения, которые вы хотите. Стандартные столбцы содержат проценты выполнения, размер файлы, скорость файла и оставшееся время. Вот ещё пример показывающий прогресс загрузки:

![progress](https://github.com/textualize/rich/raw/main/imgs/downloader.gif)

Чтобы попробовать самому, скачайте [examples/downloader.py](https://github.com/textualize/rich/blob/main/examples/downloader.py), который может загружать несколько URL-адресов одновременно, отображая прогресс.

</details>

<details>
<summary>Статус</summary>

Для ситуаций где сложно вычислить прогресс, вы можете использовать метод [статус](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console.status) который будет отображать крутящуюся анимацию и сообщение. Анимация не помешает вам использовать консоль в обычном режиме. Вот пример:

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

Это сгенерирует вот такой вывод в консоль.

![status](https://github.com/textualize/rich/raw/main/imgs/status.gif)

Крутящиеся анимации были взяты из [cli-spinners](https://www.npmjs.com/package/cli-spinners). Вы можете выбрать одну из них указав параметр `spinner`. Введите следующую команду чтобы посмотреть доступные анимации:

```
python -m rich.spinner
```

Приведенная выше команда сгенерирует следующий вывод в терминале:

![spinners](https://github.com/textualize/rich/raw/main/imgs/spinners.gif)

</details>

<details>
<summary>Дерево</summary>

Rich может отобразить [дерево](https://rich.readthedocs.io/en/latest/tree.html) с направляющими уровнями. Дерево идеально подходит для отображения структуры файлов или любых других иерархических данных.

Метки дерева могут быть содержать простой текст или чем-либо еще, что может отобразить Rich. Запустите следующую команду для демонстрации:

```
python -m rich.tree
```

Это генерирует следующий вывод:

![markdown](https://github.com/textualize/rich/raw/main/imgs/tree.png)

Смотрите пример [tree.py](https://github.com/textualize/rich/blob/main/examples/tree.py) скрипта,который отображает древовидное представление любого каталога, аналогично команде linux `tree`.

</details>

<details>
<summary>Колонки</summary>

Rich может отображать контент в аккуратных [колонках](https://rich.readthedocs.io/en/latest/columns.html) с равной или оптимальной шириной. Вот очень простой пример клона команды `ls` (MacOS / Linux) который отображает список файлов из папки в виде колонок:

```python
import os
import sys

from rich import print
from rich.columns import Columns

directory = os.listdir(sys.argv[1])
print(Columns(directory))
```

Следующий снимок экрана является [примером колонок](https://github.com/textualize/rich/blob/main/examples/columns.py) который изображает данные взятые из API в столбцах:

![columns](https://github.com/textualize/rich/raw/main/imgs/columns.png)

</details>

<details>
<summary>Markdown</summary>

Rich может отображать [markdown](https://rich.readthedocs.io/en/latest/markdown.html), проделывая неплохую работу в форматировании под терминал.

Чтобы отобразить markdown импортируйте класс `Markdown` и инициализируйте его с помощью строки содержащей код markdown. Затем распечатайте его в консоли. Вот пример:

```python
from rich.console import Console
from rich.markdown import Markdown

console = Console()
with open("README.md") as readme:
    markdown = Markdown(readme.read())
console.print(markdown)
```

Это выведет что-то похожее на это:

![markdown](https://github.com/textualize/rich/raw/main/imgs/markdown.png)

</details>

<details>
<summary>Подсветка синтаксиса</summary>

Rich использует библиотеку [pygments](https://pygments.org/) чтобы выполнить [подсветку синтаксиса](https://rich.readthedocs.io/en/latest/syntax.html). Использование аналогично рендерингу markdown; создайте объект `Syntax` и выведите его на консоль. Вот пример:

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

Это выведет что-то похожее на это:

![syntax](https://github.com/textualize/rich/raw/main/imgs/syntax.png)

</details>

<details>
<summary>Ошибки</summary>

Rich может отображать [красивый стек ошибок](https://rich.readthedocs.io/en/latest/traceback.html), который проще читать, и показывает больше информации чем стандартные стек ошибок Python. Вы можете установить Rich как стандартный обработчик ошибок чтобы все не перехваченные исключения отображались Rich.

Вот как это выглядит на OSX (похоже на Linux):

![traceback](https://github.com/textualize/rich/raw/main/imgs/traceback.png)

</details>

Все визуализации Rich используют [протокол Console](https://rich.readthedocs.io/en/latest/protocol.html), который позволяет вам добавлять свой собственный Rich контент.

# Rich CLI

Смотрите также [Rich CLI](https://github.com/textualize/rich-cli) для получения информации о приложении командной строки, работающего на базе Rich. Подсветка синтаксиса кода, рендеринг markdown, отображение CSV-файлов в таблицах и многое другое доступно непосредственно из командной строки.


![Rich CLI](https://raw.githubusercontent.com/Textualize/rich-cli/main/imgs/rich-cli-splash.jpg)

# Textual

Смотрите также дочерний проект Rich, [Textual](https://github.com/Textualize/textual), который вы можете использовать для создания сложных пользовательских интерфейсов в терминале.

# Rich для предприятий

Rich доступен как часть подписки Tidelift.

Ментейнеры проекта Rich, как и тысячи других разработчиков работают с подпиской Tidelift чтобы предоставить коммерческую поддержку и поддержку для проектов с открытым кодом, которые вы используете для создания своих приложений. Экономьте время, устраняйте риски и улучшайте состояние вашего кода, одновременно платя спонсорам проектов, которые вы используете. [Узнайте больше.](https://tidelift.com/subscription/pkg/pypi-rich?utm_source=pypi-rich&utm_medium=referral&utm_campaign=enterprise&utm_term=repo)

# Проекты использующие Rich

Вот несколько проектов использующих Rich:

- [BrancoLab/BrainRender](https://github.com/BrancoLab/BrainRender)
  библиотека Python для визуализации нейроанатомических данных в 3 измерениях
- [Ciphey/Ciphey](https://github.com/Ciphey/Ciphey)
  автоматизированная утилита для расшифровки
- [emeryberger/scalene](https://github.com/emeryberger/scalene)
  Высокая производительность, высокая точность CPU и профилировщик памяти для Python
- [hedythedev/StarCli](https://github.com/hedythedev/starcli)
  Просматривайте трендовые проекты GitHub прямо из вашего терминала
- [intel/cve-bin-tool](https://github.com/intel/cve-bin-tool)
  Эта утилита сканирует известные уязвимости (openssl, libpng, libxml2, expat and a few others) чтобы уведомить вас, если ваша система использует библиотеки с известными уязвимостями.
- [nf-core/tools](https://github.com/nf-core/tools)
  Библиотека Python с полезными инструментами для сообщества nf-core.
- [cansarigol/pdbr](https://github.com/cansarigol/pdbr)
  pdb + Rich библиотека для улучшенного дебаггинга
- [plant99/felicette](https://github.com/plant99/felicette)
  Изображения со спутников для чайников.
- [seleniumbase/SeleniumBase](https://github.com/seleniumbase/SeleniumBase)
  Автоматизируйте и тестируйте в 10 раз быстрее с Selenium и pytest. Батарейки включены.
- [smacke/ffsubsync](https://github.com/smacke/ffsubsync)
  Автоматически синхронизируйте субтитры с видео.
- [tryolabs/norfair](https://github.com/tryolabs/norfair)
  Простая библиотека Python для добавления 2D отслеживания к любому детектеру в реальном времени.
- [ansible/ansible-lint](https://github.com/ansible/ansible-lint) Ansible-lint проверяет пьесы для практик и поведений которые могут быть исправлены
- [ansible-community/molecule](https://github.com/ansible-community/molecule) Ansible Molecule тестинг фреймворк
- +[Ещё больше](https://github.com/textualize/rich/network/dependents)!

<!-- This is a test, no need to translate -->
