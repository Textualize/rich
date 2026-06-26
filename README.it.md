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


Rich è una libreria Python per un testo _rich_ e con una piacevole formattazione nel terminale.

Le [Rich API](https://rich.readthedocs.io/en/latest/) permettono di aggiungere facilmente colore e stile all'output del terminale. Rich permette di visualizzare tabelle, barre di avanzamento, markdown, evidenziazione della sintassi, tracebacks, e molto altro ancora — tutto già pronto all'uso.

![Features](https://github.com/textualize/rich/raw/main/imgs/features.png)

Per una video-introduzione di Rich puoi vedere [calmcode.io](https://calmcode.io/rich/introduction.html) by [@fishnets88](https://twitter.com/fishnets88).

Guarda cosa [le persone dicono su Rich](https://www.willmcgugan.com/blog/pages/post/rich-tweets/).

## Compatibilità

Rich funziona su Linux, OSX, e Windows. True color / emoji funzionano con il nuovo Windows Terminal, il terminale classico è limitato a 16 colori. Rich richiede Python 3.6.3 o superiore.

Rich funziona con i [Jupyter notebooks](https://jupyter.org/) senza configurazioni aggiuntive.

## Installazione

Installa con `pip` o il tuo PyPI package manager preferito.

```sh
python -m pip install rich
```

Esegui il seguente comando per testare l'output di Rich sul tuo terminale:

```sh
python -m rich
```

## Rich Print

Utilizzare rich è semplicissimo, ti basta importare il metodo [rich print](https://rich.readthedocs.io/en/latest/introduction.html#quick-start), che ha la stessa signature della funzione builtin in Python. Prova:

```python
from rich import print

print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())
```

![Hello World](https://github.com/textualize/rich/raw/main/imgs/print.png)

## Rich REPL

Rich può essere installo in Python REPL, in questo modo ogni struttura dati sarà visualizzata in modo gradevole ed evidenziato.

```python
>>> from rich import pretty
>>> pretty.install()
```

![REPL](https://github.com/textualize/rich/raw/main/imgs/repl.png)

## Utilizzo di Console

Per un maggiore personalizzazione dei contenuti puoi importare ed instanziare un oggetto [Console](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console).

```python
from rich.console import Console

console = Console()
```

L'oggetto Console ha il metodo `print` che utilizza volutamente un interfaccia simile a quella del `print` originale. Ad esempio:

```python
console.print("Hello", "World!")
```

Come puoi immaginare, questo stamperà `"Hello World!"` sul terminale. Nota che diversamente dalla funzione builtin `print`, Rich potrebbe portare a capo il testo per rispettare le dimensioni del terminale.

Ci sono diversi modi di aggiungere stile e colore al tuo output. Puoi impostare uno stile per l'intero output utilizzando l'argomento keyword `style`. Ad esempio:

```python
console.print("Hello", "World!", style="bold red")
```

L'output sarà qualcosa tipo:

![Hello World](https://github.com/textualize/rich/raw/main/imgs/hello_world.png)

Questo va bene per applicare uno stile ad una linea di testo alla volta. Per uno stile più ricercato, puoi utilizzare uno speciale linguaggio di markup che è simile nella sintassi a [bbcode](https://en.wikipedia.org/wiki/BBCode). Ad esempio:

```python
console.print("Where there is a [bold cyan]Will[/bold cyan] there [u]is[/u] a [i]way[/i].")
```

![Console Markup](https://github.com/textualize/rich/raw/main/imgs/where_there_is_a_will.png)

Puoi utilizzare l'oggetto Console per generare output sofisticati con il minimo sforzo. Vedi la docs di [Console API](https://rich.readthedocs.io/en/latest/console.html) per ulteriori dettagli.

## Rich Inspect

Rich ha una funzione [inspect](https://rich.readthedocs.io/en/latest/reference/init.html?highlight=inspect#rich.inspect) che può produrre un report per un qualsiasi oggetto Python, come una classe, un instanza, o un builtin.

```python
>>> my_list = ["foo", "bar"]
>>> from rich import inspect
>>> inspect(my_list, methods=True)
```

![Log](https://github.com/textualize/rich/raw/main/imgs/inspect.png)

Vedi [inspect docs](https://rich.readthedocs.io/en/latest/reference/init.html#rich.inspect) per ulteriori dettagli.

# Rich Library

Rich contiene alcuni builtin _renderables_ che puoi utilizzare per creare eleganti output nella tua CLI e aiutarti nel debug del tuo codice.

Fai click sulle seguenti intestazioni per ulteriori dettagli:

<details>
<summary>Log</summary>

L'oggetto Console ha un metodo `log()` che utilizza un'interfaccia simile a `print()`, ma visualizza anche una colonna con l'ora corrente, il file e la linea che hanno generato la chiamata. Di default Rich evidenzierà le strutture Python e le stringhe repr. Se logghi un oggetto di tipo collection (e.s. un dict o una lista) Rich automaticamente abbellirà l'output in modo che possa entrare nello spazio disponibile. Ecco qui un esempio di alcune delle feature discusse:

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

Il codice appena mostrato produce il seguente output:

![Log](https://github.com/textualize/rich/raw/main/imgs/log.png)

Nota l'argomento `log_locals`, che visualizza una tabella contenente le variabili locali dove il metodo log è stato chiamato.

Il metodo log può essere usato per il logging su terminale di applicazioni che solitamente girano su server, ma ha anche uno scopo orientato al debugging.

</details>
<details>
<summary>Logging Handler</summary>

Puoi anche utilizzare la classe builtin [Handler](https://rich.readthedocs.io/en/latest/logging.html) per formattare e colorare l'output dal modulo logging di Python. Ecco un esempio dell'output:

![Logging](https://github.com/textualize/rich/raw/main/imgs/logging.png)

</details>

<details>
<summary>Emoji</summary>

Per inserire un emoji nell'output della console inseriscine il nome in mezzo a due ':'. Ad esempio:

```python
>>> console.print(":smiley: :vampire: :pile_of_poo: :thumbs_up: :raccoon:")
😃 🧛 💩 👍 🦝
```

Usa questa feature saggiamente.

</details>

<details>
<summary>Tables</summary>

Rich può visualizzare [tabelle](https://rich.readthedocs.io/en/latest/tables.html) flessibili con caratteri unicode. C'è una vasta gamma di opzioni per la formattazione di bordi, stili, allineamenti di celle etc.

![table movie](https://github.com/textualize/rich/raw/main/imgs/table_movie.gif)

Questa animazione è stata realizzata con [table_movie.py](https://github.com/textualize/rich/blob/main/examples/table_movie.py) presente nella directory examples.

Ecco qui un semplice esempio di tabella:

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

Questo produce il seguente output:

![table](https://github.com/textualize/rich/raw/main/imgs/table.png)

Nota che il console markup è visualizzato nello stesso modo di `print()` e `log()`. Infatti, tutto ciò che è visualizzabile da Rich può essere incluso nelle intestazioni / righe (anche altre tabelle).

La classe `Table` è abbastanza smart da ridimensionare le colonne per entrare nello spazio residuo del terminale, wrappando il testo come richiesto. Ad esempio, con il terminale reso più piccolo della tabella sopra:

![table2](https://github.com/textualize/rich/raw/main/imgs/table2.png)

</details>

<details>
<summary>Barre di avanzamento</summary>

Rich può visualizzare, senza sfarfallio, multiple barre [di avanzamento](https://rich.readthedocs.io/en/latest/progress.html) per tenere traccia di task di lunga durata.

Per un utilizzo base, wrappa ogni 'step' con la funzione `track` e itera sul risultato. Ad esempio:

```python
from rich.progress import track

for step in track(range(100)):
    do_step(step)
```

Non è difficile aggiungere barre di avanzamento multiple. Ecco un esempio dalla documentazione:

![progress](https://github.com/textualize/rich/raw/main/imgs/progress.gif)

Le colonne possono essere configurate per visualizzare qualsiasi dettaglio tu voglia. Le colonne built-in includono percentuale di completamente, dimensione del file, velocità, e tempo rimasto. Ecco un altro esempio che mostra un download in corso:

![progress](https://github.com/textualize/rich/raw/main/imgs/downloader.gif)

Per testare tu stesso, vedi [examples/downloader.py](https://github.com/textualize/rich/blob/main/examples/downloader.py) che può scaricare multipli URL simultaneamente mentre mostra lo stato di avanzamento.

</details>

<details>
<summary>Status</summary>

Per situazioni in cui è difficile calcolare l'avanzamento, puoi utilizzare il metodo [status](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console.status) che mostrerà un animazione 'spinner' e un messaggio. L'animazione non ti impedisce di utilizzare la console normalmente. Ad esempio:

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

Questo produrrà il seguente output nel terminale.

![status](https://github.com/textualize/rich/raw/main/imgs/status.gif)

L'animazione dello spinner è ispirata da [cli-spinners](https://www.npmjs.com/package/cli-spinners). Puoi selezionarne uno specificando `spinner` tra i parametri. Esegui il seguente comando per visualizzare le possibili opzioni:

```shell
python -m rich.spinner
```

Questo produrrà il seguente output nel terminale.

![spinners](https://github.com/textualize/rich/raw/main/imgs/spinners.gif)

</details>

<details>
<summary>Albero</summary>

Rich può visualizzare un [albero](https://rich.readthedocs.io/en/latest/tree.html) con linee guida. Un albero è ideale per mostrare la struttura di un file, o altri dati gerarchici.

Le etichette dell'albero possono essere semplice testo o qualsiasi altra cosa che Rich può visualizzare. Esegui il seguente comando per una dimostrazione:

```shell
python -m rich.tree
```

Questo produrrà il seguente output:

![markdown](https://github.com/textualize/rich/raw/main/imgs/tree.png)

Vedi l'esempio [tree.py](https://github.com/textualize/rich/blob/main/examples/tree.py) per uno script che mostra una vista ad albero di ogni directory, simile a quella del comando linux `tree`.

</details>

<details>
<summary>Colonne</summary>

Rich può visualizzare contenuti in [colonne](https://rich.readthedocs.io/en/latest/columns.html) ordinate con larghezza uguale o ottimale. Ecco qui un clone base del comando (MacOS / Linux) `ls` che mostra il contenuto di una directory in colonna:

```python
import os
import sys

from rich import print
from rich.columns import Columns

directory = os.listdir(sys.argv[1])
print(Columns(directory))
```

Il seguente screenshot è l'output dell'[esempio di columns](https://github.com/textualize/rich/blob/main/examples/columns.py) che visualizza i dati ottenuti da un API in colonna:

![columns](https://github.com/textualize/rich/raw/main/imgs/columns.png)

</details>

<details>
<summary>Markdown</summary>

Rich può visualizzare [markdown](https://rich.readthedocs.io/en/latest/markdown.html) e tradurlo in modo da visualizzarlo su terminale.

Per visualizzare markdown importa la classe `Markdown` e instanziala con una stringa contenente codice markdown. Dopo stampala sulla console. Ad esempio:

```python
from rich.console import Console
from rich.markdown import Markdown

console = Console()
with open("README.md") as readme:
    markdown = Markdown(readme.read())
console.print(markdown)
```

Questo produrrà un output simile al seguente:

![markdown](https://github.com/textualize/rich/raw/main/imgs/markdown.png)

</details>

<details>
<summary>Evidenziazione della sintassi</summary>

Rich utilizza la libreria [pygments](https://pygments.org/) per implementare il [syntax highlighting](https://rich.readthedocs.io/en/latest/syntax.html). L'utilizzo è simile a quello per visualizzare markdown; instanzia un oggetto `Syntax` e stampalo sulla console. Ad esempio:

```python
from rich.console import Console
from rich.syntax import Syntax

my_code = '''
def iter_first_last(values: Iterable[T]) -> Iterable[Tuple[bool, bool, T]]:
    """Itera e genera una tupla con un flag per il primo e ultimo valore."""
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

Questo produrrà il seguente output:

![syntax](https://github.com/textualize/rich/raw/main/imgs/syntax.png)

</details>

<details>
<summary>Tracebacks</summary>

Rich può visualizzare [gradevoli tracebacks](https://rich.readthedocs.io/en/latest/traceback.html) che sono più semplici da leggere e che mostrano più codice rispetto ai Python tracebacks. Puoi impostare Rich come il traceback handler di default, in questo modo tutte le eccezioni non gestiti saranno visualizzate da Rich.

Ecco come appare su OSX (simile a Linux):

![traceback](https://github.com/textualize/rich/raw/main/imgs/traceback.png)

</details>

Tutti i Rich renderables utilizzano [Console Protocol](https://rich.readthedocs.io/en/latest/protocol.html), che puoi utilizzare per implementare nuovi contenuti su Rich.

# Rich per le aziende

Disponibile come parte dell'iscrizione a Tidelift.

Lo sviluppatore di Rich e migliaia di altri packages lavorano con Tidelift per garantire supporto commerciale e mantenimento per i pacchetti open source che utilizzi per costruire le tue applicazioni. Risparmia tempo, riduci i rischi, e migliora la vita del codice, pagando i mantenitori dello stesso package che utilizzi. [Ulteriori informazioni.](https://tidelift.com/subscription/pkg/pypi-rich?utm_source=pypi-rich&utm_medium=referral&utm_campaign=enterprise&utm_term=repo)

# Progetti che usano Rich

Ecco alcuni progetti che utilizzano Rich:

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
