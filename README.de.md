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

Rich ist eine Python-Bibliothek für _rich_ Text und schöne Formatierung im Terminal.

Die [Rich API](https://rich.readthedocs.io/en/latest/) erleichtert das Hinzufügen von Farbe und Stil zur Terminalausgabe. Rich kann auch schöne Tabellen, Fortschrittsbalken, Markdowns, durch Syntax hervorgehobenen Quellcode, Tracebacks und mehr sofort rendern.

![Features](https://github.com/textualize/rich/raw/main/imgs/features.png)

Eine Video-Einführung in Rich findest du unter [quietcode.io](https://calmcode.io/rich/introduction.html) von [@ fishnets88](https://twitter.com/fishnets88).

Schau hier, was [andere über Rich sagen](https://www.willmcgugan.com/blog/pages/post/rich-tweets/).

## Kompatibilität

Rich läuft unter Linux, OSX und Windows. True Color / Emoji funktionieren mit dem neuen Windows-Terminal. Das klassische Terminal ist auf 16 Farben beschränkt. Rich benötigt Python 3.6.3 oder höher.

Rich funktioniert ohne zusätzliche Konfiguration mit [Jupyter Notebooks](https://jupyter.org/).

## Installation

Installation mit `pip` oder deinem bevorzugten PyPI-Paketmanager.

```sh
python -m pip install rich
```

Führe die folgenden Schritte aus, um die Rich-Ausgabe auf deinem Terminal zu testen:

```sh
python -m rich
```

## Rich Print

Um deiner Anwendung mühelos eine Rich-Ausgabe hinzuzufügen, kannst du die Methode [rich print](https://rich.readthedocs.io/en/latest/introduction.html#quick-start) importieren, die dieselbe Signatur wie die integrierte Python-Funktion hat. Versuche das:

```python
from rich import print

print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())
```

![Hello World](https://github.com/textualize/rich/raw/main/imgs/print.png)

## Rich REPL

Rich kann in Python REPL installiert werden, so dass alle Datenstrukturen schön ausgegeben und hervorgehoben werden.

```python
>>> from rich import pretty
>>> pretty.install()
```

![REPL](https://github.com/textualize/rich/raw/main/imgs/repl.png)

## Verwenden der Konsole

Importiere und erstelle ein [Konsolen-Objekt](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console), um mehr Kontrolle über umfangreiche Terminalinhalte zu erhalten.

```python
from rich.console import Console

console = Console()
```

Das Konsolenobjekt verfügt über eine `print`-Methode, die eine absichtlich gleiche Schnittstelle zur integrierten `print`-Funktion aufweist. Hier ein Anwendungsbeispiel:

```python
console.print("Hello", "World!")
```

Wie zu erwarten, wird `"Hello World!"` im Terminal ausgegeben. Beachte, dass Rich im Gegensatz zur integrierten `print`-Funktion deinen Text so umbricht, dass er in die Terminalbreite passt.

Es gibt verschiedene Möglichkeiten, deiner Ausgabe Farbe und Stil hinzuzufügen. Du kannst einen Stil für die gesamte Ausgabe festlegen, indem du ein Schlüsselwortargument `style` hinzufügst. Hier ein Beispiel:

```python
console.print("Hello", "World!", style="bold red")
```

Die Ausgabe wird in etwa wie folgt aussehen:

![Hello World](https://github.com/textualize/rich/raw/main/imgs/hello_world.png)

Das ist gut, um jeweils eine Textzeile zu stylen. Für eine detailliertere Gestaltung bietet Rich ein spezielles Markup an, das in der Syntax ähnlich [bbcode](https://en.wikipedia.org/wiki/BBCode) ist. Hier ein Beispiel:

```python
console.print("Where there is a [bold cyan]Will[/bold cyan] there [u]is[/u] a [i]way[/i].")
```

![Console Markup](https://github.com/textualize/rich/raw/main/imgs/where_there_is_a_will.png)

Du kannst ein Console-Objekt verwenden, um mit minimalem Aufwand anspruchsvolle Ausgaben zu erzeugen. Siehe [Konsolen-API](https://rich.readthedocs.io/en/latest/console.html) für Details.

## Rich Inspect

Rich hat eine Funktion [inspect](https://rich.readthedocs.io/en/latest/reference/init.html?highlight=inspect#rich.inspect), die einen Bericht über jedes Python-Objekt, wie Klasse, Instanz oder builtin, erzeugen kann.

```python
>>> my_list = ["foo", "bar"]
>>> from rich import inspect
>>> inspect(my_list, methods=True)
```

![Log](https://github.com/textualize/rich/raw/main/imgs/inspect.png)

Siehe [Doks Inspektor](https://rich.readthedocs.io/en/latest/reference/init.html#rich.inspect) für Details.

# Rich-Bibliothek

Rich enthält eine Reihe von eingebauten _renderables_, die du verwenden kannst, um elegante Ausgaben in deiner CLI zu erzeugen und dir beim Debuggen deines Codes zu helfen.

Klicke auf die folgenden Überschriften, um Details zu erfahren:

<details>
<summary>Log</summary>

Das Console-Objekt hat eine `log()`-Methode, die die gleiche Schnittstelle wie `print()` hat, aber zusätzlich eine Spalte für die aktuelle Zeit und die Datei und Zeile, die den Aufruf gemacht hat, ausgibt. Standardmäßig führt Rich die Syntaxhervorhebung für Python-Strukturen und für repr-Strings durch. Wenn du eine Sammlung (z.B. ein Diktat oder eine Liste) protokollierst, wird Rich diese so hübsch ausgeben, dass sie in den verfügbaren Platz passt. Hier ein Beispiel für einige dieser Funktionen.

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

Die obige Funktion erzeugt die folgende Ausgabe:

![Log](https://github.com/textualize/rich/raw/main/imgs/log.png)

Beachte das Argument `log_locals`, das eine Tabelle mit den lokalen Variablen ausgibt, in der die log-Methode aufgerufen wurde.

Die log-Methode kann für die Protokollierung auf dem Terminal für langlaufende Anwendungen wie Server verwendet werden, ist aber auch eine sehr schöne Hilfe bei der Fehlersuche.

</details>
<details>
<summary>Logging Handler</summary>

Du kannst auch die eingebaute [Handler-Klasse](https://rich.readthedocs.io/en/latest/logging.html) verwenden, um die Ausgabe von Pythons Logging-Modul zu formatieren und einzufärben. Hier ein Beispiel für die Ausgabe:

![Logging](https://github.com/textualize/rich/raw/main/imgs/logging.png)

</details>

<details>
<summary>Emoji</summary>

Um ein Emoji in die Konsolenausgabe einzufügen, setze den Namen zwischen zwei Doppelpunkte. Hier ein Beispiel:

```python
>>> console.print(":smiley: :vampire: :pile_of_poo: :thumbs_up: :raccoon:")
😃 🧛 💩 👍 🦝
```

Bitte verwenden Sie diese Funktion mit Bedacht.

</details>

<details>
<summary>Tabellen</summary>

Rich kann flexible [Tabellen](https://rich.readthedocs.io/en/latest/tables.html) mit Unicode-Box-Characters darstellen. Es gibt eine Vielzahl von Formatierungsmöglichkeiten für Rahmen, Stile, Zellausrichtung usw.

![Film-Tabelle](https://github.com/textualize/rich/raw/main/imgs/table_movie.gif)

Die obige Animation wurde mit [table_movie.py](https://github.com/textualize/rich/blob/main/examples/table_movie.py) im Verzeichnis `examples` erzeugt.

Hier ist ein einfacheres Tabellenbeispiel:

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

Dies erzeugt diese Ausgabe:

![Tabelle](https://github.com/textualize/rich/raw/main/imgs/table.png)

Beachte, dass das Konsolen-Markup auf die gleiche Weise gerendert wird wie `print()` und `log()`. Tatsächlich kann alles, was von Rich gerendert werden kann, in den Kopfzeilen/Zeilen enthalten sein (sogar andere Tabellen).

Die Klasse `Table` ist intelligent genug, um die Größe der Spalten an die verfügbare Breite des Terminals anzupassen und den Text wie erforderlich umzubrechen. Hier ist das gleiche Beispiel, wobei das Terminal kleiner als bei der obigen Tabelle ist:

![Tabelle2](https://github.com/textualize/rich/raw/main/imgs/table2.png)

</details>

<details>
<summary>Fortschrittsbalken</summary>

Rich kann mehrere flackerfreie [Fortschrittsbalken](https://rich.readthedocs.io/en/latest/progress.html) darstellen, um langlaufende Aufgaben zu verfolgen.

Einfachste Anwendung ist, eine beliebige Sequenz in die Funktion `track` einzupacken und  über das Ergebnis zu iterieren. Hier ein Beispiel:

```python
from rich.progress import track

for step in track(range(100)):
    do_step(step)
```

Es ist nicht viel schwieriger, mehrere Fortschrittsbalken hinzuzufügen. Hier ein Beispiel aus der Doku:

![Fortschritt](https://github.com/textualize/rich/raw/main/imgs/progress.gif)

Die Spalten können so konfiguriert werden, dass sie alle gewünschten Details anzeigen. Zu den eingebauten Spalten gehören Prozentsatz der Fertigstellung, Dateigröße, Downloadgeschwindigkeit und verbleibende Zeit. Hier ist ein weiteres Beispiel, das einen laufenden Download anzeigt:

![Fortschritt](https://github.com/textualize/rich/raw/main/imgs/downloader.gif)

Um dies selbst auszuprobieren, sieh dir [examples/downloader.py](https://github.com/textualize/rich/blob/main/examples/downloader.py) an, das mehrere URLs gleichzeitig herunterladen kann und dabei den Fortschritt anzeigt.

</details>

<details>
<summary>Status</summary>

Für Situationen, in denen es schwierig ist, den Fortschritt zu berechnen, kannst du die Methode [status](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console.status) verwenden, die eine 'Spinner'-Animation und eine Meldung anzeigt. Die Animation hindert dich nicht daran, die Konsole wie gewohnt zu verwenden. Hier ein Beispiel:

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

Dies erzeugt diese Ausgabe im Terminal.

![Status](https://github.com/textualize/rich/raw/main/imgs/status.gif)

Die Spinner-Animationen wurden von [cli-spinners](https://www.npmjs.com/package/cli-spinners) geliehen. Du kannst einen Spinner auswählen, indem du den Parameter `spinner` angibst. Führe den folgenden Befehl aus, um die verfügbaren Werte zu sehen:

```
python -m rich.spinner
```

Der obige Befehl erzeugt die folgende Ausgabe im Terminal:

![Spinner](https://github.com/textualize/rich/raw/main/imgs/spinners.gif)

</details>

<details>
<summary>Baum</summary>

Rich kann einen [Baum](https://rich.readthedocs.io/en/latest/tree.html) mit Hilfslinien darstellen. Ein Baum ist ideal, um eine Dateistruktur oder andere hierarchische Daten darzustellen.

Die Beschriftungen des Baums können einfacher Text oder alles andere sein, was Rich rendern kann. Führe den folgenden Befehl zur Demonstration aus:

```
python -m rich.tree
```

Dies erzeugt diese Ausgabe:

![Markdown](https://github.com/textualize/rich/raw/main/imgs/tree.png)

Siehe das Beispiel [tree.py](https://github.com/textualize/rich/blob/main/examples/tree.py) für ein Skript, das eine Baumansicht eines beliebigen Verzeichnisses anzeigt, ähnlich dem Linux-Befehl `tree`.

</details>

<details>
<summary>Spalten</summary>

Rich kann Inhalte sauber in [Spalten](https://rich.readthedocs.io/en/latest/columns.html) mit gleicher oder optimaler Breite darstellen. Hier ist ein sehr einfacher Klon des (MacOS / Linux) `ls`-Befehls, der eine Verzeichnisliste in Spalten anzeigt:

```python
import os
import sys

from rich import print
from rich.columns import Columns

directory = os.listdir(sys.argv[1])
print(Columns(directory))
```

Der folgende Screenshot ist die Ausgabe von [Spalten-Beispiel](https://github.com/textualize/rich/blob/main/examples/columns.py), das Daten, die aus einer API kommen, in Spalten anzeigt:

![columns](https://github.com/textualize/rich/raw/main/imgs/columns.png)

</details>

<details>
<summary>Markdown</summary>

Rich kann [Markdown](https://rich.readthedocs.io/en/latest/markdown.html) rendern und leistet vernünftige Arbeit bei der Übersetzung der Formatierung ins Terminal.

Um Markdown zu rendern, importiere die Klasse `Markdown` und konstruiere einen String mit Markdown-Code. Gib ihn dann auf der Konsole aus. Hier ein Beispiel:

```python
from rich.console import Console
from rich.markdown import Markdown

console = Console()
with open("README.md") as readme:
    markdown = Markdown(readme.read())
console.print(markdown)
```

Dies erzeugt diese Ausgabe:

![markdown](https://github.com/textualize/rich/raw/main/imgs/markdown.png)

</details>

<details>
<summary>Syntax-Hervorhebung</summary>

Rich verwendet die Bibliothek [pygments](https://pygments.org/) zur Implementierung von [Syntax-Hervorhebung](https://rich.readthedocs.io/en/latest/syntax.html). Die Verwendung ist gleich dem Rendern von Markdown; konstruieren Sie ein `Syntax`-Objekt und gib es auf der Konsole aus. Hier ein Beispiel:

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

Dies erzeugt die folgende Ausgabe:

![Syntax](https://github.com/textualize/rich/raw/main/imgs/syntax.png)

</details>

<details>
<summary>Tracebacks</summary>

Rich kann [schöne Tracebacks](https://rich.readthedocs.io/en/latest/traceback.html) rendern, die einfacher zu lesen sind und mehr Code anzeigen, als die Standard-Python-Tracebacks. Du kannst Rich als Standard-Traceback-Handler festlegen, so dass alle nicht abgefangenen Exceptions von Rich gerendert werden.

So sieht es unter OSX aus (ähnlich unter Linux):

![Traceback](https://github.com/textualize/rich/raw/main/imgs/traceback.png)

</details>

Alle Rich-Renderables verwenden das [Konsolen-Protokoll](https://rich.readthedocs.io/en/latest/protocol.html), das du auch für die Implementierung deiner eigenen Rich-Inhalte verwenden kannst.

# Rich für Unternehmen

Verfügbar als Teil des Tidelift-Abonnements.

Die Betreuer von Rich und tausenden anderen Paketen arbeiten mit Tidelift zusammen, um kommerziellen Support und Wartung für die Open-Source-Pakete zu bieten, die du zur Erstellung deiner Anwendungen verwendest. Spare Zeit, reduziere Risiken und verbessere den Zustand des Codes, während du die Betreuer genau der Pakete bezahlen, die du verwendest. [Erfahre hier mehr.](https://tidelift.com/subscription/pkg/pypi-rich?utm_source=pypi-rich&utm_medium=referral&utm_campaign=enterprise&utm_term=repo)

# Projekte, die Rich verwenden

Hier sind ein paar Projekte, die Rich verwenden:

- [BrancoLab/BrainRender](https://github.com/BrancoLab/BrainRender)
  ein Python-Paket zur Visualisierung dreidimensionaler neuro-anatomischer Daten
- [Ciphey/Ciphey](https://github.com/Ciphey/Ciphey)
  Automatisiertes Entschlüsselungswerkzeug
- [emeryberger/scalene](https://github.com/emeryberger/scalene)
  ein leistungsstarker, hochpräziser CPU- und Speicher-Profiler für Python
- [hedythedev/StarCli](https://github.com/hedythedev/starcli)
  Durchsuchen von GitHub-Trending-Projekten in der Kommandozeile
- [intel/cve-bin-tool](https://github.com/intel/cve-bin-tool)
  Dieses Tool scannt nach einer Reihe von verbreiteten, verwundbaren Komponenten (openssl, libpng, libxml2, expat und ein paar andere), um dir mitzuteilen, ob dein System verbreitete Bibliotheken mit bekannten Sicherheitslücken enthält.
- [nf-core/tools](https://github.com/nf-core/tools)
  Python-Paket mit Hilfswerkzeugen für die nf-core-Gemeinschaft.
- [cansarigol/pdbr](https://github.com/cansarigol/pdbr)
  pdb + Rich-Bibliothek für erweitertes Debugging
- [plant99/felicette](https://github.com/plant99/felicette)
  Satellitenbilder für Dummies.
- [seleniumbase/SeleniumBase](https://github.com/seleniumbase/SeleniumBase)
  Automatisiere & Teste 10x schneller mit Selenium & pytest. Inklusive Batterien.
- [smacke/ffsubsync](https://github.com/smacke/ffsubsync)
  Automatisch Untertitel mit Video synchronisieren.
- [tryolabs/norfair](https://github.com/tryolabs/norfair)
  Leichtgewichtige Python-Bibliothek zum Hinzufügen von 2D-Objektverfolgung in Echtzeit zu jedem Detektor.
- [ansible/ansible-lint](https://github.com/ansible/ansible-lint) Ansible-lint prüft Playbooks auf Praktiken und Verhalten, die möglicherweise verbessert werden könnten
- [ansible-community/molecule](https://github.com/ansible-community/molecule) Ansible Molecule-Testing-Framework
- +[Viele weitere](https://github.com/textualize/rich/network/dependents)!
