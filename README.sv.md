# Rich

[![PyPI version](https://badge.fury.io/py/rich.svg)](https://badge.fury.io/py/rich)
[![codecov](https://codecov.io/gh/willmcgugan/rich/branch/master/graph/badge.svg)](https://codecov.io/gh/willmcgugan/rich)
[![Rich blog](https://img.shields.io/badge/blog-rich%20news-yellowgreen)](https://www.willmcgugan.com/tag/rich/)
[![Twitter Follow](https://img.shields.io/twitter/follow/willmcgugan.svg?style=social)](https://twitter.com/willmcgugan)

[中文 readme](https://github.com/willmcgugan/rich/blob/master/README.cn.md) • [lengua española readme](https://github.com/willmcgugan/rich/blob/master/README.es.md)

Rich är ett Python bibliotek för _rich_ text och vacker formattering i terminalen.

[Rich API](https://rich.readthedocs.io/en/latest/) gör det enkelt att lägga till färg och stil till terminal utmatning. Rich kan också framställa fina tabeller, framstegsfält, märkspråk, syntaxmarkerad källkod, tillbaka-spårning, och mera - redo att använda.

![Funktioner](https://github.com/willmcgugan/rich/raw/master/imgs/features.png)

För en video demonstration av Rich kolla [calmcode.io](https://calmcode.io/rich/introduction.html) av [@fishnets88](https://twitter.com/fishnets88).

Se vad [folk pratar om Rich](https://www.willmcgugan.com/blog/pages/post/rich-tweets/).

## Kompatibilitet

Rich funkar med Linux, OSX, och Windows. Sann färg / emoji funkar med nya Windows Terminalen, klassiska terminal är begränsad till 8 färger. Rich kräver Python 3.6.1 eller senare.

Rich funkar med [Jupyter notebooks](https://jupyter.org/) utan någon ytterligare konfiguration behövd.

## Installering

Installera med `pip` eller din favorita PyPi packet hanterare.

```
pip install rich
```

Kör följade följande för att testa Rich utmatning i din terminal:

```
python -m rich
```

## Rich utskrivningsfunktion

För att enkelt lägga till rich utmatning i din applikation, kan du importera [rich print](https://rich.readthedocs.io/en/latest/introduction.html#quick-start) metoden, vilket har den samma signatur som den inbyggda Python funktionen. Testa detta:

```python
from rich import print

print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())
```

![Hello World](https://github.com/willmcgugan/rich/raw/master/imgs/print.png)

## Rich REPL

Rich kan installeras i Python REPL, så att varje datastruktur kommer att skrivas ut fint och markeras. 

```python
>>> from rich import pretty
>>> pretty.install()
```

![REPL](https://github.com/willmcgugan/rich/raw/master/imgs/repl.png)

## Rich Inspektera

Rich har en [inspektionsfunktion](https://rich.readthedocs.io/en/latest/reference/init.html?highlight=inspect#rich.inspect) som kan producera en rapport om vilket Python objekt som helst, till exempel klass, instans, eller inbyggt.

```python
>>> from rich import inspect
>>> inspect(str, methods=True)
```

## Användning av konsolen

För mer kontroll över rich terminal innehållsutmatning, importera och konstruera ett [Console](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console) objekt.

```python
from rich.console import Console

console = Console()
```

`Console` objektet har en `print` metod vilket har ett avsiktligt liknande gränssnitt till den inbyggda `print` funktionen. Här är ett exempel av användningen:

```python
console.print("Hello", "World!")
```

Som du möjligtvis anar, detta kommer skriva ut `"Hello World!"` till terminalen. Notera att till skillnad från den inbyggda `print` funktionen, Rich kommer att radbryta din text så att den passar inom terminalbredden.

Det finns ett par sätt att lägga till färg och stil till din utmatning. Du kan sätta en stil för hela utmatningen genom att addera ett `style` nyckelord argument. Här är ett exempel:

```python
console.print("Hello", "World!", style="bold red")
```

Utmatningen kommer bli något liknande:

![Hello World](https://github.com/willmcgugan/rich/raw/master/imgs/hello_world.png)

Det är bra för att ge stil till en textrad åt gången. För mer finkornad stilisering, Rich framställer en speciell märkspråk vilket liknar [bbcode](https://en.wikipedia.org/wiki/BBCode) i syntax. Här är ett exempel:

```python
console.print("Where there is a [bold cyan]Will[/bold cyan] there [u]is[/u] a [i]way[/i].")
```

![Konsol märkspråk](https://github.com/willmcgugan/rich/raw/master/imgs/where_there_is_a_will.png)

### Konsollogging

`Console` objektet har en `log()` metod vilket har liknande gränssnitt som `print()`, men framställer även en kolumn för den nuvarande tid och fil samt rad vilket gjorde anroppet. Som standard kommer Rich att markera syntax för Python strukturer och för repr strängar. Ifall du loggar en samling (det vill säga en ordbok eller en lista) kommer Rich att finskriva ut det så att det passar i det tillgängliga utrymme. Här är ett exempel av dessa funktioner.

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

Det ovanstående har följande utmatning:

![Log](https://github.com/willmcgugan/rich/raw/master/imgs/log.png)

Notera `log_locals` argumentet, vilket utmatar en tabell innehållandes de lokala variablerna varifrån log metoden kallades från.

Log metoden kan användas för att logga till terminal för långkörande applikationer så som servrar, men är också en väldigt bra felsökningsverktyg.

### Loggningshanterare

Du kan också använda den inbyggda [Handler klassen](https://rich.readthedocs.io/en/latest/logging.html) för att formatera och färglägga utmatningen från Pythons loggningsmodul. Här är ett exempel av utmatningen:

![Loggning](https://github.com/willmcgugan/rich/raw/master/imgs/logging.png)

## Emoji

För att infoga en emoji till konsolutmatningen placera namnet mellan två kolon. Här är ett exempel:

```python
>>> console.print(":smiley: :vampire: :pile_of_poo: :thumbs_up: :raccoon:")
😃 🧛 💩 👍 🦝
```

Vänligen använd denna funktion klokt.

## Tabell

Rich kan framställa flexibla [tabeller](https://rich.readthedocs.io/en/latest/tables.html) med unicode boxkaraktärer. Det finns en stor mängd av formateringsalternativ för gränser, stilar, och celljustering etc.

![Tabell film](https://github.com/willmcgugan/rich/raw/master/imgs/table_movie.gif)

Animationen ovan genererades utav [table_movie.py](https://github.com/willmcgugan/rich/blob/master/examples/table_movie.py) i exempelkatalogen.

Här är ett exempel av en enklare tabell:

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

Detta producerar följande utmatning:

![tabell](https://github.com/willmcgugan/rich/raw/master/imgs/table.png)

Notera att konsol märkspråk är framställt på samma sätt som `print()` och `log()`. I själva verket, vad som helst som är framställt av Rich kan inkluderas i rubriker / rader (även andra tabeller).

`Table` klassen är smart nog att storleksändra kolumner att passa den tillgängliga bredden av terminalen, och slår in text ifall det behövs. Här är samma exempel, med terminalen gjord mindre än tabell ovan:

![tabell2](https://github.com/willmcgugan/rich/raw/master/imgs/table2.png)

## Framstegsfält

Rich kan framställa flera flimmerfria [framstegsfält](https://rich.readthedocs.io/en/latest/progress.html) för att följa långvariga uppgifter.

För grundläggande användning, slå in valfri sekvens i `track` funktion och iterera över resultatet. Här är ett exempel:

```python
from rich.progress import track

for step in track(range(100)):
    do_step(step)
```

Det är inte mycket svårare att lägga till flera framstegsfält. Här är ett exempel tagen från dokumentationen:

![framsteg](https://github.com/willmcgugan/rich/raw/master/imgs/progress.gif)

Dessa kolumner kan konfigureras att visa vilka detaljer du vill. Inbyggda kolumner inkluderar procentuell färdig, filstorlek, filhastighet, och återstående tid. Här är ännu ett exempel som visar en pågående nedladdning:

![framsteg](https://github.com/willmcgugan/rich/raw/master/imgs/downloader.gif)

För att själv testa detta, kolla [examples/downloader.py](https://github.com/willmcgugan/rich/blob/master/examples/downloader.py) vilket kan ladda ner flera URLs samtidigt medan visar framsteg.

## Status

För situationer där det är svårt att beräkna framsteg, kan du använda [status](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console.status) metoden vilket kommer visa en 'snurra' animation och meddelande. Animationen hindrar dig inte från att använda konsolen som normalt. Här är ett exempel:

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

Detta genererar följande utmatning i terminalen.

![status](https://github.com/willmcgugan/rich/raw/master/imgs/status.gif)

Snurra animationen är lånad ifrån [cli-spinners](https://www.npmjs.com/package/cli-spinners). Du kan välja en snurra genom att specifiera `spinner` parametern. Kör följande kommando för att se tillgängliga värden:

```
python -m rich.spinner
```

Kommandot ovan genererar följande utmatning i terminalen:

![Snurror](https://github.com/willmcgugan/rich/raw/master/imgs/spinners.gif)

## Träd

Rich kan framställa ett [träd](https://rich.readthedocs.io/en/latest/tree.html) med riktlinjer. Ett träd är idealt för att visa en filstruktur, eller andra hierarkiska data.

Etiketter på trädet kan vara enkelt text eller något annat som Rich kan framställa. Kör följande för en demonstration:

```
python -m rich.tree
```

Detta genererar följande utmatning:

![märkspråk](https://github.com/willmcgugan/rich/raw/master/imgs/tree.png)

Se [tree.py](https://github.com/willmcgugan/rich/blob/master/examples/tree.py) exemplet för ett skript som visar en trädvy av vilken katalog som helst, som liknar linux `tree` kommandot.

## Kolumner

Rich kan framställa innehåll i prydliga [kolumner](https://rich.readthedocs.io/en/latest/columns.html) med lika eller optimal bredd. Här är en grundläggande klon av (MacOS / Linux) `ls` kommandot vilket visar en kataloglista i kolumner:

```python
import os
import sys

from rich import print
from rich.columns import Columns

directory = os.listdir(sys.argv[1])
print(Columns(directory))
```

Följande skärmdump är resultatet från [kolumner exempelet](https://github.com/willmcgugan/rich/blob/master/examples/columns.py) vilket visar data tagen från ett API i kolumner:

![kolumner](https://github.com/willmcgugan/rich/raw/master/imgs/columns.png)

## Märkspråk

Rich kan framställa [märkspråk](https://rich.readthedocs.io/en/latest/markdown.html) och gör ett rimligt jobb med att översätta formateringen till terminalen.

För att framställa märkspråk importera `Markdown` klassen och konstruera den med en sträng innehållandes märkspråkskod. Mata sedan ut det till konsolen. Här är ett exempel:

```python
from rich.console import Console
from rich.markdown import Markdown

console = Console()
with open("README.md") as readme:
    markdown = Markdown(readme.read())
console.print(markdown)
```

Detta kommer att producera utmatning som liknar följande:

![märkspråk](https://github.com/willmcgugan/rich/raw/master/imgs/markdown.png)

## Syntaxmarkering

Rich använder [pygments](https://pygments.org/) biblioteket för att implementera [syntax markering](https://rich.readthedocs.io/en/latest/syntax.html). Användningen är liknande till framställa märkspråk; konstruera ett `Syntax` objekt och skriv ut den till konsolen. Här är ett exempel:

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

Detta kommer producera följande utmatning:

![syntax](https://github.com/willmcgugan/rich/raw/master/imgs/syntax.png)

## Tillbaka-spårning

Rich kan framställa [vackra tillbaka-spårningar](https://rich.readthedocs.io/en/latest/traceback.html) vilket är enklare att läsa och visar mer kod än vanliga Python tillbaka-spårningar. Du kan sätta Rich som standard tillbaka-spårningshanterare så att alla ofångade undantag kommer att framställas av Rich.

Så här ser det ut på OSX (liknande på Linux):

![traceback](https://github.com/willmcgugan/rich/raw/master/imgs/traceback.png)

## Projekt som använder sig av Rich

Här är ett par projekt som använder Rich:

- [BrancoLab/BrainRender](https://github.com/BrancoLab/BrainRender)
  ett python packet för visualisering av tredimensionell neuro-anatomiska data
- [Ciphey/Ciphey](https://github.com/Ciphey/Ciphey)
  Automatiserat dekrypteringsverktyg
- [emeryberger/scalene](https://github.com/emeryberger/scalene)
  en högpresterande processor med hög precision och minnesprofilerare för Python
- [hedythedev/StarCli](https://github.com/hedythedev/starcli)
  Bläddra bland trendande projekt i Github från din kommandotolk
- [intel/cve-bin-tool](https://github.com/intel/cve-bin-tool)
  Detta verktyg skannar efter vanliga, sårbara komponenter (openssl, libpng, libxml2, expat och en del andra) för att låta dig veta ifall ditt system inkluderar vanliga bibliotek med kända sårbarheter.
- [nf-core/tools](https://github.com/nf-core/tools)
  Python packet med hjälpverktyg för nf-core gemenskapen.
- [cansarigol/pdbr](https://github.com/cansarigol/pdbr)
  pdb + Rich bibliotek för förbättrad felsökning.
- [plant99/felicette](https://github.com/plant99/felicette)
  Satellitbilder för nybörjare.
- [seleniumbase/SeleniumBase](https://github.com/seleniumbase/SeleniumBase)
  Automatisera & testa 10x snabbare med Selenium & pytest. Batterier inkluderat.
- [smacke/ffsubsync](https://github.com/smacke/ffsubsync)
  Automagiskt synkronisera undertexter med video.
- [tryolabs/norfair](https://github.com/tryolabs/norfair)
  Lättvikt Python bibliotek för att addera 2d-objektspårning i realtid till vilken detektor som helst.
- [ansible/ansible-lint](https://github.com/ansible/ansible-lint) Ansible-lint kontroller playbooks för dess metoder och beteenden som potentiellt kan förbättras
- [ansible-community/molecule](https://github.com/ansible-community/molecule) Ansible Molecule ramverk för testning
- +[Many more](https://github.com/willmcgugan/rich/network/dependents)!
