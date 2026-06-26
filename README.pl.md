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
 • [Indonesian readme](https://github.com/textualize/rich/blob/main/README.id.md)
 • [فارسی readme](https://github.com/textualize/rich/blob/main/README.fa.md)
 • [Türkçe readme](https://github.com/textualize/rich/blob/main/README.tr.md)
 • [Polskie readme](https://github.com/textualize/rich/blob/main/README.pl.md)


Rich to bilbioteka Pythona dla tekstów _rich_ i pięknego formatowania w terminalu.

[Rich API](https://rich.readthedocs.io/en/latest/) sprawia, że dodanie kolorów i stylów do wyjścia terminala jest proste. Rich może również wyświetlać ładne tabele, paski postępu, markdown, podświetlenie składni kodu źródłowego, ślady wsteczne (tracebacki), i jeszcze więcej - od ręki.

![Features](https://github.com/textualize/rich/raw/main/imgs/features.png)

Wprowadzenie wideo do Richa na [calmcode.io](https://calmcode.io/rich/introduction.html) stworzonym przez [@fishnets88](https://twitter.com/fishnets88).

Zobacz co [inni mówią o Richu](https://www.willmcgugan.com/blog/pages/post/rich-tweets/).

## Kompatybilność

Rich działa na systemach operacyjnych Linux, OSX i Windows. True color / emoji współgra z nowym Terminalem Windows, klasyczny terminal jest ograniczony do 16 kolorów. Rich wymaga Pythona 3.7 lub nowszego.

Rich działa z [notatnikami Jupyter](https://jupyter.org) bez potrzeby dodatkowej konfiguracji.

## Instalacja

Zainstaluj z użyciem `pip` lub twojego ulubionego menedżera pakietów PyPI.

```sh
python -m pip install rich
```

Uruchom komendę poniżej aby przetestować wyjście Rich na twoim terminalu:

```sh
python -m rich
```

## Rich Print

By bezproblemowo dodać wyjście rich do twojej aplikacji, możesz zaimportować metodę [rich print](https://rich.readthedocs.io/en/latest/introduction.html#quick-start), która ma tą samą sygnaturę jak wbudowana funkcja Pythona. Wypróbuj:

```python
from rich import print

print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())
```

![Hello World](https://github.com/textualize/rich/raw/main/imgs/print.png)

## Rich REPL

Rich może zostać zainstalowany w REPL, żeby wszystkie struktury danych były ładnie wypisane i podświetlone.

```python
>>> from rich import pretty
>>> pretty.install()
```

![REPL](https://github.com/textualize/rich/raw/main/imgs/repl.png)

## Używanie konsoli

Dla większej kontroli nad bogatą zawartością terminala, zaimportuj i skonstruuj obiekt [Console](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console).

```python
from rich.console import Console

console = Console()
```

Obiekt Console ma metodę `print`, mającą celowo podobny interfejs do wbudowanej funkcji `print`. Tu jest przykład użycia:

```python
console.print("Hello", "World!")
```

Jak można się spodziewać wyświetli to `"Hello World!"` do terminala. Warto zauważyć, że Rich automatycznie zawija tekst, aby mieścił się on w szerokości terminala.

Jest kilka możliwości dodania koloru i stylu do wyjścia terminala. Możesz ustawić styl dla całego wyjścia, dodając argument `style`. Na przykład:

```python
console.print("Hello", "World!", style="bold red")
```

Wyjście będzie wyglądało tak:

![Hello World](https://github.com/textualize/rich/raw/main/imgs/hello_world.png)

Jest to w porządku dla stylizacji jednej linijki tekstu. Dla dokładniejszej stylizacj, Rich wyświetla specjalny format markup podobny w składni do [bbcode](https://en.wikipedia.org/wiki/BBCode). Przykład poniżej:

```python
console.print("Where there is a [bold cyan]Will[/bold cyan] there [u]is[/u] a [i]way[/i].")
```

![Console Markup](https://github.com/textualize/rich/raw/main/imgs/where_there_is_a_will.png)

Możesz użyć obiektu Console, aby wygenerować skomplikowane wyjście bez problemu. Więcej informacji odnośnie Console API w [dokumentacji](https://rich.readthedocs.io/en/latest/console.html).

## Rich Inspect

Rich ma funkcję [inspect](https://rich.readthedocs.io/en/latest/reference/init.html?highlight=inspect#rich.inspect), która może produkować raporty na jakimkolwiek obiekcie Python, jak np. klasa, instancja, lub wbudowana funkcja.

```python
>>> my_list = ["foo", "bar"]
>>> from rich import inspect
>>> inspect(my_list, methods=True)
```

![Log](https://github.com/textualize/rich/raw/main/imgs/inspect.png)

Więcej informacji na temat funkcji inspect w [dokumentacji](https://rich.readthedocs.io/en/latest/reference/init.html#rich.inspect).

## Biblioteka Rich

Rich zawiera wiele wbudowanych _renderables_, które możesz użyć do stworzenia eleganckiego wyjścia w twoim CLI i pomóc ci w debugowaniu twojego kodu.

Kliknij poniższe nagłówki, żeby poznać detale:

<details>
<summary>Log</summary>

Obiekt Console ma metodę `log()`, mającą podobny interfejs do `print()`, ale wyświetla również kolumnę zawierającą aktualny czas oraz plik i linijkę, która wywołała powyższą metodę. Domyślnie Rich podświetla składnię dla struktur Pythona i ciągów repr. Jeśli zlogujesz kolekcję (czyli listę `list` lub słownik `dict`), Rich ją ładnie wypisze tak, żeby zmieściła się w dostępnym miejscu. Poniżej znajduje się przykład tych funkcji.

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

Powyższy kod wyświetla poniższy tekst:

![Log](https://github.com/textualize/rich/raw/main/imgs/log.png)

Istnieje argument `log_locals`, który wyświetla tabelę zawierającą zmienne lokalne skąd wywołano metodę  log.

Metoda log może być używana do logowania do terminala dla długo działających aplikacji takich jak serwery, ale jest również bardzo dobrą pomocą w debugowaniu.

</details>
<details>
<summary>Handler Logów</summary>

Możesz także użyć wbudowanej [klasy Handler](https://rich.readthedocs.io/en/latest/logging.html), aby sformatować i pokolorować wyjście z modułu logging Pythona. Przykład poniżej:

![Logging](https://github.com/textualize/rich/raw/main/imgs/logging.png)

</details>

<details>
<summary>Emoji</summary>

Żeby wstawić emoji do wyjścia konsoli, umieść jego nazwę pomiędzy dwoma dwukropkami, na przykład:

```python
>>> console.print(":smiley: :vampire: :pile_of_poo: :thumbs_up: :raccoon:")
😃 🧛 💩 👍 🦝
```

Korzystaj z tej funkcji rozsądnie.

</details>

<details>
<summary>Tabele</summary>

Rich może wyświetlać elastyczne [tabele](https://rich.readthedocs.io/en/latest/tables.html) ze znakami unicode box. Istnieje duża różnorodność opcji formatowania, stylów, wyrównywania komórek itp.

![table movie](https://github.com/textualize/rich/raw/main/imgs/table_movie.gif)

Powyższa animacja została wygenerowana z [table_movie.py](https://github.com/textualize/rich/blob/main/examples/table_movie.py) w folderze examples.

Poniżej prostszy przykład:

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

Ten kod wyświetla poniższy tekst:

![table](https://github.com/textualize/rich/raw/main/imgs/table.png)

Markup konsoli jest renderowany w ten sam sposób co `print()` i `log()`. Tak naprawdę wszystko co może być wyświetlone przez Richa może być zawarte w nagłówkach / wierszach (nawet inne tabele).

Klasa `Table` jest na tyle mądra, że zmienia wielkość kolumn, aby zmieścić się w dostępnej szerokości terminala, zawijając tekst jeśli potrzeba. Poniżej ten sam przykład z mniejszą wielkością terminala:

![table2](https://github.com/textualize/rich/raw/main/imgs/table2.png)

</details>

<details>
<summary>Paski Postępu</summary>

Rich może renderować wiele niemrugających pasków [postępu](https://rich.readthedocs.io/en/latest/progress.html), aby można było śledzić długo trwające zadania.

Dla podstawowego użycia, owiń jakąkolwiek sekwencję w funkcji `track` i iteruj nad wynikiem. Przykład poniżej:

```python
from rich.progress import track

for step in track(range(100)):
    do_step(step)
```

Nie jest trudniejsze dodanie wielu pasków postępu. Poniżej przykład z dokumentacji:

![progress](https://github.com/textualize/rich/raw/main/imgs/progress.gif)

Kolumny mogą być skonfigurowane, tak aby wyświetlać jakiekolwiek detale chcesz. Wbudowane kolumny zawierają stopień ukończenia (w %), wielkość pliku, szybkość operacji i pozostały czas. Poniżej kolejny przykład pokazujący pobieranie w toku.

![progress](https://github.com/textualize/rich/raw/main/imgs/downloader.gif)

Możesz wypróbować tę funkcję samemu, patrz [examples/downloader.py](https://github.com/textualize/rich/blob/main/examples/downloader.py), który może pobierać wiele URLów jednocześnie, pokazując postęp.

</details>

<details>
<summary>Status</summary>

W sytuacjach, gdzie ciężko jest wyliczyć postęp, można użyć metody [status](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console.status), która wyświetli animację 'spinnera' i wiadomość. Animacja nie przeszkodzi ci w używaniu konsoli normalnie. Przykład poniżej:

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

Generuje to następującą linijkę.

![status](https://github.com/textualize/rich/raw/main/imgs/status.gif)

Animacje spinnera zostały zapożyczone z [cli-spinners](https://www.npmjs.com/package/cli-spinners). Możesz wybrać spinnera określając parametr `spinner`. Wykonaj następującą komendę, aby zobaczyć dostępne wartości:

```
python -m rich.spinner
```

To polecenie generuje następujący tekst:

![spinners](https://github.com/textualize/rich/raw/main/imgs/spinners.gif)\

</details>

<details>
<summary>Tree</summary>

Rich może renderować drzewo - [tree](https://rich.readthedocs.io/en/latest/tree.html) zgodnie z wytycznymi. Drzewo jest idealne do wyświetlania struktury pliku, albo jakiekolwiek inne dane hierarchiczne.

Etykiety drzewa mogą być prostym tekstem albo czymkolwiek innym, co może wyświetlić Rich. Wykonaj poniższe polecenie dla demonstracji:

```
python -m rich.tree
```

To polecenie generuje następujący tekst:

![markdown](https://github.com/textualize/rich/raw/main/imgs/tree.png)

W pliku [tree.py](https://github.com/textualize/rich/blob/main/examples/tree.py) znajduje się przykład skryptu wyświetlającego widok drzewa jakiegokolwiek folderu, podobnie do linuxowej komendy `tree`.

</details>

<details>
<summary>Kolumny</summary>

Rich może wyświetlać zawartość w schludnych [kolumnach](https://rich.readthedocs.io/en/latest/columns.html) z równą, lub optymalną szerokością. Poniżej znajduje się bardzo podstawowy klon komendy (MacOSa / Linuxa) `ls`, która wyświetla zawartość folderu w kolumnach:

```python
import os
import sys

from rich import print
from rich.columns import Columns

directory = os.listdir(sys.argv[1])
print(Columns(directory))
```

Poniższy zrzut ekranu prezentuje wyjście [przykładu kolumn](https://github.com/textualize/rich/blob/main/examples/columns.py), wyświetlającego dane pobrane z API w kolumnach:

![columns](https://github.com/textualize/rich/raw/main/imgs/columns.png)

</details>

<details>
<summary>Markdown</summary>

Rich może renderować [markdown](https://rich.readthedocs.io/en/latest/markdown.html) i wykonuje niezłą pracę tłumaczenia formatowania do terminalu.

Aby wyrenderować markdown, zaimportuj klasę `Markdown` i skonstruuj z ciągiem zawierającym kod markdown. Potem wydrukuj ją do konsoli. Przykład poniżej:

```python
from rich.console import Console
from rich.markdown import Markdown

console = Console()
with open("README.md") as readme:
    markdown = Markdown(readme.read())
console.print(markdown)
```

Ten kod wyświetli tekst w stylu:

![markdown](https://github.com/textualize/rich/raw/main/imgs/markdown.png)

</details>

<details>
<summary>Podświetlanie kodu źródłowego</summary>

Rich używa biblioteki [pygments](https://pygments.org/), żeby zaimplementować [podświetlanie kodu źródłowego](https://rich.readthedocs.io/en/latest/syntax.html). Użycie jest podobne do renderowania markdownu; skonstruuj obiekt `Syntax` i wydrukuj go do konsoli. Przykład poniżej:

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

Ten kod wyświetli:

![syntax](https://github.com/textualize/rich/raw/main/imgs/syntax.png)

</details>

<details>
<summary>Tracebacki</summary>

Rich może renderować [piękne tracebacki](https://rich.readthedocs.io/en/latest/traceback.html), będące łatwiejsze do czytania i wyświetlają więcej kodu niż standardowe tracebacki Pythona. Można ustawić Richa jako domyślny handler tracebacków, żeby wszystkie niewyłapane wyjątki (błędy) były renderowane przez Richa.
 • [Polskie readme](https://github.com/textualize/rich/blob/main/README.pl.md)
