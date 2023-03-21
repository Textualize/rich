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

Rich est une bibliothèque Python pour le _rich_ texte et la mise en forme dans le terminal.

L'[API Rich](https://rich.readthedocs.io/en/latest/) permet d'ajouter facilement de la couleur et du style sur le texte du terminal. Rich peut également rendre de jolis tableaux, des barres de progression, du markdown, du code source avec de la coloration syntaxique, des messages d'erreurs et bien d'autres choses encore, et ce dès le départ.

![Features](https://github.com/textualize/rich/raw/master/imgs/features.png)

Pour une introduction vidéo à Rich, voir [camelcode.io](https://calmcode.io/rich/introduction.html) par [@ fishnets88](https://twitter.com/fishnets88)

Voyez ce que [les gens disent de Rich](https://www.willmcgugan.com/blog/pages/post/rich-tweets/)

## Compatibilité

Rich fonctionne avec Linux, OSX et Windows. True color / emoji fonctionne avec le nouveau Terminal Windows, le terminal classique est limité à 16 couleurs. Rich nécessite Python 3.6.3 ou plus.

Rich fonctionne avec les notebooks Jupyter sans configuration supplémentaire.

## Installation

Installez avec `pip` ou votre gestionnaire de paquets PyPI préféré.

```sh
python -m pip install rich
```

Exécutez ce qui suit pour tester la sortie de Rich sur votre terminal :

```sh
python -m rich
```

## Rich Print

Pour ajouter sans effort une sortie Rich à votre application, vous pouvez importer la méthode [rich print](https://rich.readthedocs.io/en/latest/introduction.html#quick-start), qui a la même signature que la fonction Python intégrée. Essayez ceci :

```python
from rich import print

print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())
```

![Hello World](https://github.com/textualize/rich/raw/master/imgs/print.png)

## Rich REPL

Rich peut être installé dans le REPL de Python, de sorte que toutes les structures de données soient joliment affichées et mises en évidence.

```python
>>> from rich import pretty
>>> pretty.install()
```

![REPL](https://github.com/textualize/rich/raw/master/imgs/repl.png)

## Utilisation de Console

Pour mieux contrôler le contenu rich du terminal, importez et construisez une classe [Console](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console)

```python
from rich.console import Console

console = Console()
```

La classe Console possède une méthode `print` dont l'interface est intentionnellement similaire à celle de la fonction `print` native. Voici un exemple d'utilisation :

```python
console.print("Hello", "World!")
```

Comme vous pouvez vous y attendre, cela va afficher "Hello World !" sur le terminal. Notez que, contrairement à la fonction d'affichage intégrée, Rich mettra votre texte en forme pour qu'il tienne dans la largeur du terminal.

Il y a plusieurs façons d'ajouter de la couleur et du style à votre sortie de texte. Vous pouvez définir un style pour l'ensemble de la sortie de texte en ajoutant un argument de mot-clé style. Voici un exemple :

```python
console.print("Hello", "World!", style="bold red")
```

La sortie de texte sera quelque chose comme ce qui suit :

![Hello World](https://github.com/textualize/rich/raw/master/imgs/hello_world.png)

C'est très bien pour styliser une ligne de texte à la fois. Pour un style plus fin, Rich rend un balisage spécial dont la syntaxe est similaire à celle du [bbcode](https://en.wikipedia.org/wiki/BBCode). Voici un exemple :

```python
console.print("Where there is a [bold cyan]Will[/bold cyan] there [u]is[/u] a [i]way[/i].")
```

![Console Markup](https://github.com/textualize/rich/raw/master/imgs/where_there_is_a_will.png)

Vous pouvez utiliser un objet Console pour générer une sortie sophistiquée avec un effort minimal. Consultez la documentation de l'[API Console](https://rich.readthedocs.io/en/latest/console.html) pour plus de détails.

## Rich Inspect

Rich possède une fonction [inspect](https://rich.readthedocs.io/en/latest/reference/init.html?highlight=inspect#rich.inspect) qui peut produire un rapport sur n'importe quel objet Python, comme une classe, une instance ou une fonction intégrée.

```python
>>> my_list = ["foo", "bar"]
>>> from rich import inspect
>>> inspect(my_list, methods=True)
```

![Log](https://github.com/textualize/rich/raw/master/imgs/inspect.png)

Consultez la [documentation d'inspect](https://rich.readthedocs.io/en/latest/reference/init.html#rich.inspect) pour plus de détails.

## Bibliothèque Rich
Rich contient un certain nombre _d'éléments de rendu_ intégrés que vous pouvez utiliser pour créer une sortie élégante dans votre CLI et vous aider à déboguer votre code.

Cliquez sur les rubriques suivantes pour plus de détails :

<details>
<summary>Log</summary>

L'objet Console a une méthode `log()` qui a une interface similaire à `print()`, mais qui rend aussi une colonne pour l'heure actuelle, le fichier et la ligne qui ont fait l'appel. Par défaut, Rich fera la coloration syntaxique des structures Python et des chaînes repr. Si vous enregistrez une collection (i.e. un dict ou une liste) Rich affichera la collection de façon à ce qu'elle tienne dans l'espace disponible. Voici un exemple de certaines de ces fonctionnalités.

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

L'opération ci-dessus produit le résultat suivant :

![Log](https://github.com/textualize/rich/raw/master/imgs/log.png)

Notez l'argument `log_locals`, qui produit un tableau contenant les variables locales où la méthode log a été appelée.

La méthode log peut être utilisée pour la journalisation vers le terminal pour les applications qui tournent longtemps, comme les serveurs, mais c'est aussi une très bonne aide au débogage.
</details>

<details>
<summary>Journalisation</summary>

Vous pouvez également utiliser la classe intégrée [Handler](https://rich.readthedocs.io/en/latest/logging.html) pour formater et coloriser les textes de sortie du module de journalisation de Python. Voici un exemple de texte de sortie :

![Logging](https://github.com/textualize/rich/raw/master/imgs/logging.png)
</details>

<details>
<summary>Emoji</summary>

Pour insérer un emoji dans la sortie de la console, placez le nom entre deux points. Voici un exemple :

```python
>>> console.print(":smiley: :vampire: :pile_of_poo: :thumbs_up: :raccoon:")
😃 🧛 💩 👍 🦝
```

Veuillez utiliser cette fonction à bon escient.
</details>

<details>
<summary>Tableaux</summary>

Rich peut rendre des [tableaux](https://rich.readthedocs.io/en/latest/tables.html) flexibles avec des caractères unicodes. Il existe une grande variété d'options de formatage pour les bordures, les styles, l'alignement des cellules, etc.

![table movie](https://github.com/textualize/rich/raw/master/imgs/table_movie.gif)

L'animation ci-dessus a été générée avec [table_movie.py](https://github.com/textualize/rich/blob/master/examples/table_movie.py) dans le répertoire des exemples.

Voici un exemple de tableau plus simple :

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

Cela produit le résultat suivant :

![table](https://github.com/textualize/rich/raw/master/imgs/table.png)

Notez que les balises de la console sont rendues de la même manière que `print()` et `log()`. De fait, tout ce qui peut être rendu par Rich peut être inclus dans les en-têtes / lignes (même d'autres tables).

La classe `Table` est suffisamment intelligente pour redimensionner les colonnes en fonction de la largeur disponible du terminal, en enveloppant et en réduisant le texte si nécessaire. Voici le même exemple, avec un terminal plus petit que le tableau ci-dessus :

![table2](https://github.com/textualize/rich/raw/master/imgs/table2.png)
</details>

<details>
<summary>Barres de progression</summary>

Rich peut afficher plusieurs [barres de progression](https://rich.readthedocs.io/en/latest/progress.html) sans scintillement pour suivre les tâches de longue périodes.

Pour une utilisation basique, créez une boucle sur n'importe quelle séquence dans la fonction `track` et itérez sur le résultat. Voici un exemple :

```python
from rich.progress import track

for step in track(range(100)):
    do_step(step)
```

Il n'est pas beaucoup plus difficile d'ajouter plusieurs barres de progression. Voici un exemple tiré de la documentation :

![progress](https://github.com/textualize/rich/raw/master/imgs/progress.gif)

Les colonnes peuvent être configurées pour afficher tous les détails que vous souhaitez. Les colonnes intégrées comprennent le pourcentage d'achèvement, la taille du fichier, la vitesse du fichier et le temps restant. Voici un autre exemple montrant un téléchargement en cours :

![progress](https://github.com/textualize/rich/raw/master/imgs/downloader.gif)

Pour l'essayer vous-même, testez [examples/downloader.py](https://github.com/textualize/rich/blob/master/examples/downloader.py) qui peut télécharger plusieurs URL simultanément tout en affichant la progression au fil du temps.

</details>

<details>
<summary>Statut</summary>

Pour les situations où il est difficile de calculer la progression, vous pouvez utiliser la méthode [status](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console.status) qui affichera une animation et un message de type "spinner". L'animation ne vous empêchera pas d'utiliser la console normalement. Voici un exemple :

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

Cela génère la sortie suivante dans le terminal.

![status](https://github.com/textualize/rich/raw/master/imgs/status.gif)

Les animations des characteres d'animations ont été empruntées à [cli-spinners](https://www.npmjs.com/package/cli-spinners). Vous pouvez en sélectionner un en spécifiant le paramètre `spinner`. Exécutez la commande suivante pour voir les valeurs disponibles :

```
python -m rich.spinner
```

La commande ci-dessus génère la sortie suivante dans le terminal :

![spinners](https://github.com/textualize/rich/raw/master/imgs/spinners.gif)
</details>

<details>
<summary>Arborescence</summary>

Rich peut affiché une [arborescence](https://rich.readthedocs.io/en/latest/tree.html) avec des lignes de repère. Une arborescence est idéale pour afficher une structure de fichiers, ou toute autre donnée hiérarchique.

Les étiquettes de cette arborescence peuvent être du texte simple ou tout autre élément que Rich peut rendre. Exécutez ce qui suit pour une démonstration :

```
python -m rich.tree
```

La commande ci-dessus génère la sortie suivante dans le terminal :

![markdown](https://github.com/textualize/rich/raw/master/imgs/tree.png)

Voir l'exemple [tree.py](https://github.com/textualize/rich/blob/master/examples/tree.py) pour un script qui affiche une vue arborescente de n'importe quel répertoire, similaire à la commande linux `tree`.

</details>

<details>
<summary>Colonnes</summary>

Rich peut rendre du contenu en [colonnes](https://rich.readthedocs.io/en/latest/columns.html) avec une largeur égale ou optimale. Voici un clone très basique de la commande `ls` (MacOS / Linux) qui affiche une liste de répertoires en colonnes :

```python
import os
import sys

from rich import print
from rich.columns import Columns

directory = os.listdir(sys.argv[1])
print(Columns(directory))
```

La capture d'écran suivante est le résultat de [columns example](https://github.com/textualize/rich/blob/master/examples/columns.py) qui affiche les données extraites d'une API en colonnes :

![colonne](https://github.com/textualize/rich/raw/master/imgs/columns.png)

</details>

<details>
<summary>Markdown</summary>

Rich peut rendre le [markdown](https://rich.readthedocs.io/en/latest/markdown.html) et fait un travail raisonnable pour traduire le formatage dans le terminal.

Pour rendre du markdown, importez la classe `Markdown` et construisez-la avec une chaîne contenant du code markdown. Ensuite, affichez-la dans la console. Voici un exemple :

```python
from rich.console import Console
from rich.markdown import Markdown

console = Console()
with open("README.md") as readme:
    markdown = Markdown(readme.read())
console.print(markdown)
```

Cela produira un résultat semblable à ce qui suit :

![markdown](https://github.com/textualize/rich/raw/master/imgs/markdown.png)
 
</details>

<details>
<summary>Mise en couleur de la syntaxe</summary>

Rich utilise la bibliothèque [pygments](https://pygments.org/) pour implémenter la [coloration syntaxique](https://rich.readthedocs.io/en/latest/syntax.html). L'utilisation est similaire au rendu de markdown ; construire un objet `Syntax` et afficher celui-ci sur la console. Voici un exemple :

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

Cela produira le résultat suivant :

![syntax](https://github.com/textualize/rich/raw/master/imgs/syntax.png)
</details>

<details>
<summary>Tracebacks</summary>

Rich peut rendre des [traçages d'erreurs](https://rich.readthedocs.io/en/latest/traceback.html) plus faciles à lire et qui montrent plus de code que les traçages d'erreurs standard de Python. Vous pouvez définir Rich comme le gestionnaire d'erreurs par défaut afin que toutes les exceptions/erreurs non capturées soient rendues par Rich.

Voici à quoi cela ressemble sous OSX (similaire sous Linux) :

![traceback](https://github.com/textualize/rich/raw/master/imgs/traceback.png)

</details>

Tous les éléments de rendu utilisent le [Console Protocol](https://rich.readthedocs.io/en/latest/protocol.html), que vous pouvez également utiliser pour mettre en œuvre votre propre contenu Rich.

# Rich pour les entreprises

Disponible dans le cadre de l'abonnement Tidelift.

Les mainteneurs de Rich et de milliers d'autres paquets collaborent avec Tidelift pour fournir un support et une maintenance commerciale pour les paquets open source que vous utilisez pour construire vos applications. Gagnez du temps, réduisez les risques et améliorez votre qualité de code, tout en payant les mainteneurs des paquets que vous utilisez. [En savoir plus](https://tidelift.com/subscription/pkg/pypi-rich?utm_source=pypi-rich&utm_medium=referral&utm_campaign=enterprise&utm_term=repo)

# Projets utilisant Rich

- [BrancoLab/BrainRender](https://github.com/BrancoLab/BrainRender)
  un package python pour la visualisation de données neuro-anatomiques tridimensionnelles
- [Ciphey/Ciphey](https://github.com/Ciphey/Ciphey)
  Outil de déchiffrage automatisé
- [emeryberger/scalene](https://github.com/emeryberger/scalene)
  un profileur de CPU et de mémoire haute performance et haute précision pour Python
- [hedythedev/StarCli](https://github.com/hedythedev/starcli)
  Parcourir les projets tendances de GitHub à partir de votre ligne de commande
- [intel/cve-bin-tool](https://github.com/intel/cve-bin-tool)
  Cet outil recherche un certain nombre de composants courants et vulnérables (openssl, libpng, libxml2, expat et quelques autres) pour vous indiquer si votre système comprend des bibliothèques présentant des vulnérabilités connues.
- [nf-core/tools](https://github.com/nf-core/tools)
  Paquet Python contenant des outils d'aide pour la communauté nf-core.
- [cansarigol/pdbr](https://github.com/cansarigol/pdbr)
  pdb + bibliothèque Rich pour un débogage amélioré
- [plant99/felicette](https://github.com/plant99/felicette)
  L'imagerie satellite pour les nuls.
- [seleniumbase/SeleniumBase](https://github.com/seleniumbase/SeleniumBase)
  Automatisez et testez 10 fois plus vite avec Selenium et pytest. Piles incluses.
- [smacke/ffsubsync](https://github.com/smacke/ffsubsync)
  Synchronisation automatique des sous-titres avec la vidéo.
- [tryolabs/norfair](https://github.com/tryolabs/norfair)
  Bibliothèque Python légère pour ajouter le suivi d'objets 2D en temps réel à n'importe quel détecteur.
- [ansible/ansible-lint](https://github.com/ansible/ansible-lint) Ansible-lint vérifie dans les playbooks les pratiques et comportements qui pourraient être améliorés.
- [ansible-community/molecule](https://github.com/ansible-community/molecule) Cadre de test Ansible Molecule.
- [Beaucoup d'autres](https://github.com/textualize/rich/network/dependents) !
