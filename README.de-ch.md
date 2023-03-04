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

Rich isch ä Python Library för _rich_ Text ond ganz schöni formatiärig im Törminäl

D [Rich API](https://rich.readthedocs.io/en/latest/) machts ganz eifach zom Farbä ond Stiil zu de Törminälusgob hinzu z füäge. Rich cha au schöni Tabelle, Progressbare, Markdown, Syntax hervorhebe, Tracebäcks und meh darstelle — fix fertig usem Böxli.

![Features](https://github.com/textualize/rich/raw/master/imgs/features.png)

E Video Iifüärig öber Rich geds onder [calmcode.io](https://calmcode.io/rich/introduction.html) vo [@fishnets88](https://twitter.com/fishnets88).

Lueg was [anderi öber Rich säged](https://www.willmcgugan.com/blog/pages/post/rich-tweets/).

## Kompatibilität

Rich funktioniert mit Linux, OSX ond Windows. True color / emoji funktioniert mit em neue Windows Törminäl, s klassische Törminäl isch of 16 Farbe limitiärt. Rich brucht Python 3.6.3 oder neuer.

Rich funktioniert mit [Jupyter notebooks](https://jupyter.org/) ohni irgendwelchä zuäsätzloche konfiguration.

## Installation

Installation mit `pip` oder mit dim liäblings PyPI Päckli-Manager.

```sh
python -m pip install rich
```

Für das do us zum d Rich usgob im Törminäl z teste:

```sh
python -m rich
```

## Rich Print

Zom ohni Ufwand Rich Usgob zu dinnere Applikation hinzuäfüäge, chasch eifach d [rich print](https://rich.readthedocs.io/en/latest/introduction.html#quick-start) Methodä importiäre, weli di glich Signatuur hed wiä d Builtin Python Funktion. Versuech das:

```python
from rich import print

print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())
```

![Hello World](https://github.com/textualize/rich/raw/master/imgs/print.png)

## Rich REPL

Rich cha i de Python REPL installiert werde so dass irgend e Datestruktuur hübsch usgeh ond Highlighted wird.

```python
>>> from rich import pretty
>>> pretty.install()
```

![REPL](https://github.com/textualize/rich/raw/master/imgs/repl.png)

## Console bruchä

Für meh kontrolle öber de Törminäl inhalt, importiär und instanziär e [Console](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console) Objekt.

```python
from rich.console import Console

console = Console()
```

S Console Objekt hät e `print` Methode mitäre absichtloch gliche Schnittstell wiä d Builtin `print` Funktion. Do es Bispiil wiä mos brucht:

```python
console.print("Hello", "World!")
```

Wiä erwartet wird `"Hello World!"` im Törminäl usgeh. Beach das im gägesatz zu de Builtin `print` Funktion, Rich de text so ombricht das es id Törminäl breiti ine passt.

Es ged es paar Wäg zom Farb und Stiil zu de Usgob hinzuä z füäge. Me cha en stiil a de ganze Usgob zuäwiise i dem mo s Schlösselwortargument `style` verwendet. Do es Bispiil:

```python
console.print("Hello", "World!", style="bold red")
```

D Usgob gsiät öppe ä so us:

![Hello World](https://github.com/textualize/rich/raw/master/imgs/hello_world.png)

Da isch guät für d Gstalltig vom Text pro Liniä. Vör ä granularäri Gstalltig hed Rich e spezielli Markup mitäre ähnloche Befehlsufbau wiä [bbcode](https://en.wikipedia.org/wiki/BBCode). Do es Bispiil:

```python
console.print("Where there is a [bold cyan]Will[/bold cyan] there [u]is[/u] a [i]way[/i].")
```

![Console Markup](https://github.com/textualize/rich/raw/master/imgs/where_there_is_a_will.png)

Du chasch mitmäne Console Objekt mit wenig Ufwand aasprechendi Usgob erziile. Lueg do d [Console API](https://rich.readthedocs.io/en/latest/console.html) Dokumentation für d Details a.

## Rich Inspect

Rich hät e [inspect](https://rich.readthedocs.io/en/latest/reference/init.html?highlight=inspect#rich.inspect) Funktion wo cha Bricht öber jeglochi Python Objekt, wie Class, Instanz oder Builtin erstelle.

```python
>>> my_list = ["foo", "bar"]
>>> from rich import inspect
>>> inspect(my_list, methods=True)
```

![Log](https://github.com/textualize/rich/raw/master/imgs/inspect.png)

Lueg do d [inspect Dokumentation](https://rich.readthedocs.io/en/latest/reference/init.html#rich.inspect) für d Details a.

# Rich-Bibliothek

Rich häd ä Aazahl vo integriäte _renderables_ wo du chasch verwende zum eleganti Usgobe i dinner e CLI generiäre ond der hälfed bim debugge vo dim Code.

Drock of di folgende Öberschrifte für d Details:

<details>
<summary>Log</summary>

S Console Objekt hät e `log()` Methode wo verglichbar zu de `print()` Schnittstell isch aber zuäsätzloch no e Spaltä för di aktuäll Zitt und d Datai mit de Zille wo de Ufruäf macht us git. Standardmässig tuät Rich es Syntax Highlighting für Python Strukturä sowiä repr Text machä. Went e Collection (wiä zum Bispiil dict oder list) loggsch wird Rich das hübsch Usgeh so dass es i de verfüägbari Platz ine passt. Do es Bispiil für e paar vo dene Funktionä.

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

Das do obe gid di folgend Usgob:

![Log](https://github.com/textualize/rich/raw/master/imgs/log.png)

Beachte s Argument `log_locals` wo innere Tabelle di lokalä Variable us gid zur Zitt wo d Methodä ufgruäfä worde isch.

D log Methodä cha zum is Törminäl inne z Logge für langläbige Applikationä wie Server brucht werde isch aber au fürs Debuggä ganz e netti Hilf.

</details>
<details>
<summary>Logging Handler</summary>

Du chasch au d Builtin [Handler Class](https://rich.readthedocs.io/en/latest/logging.html) verwende zum d Usgob vom Python logging Module z formatiäre und iifärbe. Do es Bispiil vo de Usgob:

![Logging](https://github.com/textualize/rich/raw/master/imgs/logging.png)

</details>

<details>
<summary>Emoji</summary>

Zom e Emoji i de Konsoleusgob iizfüäge tuä de name züschet zwei Doppelpünkt. Do es Bispiil:

```python
>>> console.print(":smiley: :vampire: :pile_of_poo: :thumbs_up: :raccoon:")
😃 🧛 💩 👍 🦝
```

Bitte verwend diä Funktion gschiid.

</details>

<details>
<summary>Tabelle</summary>

Rich cha flexiibäl [Tabelle](https://rich.readthedocs.io/en/latest/tables.html) mit Boxä us Unicodezeiche generiäre. Es gid e Viilzahl vo Formatiärigsoptionä für Ränder, Stiil, Zelleusrichtig ond so witter.

![table movie](https://github.com/textualize/rich/raw/master/imgs/table_movie.gif)

D Animation obe isch mit [table_movie.py](https://github.com/textualize/rich/blob/master/examples/table_movie.py) us em Bispiil-Ordner erstellt worde.

Do es eifachs Tabelle-Bispiil:

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

Das gid di folgend Usgob:

![table](https://github.com/textualize/rich/raw/master/imgs/table.png)

Beacht das d Konsole Markup glich wie bi `print()` ond `log()` generiärt wird. Ond zwor cha alles wo vo Rich generiert werde cha au im Chopf / Zille iigfüägt werde (sogar anderi Tabellene).

D Klass `Table` isch gschiid gnuäg yum d Spaltebreite am verfüägbare Platz im Törminäl aazpasse und de Text gegäbenefalls umzbreche. Do isch s gliche Bispiil mit em Törminäl chlinner als d Tabelle vo obe:

![table2](https://github.com/textualize/rich/raw/master/imgs/table2.png)

</details>

<details>
<summary>Progress Bars</summary>

Rich cha meereri flackerfreii [Progress](https://rich.readthedocs.io/en/latest/progress.html) Bars darstelle zum langläbigi Tasks verfolgä.

Zur eifache Benutzig irgend e Sequenz id `track` Funktion ine packe und über s Resultat iteriäre. Do es Bispiil:

```python
from rich.progress import track

for step in track(range(100)):
    do_step(step)
```

Es isch nöd vill schwiriger zum mehräri Progress Bars hinzuä zfüäge. Do es Bispiil us de Doku:

![progress](https://github.com/textualize/rich/raw/master/imgs/progress.gif)

D Spaltä cha so konfiguriärt werde das alli gwünschte Details aazeigt werded. D Built-in Spalte beinhaltät Prozentsatz, Dateigrössi, Dateigschwindikeit ond öbrigi Zitt. Do isch e andos Bispiil wo en laufände Download zeigt:

![progress](https://github.com/textualize/rich/raw/master/imgs/downloader.gif)

Zums selber usprobiäre lueg [examples/downloader.py](https://github.com/textualize/rich/blob/master/examples/downloader.py) a, wo cha glichzittig mehräri URLs abelade und de Fortschritt aazeige.

</details>

<details>
<summary>Status</summary>

För Situatione wos schwär isch zum de Fortschritt z berechne, chasch d [status](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console.status) Methode verwende wo en 'spinner' animiärt und e Nochricht darstellt. D Animation haltet di nöd ab d Konsole witter normal z bruche. Do es Bispiil:

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

Das gid di folgendi Usgob im Törminäl.

![status](https://github.com/textualize/rich/raw/master/imgs/status.gif)

D Spinner Animatione sind vo [cli-spinners](https://www.npmjs.com/package/cli-spinners) usglehnt. Du chasch en speziifischä Spinner mit em `spinner` Parameter uswähle. Start de folgend Befehl zom die verfüägbare Wert z gsiä:

```
python -m rich.spinner
```

De Befehl obe generiärt di folgändi Usgob im Törminäl:

![spinners](https://github.com/textualize/rich/raw/master/imgs/spinners.gif)

</details>

<details>
<summary>Tree</summary>

Rich cha en [tree](https://rich.readthedocs.io/en/latest/tree.html) mit Hilfsliniä generiäre. En Tree isch ideal zom darstelle vo Dateistruktuure oder anderi hirarchischi Date.

S Label vom Tree cha en eifache Text or alles andere wo Rich cha rendere. Start das Folgendi für e Demonstation:

```
python -m rich.tree
```

Das generiärt di folgend Usgob:

![markdown](https://github.com/textualize/rich/raw/master/imgs/tree.png)

Lueg s Bispiil Script [tree.py](https://github.com/textualize/rich/blob/master/examples/tree.py) für e Darstellig vo irgend eim Ordner als Tree, glich wie de Linux Befehl `tree`.

</details>

<details>
<summary>Spaltene</summary>

Rich cha Inhalt i hübsche [Spaltene](https://rich.readthedocs.io/en/latest/columns.html) darstelle mit glichä oder optimale Breiti. Do isch e ganz eifachi kopii vom (MacOS / Linux) `ls` Befehl wo Ordner in Spaltene darstellt

```python
import os
import sys

from rich import print
from rich.columns import Columns

directory = os.listdir(sys.argv[1])
print(Columns(directory))
```

De folgend Screenshot isch d Usgob vom [Spalte-Bispiil](https://github.com/textualize/rich/blob/master/examples/columns.py), wo Date vonnere API hollt ond in Spaltene darstellt:

![columns](https://github.com/textualize/rich/raw/master/imgs/columns.png)

</details>

<details>
<summary>Markdown</summary>

Rich cha [markdown](https://rich.readthedocs.io/en/latest/markdown.html) übersetze ond leistet vernünftigi Ärbät bim formatiärige is Törminäl z übersetze.

Zum Markdown z übersetze importier d Klass `Markdown` und instanzier es mitem Markdown Text. Nocher gid mos uf de Konsolä us. Do es Bispiil:

```python
from rich.console import Console
from rich.markdown import Markdown

console = Console()
with open("README.md") as readme:
    markdown = Markdown(readme.read())
console.print(markdown)
```

Das wird d Usgob ungefär wie s Folgende geh:

![markdown](https://github.com/textualize/rich/raw/master/imgs/markdown.png)

</details>

<details>
<summary>Syntax Highlighting</summary>

Rich brucht d [pygments](https://pygments.org/) Library für d [Syntax Highlighting](https://rich.readthedocs.io/en/latest/syntax.html). S Bruche isch ähnloch zum Markdown übersetze; instanziär e `Syntax` Objekt ond gibs uf de Konsolä us. Do es Bispiil:

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

Das wird d Usgob ungefär wie s Folgende geh:

![syntax](https://github.com/textualize/rich/raw/master/imgs/syntax.png)

</details>

<details>
<summary>Tracebacks</summary>

Rich cha [wunderschöni Tracebacks](https://rich.readthedocs.io/en/latest/traceback.html) generiäre wo eifach zum läse sind und meh Code als de Standard-Python-Traceback darstellt. Du chasch Rich als default Traceback Handler setzä ond alli nöd abfangene Exceptions werded mit Rich dargstellt.

So gsiets ungefär ufemen OSX (ähnloch uf Linux) us:

![traceback](https://github.com/textualize/rich/raw/master/imgs/traceback.png)

</details>

Alli Rich Renderables bruched s [Console-Protokoll](https://rich.readthedocs.io/en/latest/protocol.html), wo mo au für d eige Entwicklig vo Rich-Inhalt cha bruche.

# Rich für Ondernemä

Verfüägbar als Tidelift Abo.

De Betreue vo Rich ond tuusigi anderi Päkli schaffed mit Tidelift zum komerziälle Support und Wartig für Open Source Päkli wo du zum Baue vo dinnere Applikation bruchsch. Spar Zit, reduziär s Risiko ond verbessere d Code Health mit em bezahle vo de Wartig für gnau die Päkli wo mo brucht. [Lärn meh.](https://tidelift.com/subscription/pkg/pypi-rich?utm_source=pypi-rich&utm_medium=referral&utm_campaign=enterprise&utm_term=repo)

# Projekt wo Rich bruched

Do es paar Projekt wo Rich verwended:

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
- +[Vieli meh](https://github.com/textualize/rich/network/dependents)!

<!-- This is a test, no need to translate -->
