[![Supported Python Versions](https://img.shields.io/pypi/pyversions/rich)](https://pypi.org/project/rich/) [![PyPI version](https://badge.fury.io/py/rich.svg)](https://badge.fury.io/py/rich)

[![Downloads](https://pepy.tech/badge/rich/month)](https://pepy.tech/project/rich)
[![codecov](https://img.shields.io/codecov/c/github/Textualize/rich?label=codecov&logo=codecov)](https://codecov.io/gh/Textualize/rich)
[![Rich blog](https://img.shields.io/badge/blog-rich%20news-yellowgreen)](https://www.willmcgugan.com/tag/rich/)
[![Twitter Follow](https://img.shields.io/twitter/follow/willmcgugan.svg?style=social)](https://twitter.com/willmcgugan)

![Logo](https://github.com/textualize/rich/raw/main/imgs/logo.svg)

[English readme](https://github.com/textualize/rich/blob/main/README.md)
 • [简体中文 readme](https://github.com/textualize/rich/blob/main/README.cn.md)
 • [正體中文 readme](https://github.com/textualize/rich/blob/main/README.zh-tw.md)
 • [Español readme](https://github.com/textualize/rich/blob/main/README.es.md)
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

Rich es un paquete de Python para texto _enriquecido_ y un hermoso formato en la terminal.

La [API Rich](https://rich.readthedocs.io/en/latest/) facilita la adición de color y estilo a la salida del terminal. Rich también puede representar tablas bonitas, barras de progreso, markdown, código fuente resaltado por sintaxis, trazas y más — listo para usar.

![Funciones](https://github.com/textualize/rich/raw/main/imgs/features.png)

Para ver un vídeo de introducción a Rich, consulte [calmcode.io](https://calmcode.io/rich/introduction.html) de [@fishnets88](https://twitter.com/fishnets88).

Vea lo que [la gente dice sobre Rich](https://www.willmcgugan.com/blog/pages/post/rich-tweets/).

## Compatibilidad

Rich funciona con Linux, macOS y Windows. True color / emoji funciona con la nueva Terminal de Windows; la terminal clásica está limitada a 16 colores. Rich requiere Python 3.8 o posterior.

Rich funciona con [Jupyter notebooks](https://jupyter.org/) sin necesidad de configuración adicional.

## Instalación

Instale con `pip` o su administrador de paquetes PyPI favorito.

```sh
python -m pip install rich
```

Ejecute lo siguiente para probar la salida de Rich sobre su terminal:

```sh
python -m rich
```

## Función print de Rich

Para agregar sin esfuerzo resultados enriquecidos a su aplicación, puede importar el método [rich print](https://rich.readthedocs.io/en/latest/introduction.html#quick-start), que tiene la misma firma que el método incorporado de Python. Prueba esto:

```python
from rich import print

print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())
```

![Hello World](https://github.com/textualize/rich/raw/main/imgs/print.png)

## Rich REPL

Rich se puede instalar en Python REPL, por lo que cualquier estructura de datos se imprimirá y resaltará bastante.

```python
>>> from rich import pretty
>>> pretty.install()
```

![REPL](https://github.com/textualize/rich/raw/main/imgs/repl.png)

## Usando la consola

Para tener más control sobre el contenido enriquecido del terminal, importe y cree un objeto [Console](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console).

```python
from rich.console import Console

console = Console()
```

El objeto Console tiene un método `print` que tiene una interfaz intencionalmente similar a la función incorporada `print`. Aquí tienes un ejemplo de uso:

```python
console.print("Hello", "World!")
```

Como era de esperar, esto imprimirá `"Hello World!"` en la terminal. Tenga en cuenta que, a diferencia de la función `print` incorporada, Rich ajustará su texto para ajustarlo al ancho de la terminal.

Hay algunas formas de agregar color y estilo a su salida. Puede establecer un estilo para toda la salida agregando un argumento de palabra clave `style`. He aquí un ejemplo:

```python
console.print("Hello", "World!", style="bold red")
```

La salida será similar a la siguiente:

![Hello World](https://github.com/textualize/rich/raw/main/imgs/hello_world.png)

Eso está bien para diseñar una línea de texto a la vez. Para un estilo más fino, Rich presenta un marcado especial que es similar en sintaxis a [bbcode](https://en.wikipedia.org/wiki/BBCode). He aquí un ejemplo:

```python
console.print("Where there is a [bold cyan]Will[/bold cyan] there [u]is[/u] a [i]way[/i].")
```

![Console Markup](https://github.com/textualize/rich/raw/main/imgs/where_there_is_a_will.png)

Usted puede usar el objeto Console para generar salida sofisticada con mínimo esfuerzo. Ver la documentación [API Console](https://rich.readthedocs.io/en/latest/console.html) para detalles.

## Rich Inspector

Rich tiene ua función [inspeccionar](https://rich.readthedocs.io/en/latest/reference/init.html?highlight=inspect#rich.inspect) cual puede producir un reporte sobre cualquier objeto Python, como clases, instancia o builtin.

```python
>>> my_list = ["foo", "bar"]
>>> from rich import inspect
>>> inspect(my_list, methods=True)
```

![Log](https://github.com/textualize/rich/raw/main/imgs/inspect.png)

Ver la [documentación inspector](https://rich.readthedocs.io/en/latest/reference/init.html#rich.inspect) para detalles.

# Paquete Rich

Rich contiene un número de builtin _renderables_ que puedes usar para crear salida elegante en su CLI y ayudarle a depurar su código.

Haga clic en los siguientes títulos para obtener más detalles:

<details>
<summary>Registro de consola</summary>

El objeto Console tiene un método `log()` que tiene una interfaz similar a `print()`, pero también muestra una columna para la hora actual y el archivo y la línea que realizó la llamada. De forma predeterminada, Rich resaltará la sintaxis de las estructuras de Python y de las cadenas de reproducción. Si registra una colección (es decir, un diccionario o una lista), Rich la imprimirá de forma bonita para que quepa en el espacio disponible. A continuación, se muestra un ejemplo de algunas de estas funciones.

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

Lo anterior produce el siguiente resultado:

![Registro](https://github.com/textualize/rich/raw/main/imgs/log.png)

Tenga en cuenta el argumento `log_locals`, que genera una tabla que contiene las variables locales donde se llamó al método log.

El método de registro podría usarse para iniciar sesión en el terminal para aplicaciones de larga ejecución, como servidores, pero también es una ayuda de depuración muy buena.

</details>
<details>
<summary>Controlador de registro</summary>

También puede usar la [Handler class](https://rich.readthedocs.io/en/latest/logging.html) incorporada  para formatear y colorear la salida del módulo de registro de Python. Aquí hay un ejemplo de la salida:

![Registro](https://github.com/textualize/rich/raw/main/imgs/logging.png)
</details>

<details>
<summary>Emoji</summary>

Para insertar un emoji en la salida de la consola, coloque el nombre entre dos puntos. He aquí un ejemplo:

```python
>>> console.print(":smiley: :vampire: :pile_of_poo: :thumbs_up: :raccoon:")
😃 🧛 💩 👍 🦝
```

Utilice esta función con prudencia.
</details>

<details>
<summary>Tablas</summary>

Rich puede renderizar [tablas](https://rich.readthedocs.io/en/latest/tables.html) flexibles con caracteres de cuadro Unicode. Existe una gran variedad de opciones de formato para bordes, estilos, alineación de celdas, etc.

![table movie](https://github.com/textualize/rich/raw/main/imgs/table_movie.gif)

La animación anterior se generó con [table_movie.py](https://github.com/textualize/rich/blob/main/examples/table_movie.py) en el directorio de ejemplos.

Aquí hay un ejemplo de tabla más simple:

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

Esto produce la siguiente salida:

![table](https://github.com/textualize/rich/raw/main/imgs/table.png)

Tenga en cuenta que el marcado de la consola se representa de la misma manera que `print()` y `log()`. De hecho, cualquier cosa que Rich pueda representar se puede incluir en los encabezados / filas (incluso en otras tablas).

La clase `Table` es lo suficientemente inteligente como para cambiar el tamaño de las columnas para que se ajusten al ancho disponible de la terminal, ajustando el texto según sea necesario. Este es el mismo ejemplo, con la terminal más pequeña que la tabla anterior:

![table2](https://github.com/textualize/rich/raw/main/imgs/table2.png)

</details>

<details>
<summary>Barras de progreso</summary>

Rich puede representar varias barras de [progreso](https://rich.readthedocs.io/en/latest/progress.html) sin parpadeos para realizar un seguimiento de las tareas de larga duración.

Para un uso básico, envuelva cualquier secuencia en la función `track` e itere sobre el resultado. He aquí un ejemplo:

```python
from rich.progress import track

for step in track(range(100)):
    do_step(step)
```

No es mucho más difícil agregar varias barras de progreso. Aquí hay un ejemplo tomado de la documentación:

![progress](https://github.com/textualize/rich/raw/main/imgs/progress.gif)

Las columnas pueden configurarse para mostrar los detalles que desee. Las columnas integradas incluyen porcentaje completado, tamaño de archivo, velocidad de archivo y tiempo restante. Aquí hay otro ejemplo que muestra una descarga en progreso:

![progress](https://github.com/textualize/rich/raw/main/imgs/downloader.gif)

Para probar esto usted mismo, consulte [examples/downloader.py](https://github.com/textualize/rich/blob/main/examples/downloader.py) que puede descargar varias URL simultáneamente mientras muestra el progreso.

</details>

<details>
<summary>Estado</summary>

Para situaciones en las que es difícil calcular el progreso, puede utilizar el método [status](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console.status) que mostrará una animación y un mensaje de "spinner". La animación no le impedirá usar la consola con normalidad. He aquí un ejemplo:

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

Esto genera la siguiente salida en el terminal.

![status](https://github.com/textualize/rich/raw/main/imgs/status.gif)

Las animaciones de spinner fueron tomadas de [cli-spinners](https://www.npmjs.com/package/cli-spinners). Puede seleccionar un spinner especificando el `spinner` parameter. Ejecute el siguiente comando para ver los valores disponibles:

```
python -m rich.spinner
```

El comando anterior genera la siguiente salida en la terminal:

![spinners](https://github.com/textualize/rich/raw/main/imgs/spinners.gif)

</details>

<details>
<summary>Árbol</summary>

Rich genera un [tree](https://rich.readthedocs.io/en/latest/tree.html) con líneas de guía. Un árbol es ideal para mostrar una estructura de archivos, o cualquier otro dato jerárquico.

Las etiquetas del árbol pueden ser texto simple o cualquier otra cosa que Rich pueda mostar. Ejecuta lo siguiente para una demostración:

```
python -m rich.tree
```

Esto genera la siguiente salida:

![markdown](https://github.com/textualize/rich/raw/main/imgs/tree.png)

Ver el ejemplo [tree.py](https://github.com/textualize/rich/blob/main/examples/tree.py) para un script que muestra una vista de  árbol de cualquier directorio, similar a el comando de linux `tree`.

</details>

<details>
<summary>Columnas</summary>

Rich puede representar contenido en [columnas](https://rich.readthedocs.io/en/latest/columns.html) ordenadas con un ancho igual u óptimo. Aquí hay un clon muy básico del comando (MacOS / Linux) `ls` que muestra una lista de directorios en columnas:

```python
import os
import sys

from rich import print
from rich.columns import Columns

directory = os.listdir(sys.argv[1])
print(Columns(directory))
```

La siguiente captura de pantalla es el resultado del [ejemplo de columnas](https://github.com/textualize/rich/blob/main/examples/columns.py) que muestra los datos extraídos de una API en columnas:

![columns](https://github.com/textualize/rich/raw/main/imgs/columns.png)

</details>

<details>
<summary>Markdown</summary>

Rich puede renderizar [markdown](https://rich.readthedocs.io/en/latest/markdown.html) y hace un trabajo razonable al traducir el formato al terminal.

Para renderizar markdown, importe la clase `Markdown` y constrúyala con una cadena que contenga el código de markdown. Luego imprímalo en la consola. He aquí un ejemplo:

```python
from rich.console import Console
from rich.markdown import Markdown

console = Console()
with open("README.md") as readme:
    markdown = Markdown(readme.read())
console.print(markdown)
```

Esto producirá una salida similar a la siguiente:

![markdown](https://github.com/textualize/rich/raw/main/imgs/markdown.png)

</details>

<details>
<summary>Resaltado de sintaxis</summary>

Rich usa el paquete [pygments](https://pygments.org/) para implementar [resaltado de sintaxis](https://rich.readthedocs.io/en/latest/syntax.html). El uso es similar a renderizar markdown; construya un objeto `Syntax` e imprímalo en la consola. He aquí un ejemplo:

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

Esto producirá el siguiente resultado:

![syntax](https://github.com/textualize/rich/raw/main/imgs/syntax.png)

</details>

<details>
<summary>Tracebacks</summary>

Rich puede representar [tracebacks hermosos](https://rich.readthedocs.io/en/latest/traceback.html) que son más fáciles de leer y muestran más código que los tracebacks estándar de Python. Puede configurar Rich como el controlador tracebacks predeterminado para que todas las excepciones sin capturar sean procesadas por Rich.

Así es como se ve en OSX (similar en Linux):

![traceback](https://github.com/textualize/rich/raw/main/imgs/traceback.png)

</details>

Todos los renderizables enriquecidos utilizan el [Console Protocol](https://rich.readthedocs.io/en/latest/protocol.html), que también puede utilizar para implementar su propio contenido Rich.

# Rich para empresas

Disponible como parte de la suscripción a Tidelift.

Los mantenedores de Rich y miles de otros paquetes están trabajando con Tidelift para brindar soporte comercial y mantenimiento para los paquetes de código abierto que usa para construir sus aplicaciones. Ahorre tiempo, reduzca el riesgo y mejore el estado del código, mientras paga a los mantenedores de los paquetes exactos que utiliza. [Más información](https://tidelift.com/subscription/pkg/pypi-rich?utm_source=pypi-rich&utm_medium=referral&utm_campaign=enterprise&utm_term=repo)

# Proyecto usando Rich

Aquí hay algunos proyectos que usan Rich:

- [BrancoLab/BrainRender](https://github.com/BrancoLab/BrainRender)
  un paquete de Python para la visualización de datos neuroanatómicos tridimensionales
- [Ciphey/Ciphey](https://github.com/Ciphey/Ciphey)
  Herramienta de descifrado automatizado
- [emeryberger/scalene](https://github.com/emeryberger/scalene)
  un perfilador de memoria y CPU de alta precisión y alto rendimiento para Python
- [hedythedev/StarCli](https://github.com/hedythedev/starcli)
  Explore los proyectos de tendencias de GitHub desde su línea de comando
- [intel/cve-bin-tool](https://github.com/intel/cve-bin-tool)
  Esta herramienta busca una serie de componentes vulnerables comunes (openssl, libpng, libxml2, expat y algunos otros) para informarle si su sistema incluye bibliotecas comunes con vulnerabilidades conocidas.
- [nf-core/tools](https://github.com/nf)
  Paquete de Python con herramientas auxiliares para la comunidad nf-core.
- [cansarigol/pdbr](https://github.com/cansarigol/pdbr)
  pdb + biblioteca Rich para una depuración mejorada
- [plant99/felicette](https://github.com/plant99/felicette)
  Imágenes de satélite para tontos.
- [seleniumbase/SeleniumBase](https://github.com/seleniumbase/SeleniumBase)
  Automatice y pruebe 10 veces más rápido con Selenium y pytest. Baterias incluidas.
- [smacke/ffsubsync](https://github.com/smacke/ffsubsync)
  Sincronice automáticamente los subtítulos con el video.
- [tryolabs/norfair](https://github.com/tryolabs/norfair)
  Libreria de Python para agregar tracking a cualquier detector.
- [ansible/ansible-lint](https://github.com/ansible/ansible-lint) Ansible-lint comprueba los playbooks en busca de prácticas y comportamientos que podrían mejorarse
- [ansible-community/molecule](https://github.com/ansible-community/molecule) Marco de prueba de Ansible Molecule
- +¡[Muchos más](https://github.com/textualize/rich/network/dependents)!
