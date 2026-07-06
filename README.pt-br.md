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
 • [Русский readme](https://github.com/textualize/rich/blob/main/README.ru.md)
  • [فارسی readme](https://github.com/textualize/rich/blob/main/README.fa.md)
 • [Türkçe readme](https://github.com/textualize/rich/blob/main/README.tr.md)
 • [Polskie readme](https://github.com/textualize/rich/blob/main/README.pl.md)

Rich é uma biblioteca Python para _rich_ text e formatação de estilos no terminal.

A [API do Rich](https://rich.readthedocs.io/en/latest/) permite adicionar cores e estilos no output do terminal de forma fácil. Rich também permite formataçao de tabelas, barra de progresso, markdown, highlight de sintaxe de código fonte, rastreio de erros (traceback) e muito mais.

![Funcões](https://github.com/textualize/rich/raw/main/imgs/features.png)

Para mais detalhes, veja um vídeo de introdução so Rich em [calmcode.io](https://calmcode.io/rich/introduction.html) por [@fishnets88](https://twitter.com/fishnets88).

Veja aqui [o que estão falando sobre o Rich](https://www.willmcgugan.com/blog/pages/post/rich-tweets/).

## Compatibilidade

Rich funciona no Linux, OSX e Windows. True color / emoji funciona no novo Terminal do Windows, o terminal classico é limitado a 16 cores. Rich requer Python 3.6.3 ou superior.

Rich funciona com [Jupyter notebooks](https://jupyter.org/) sem a necessidade de configurações adicionais.

## Instalação

Instale usando `pip` ou seu gerenciador de pacotes PyPI favorito.

```sh
python -m pip install rich
```

Execute o seguinte comando para testar o output do Rich no seu terminal:

```sh
python -m rich
```

## Print do Rich

Para adicionar as as funções de formatação do rich na sua aplicação de forma fácil, simplesmente importe o metodo [rich print](https://rich.readthedocs.io/en/latest/introduction.html#quick-start) que tem a mesma assinatura da função nativa do Python. Por exemplo:

```python
from rich import print

print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())
```

![Hello World](https://github.com/textualize/rich/raw/main/imgs/print.png)

## REPL do Rich

O Rich pode ser instalado no REPL do Python fazendo com que qualquer estrutura de dados seja exibida formatada e com highlights.

```python
>>> from rich import pretty
>>> pretty.install()
```

![REPL](https://github.com/textualize/rich/raw/main/imgs/repl.png)

## Usando o Console

Para ter mais controle sobre a formatação do conteudo no terminal, importe e instancie um objeto do [Console](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console).

```python
from rich.console import Console

console = Console()
```

Objetos do tipo Console tem um metodo `print` que tem a interface intencionalmente similar à função `print` nativa. Veja a seguir um exeplo de uso:

```python
console.print("Hello", "World!")
```

Como esperado, este comando vai imprimir `"Hello World!"` no terminal. Porém, observe que, diferente da função `print` nativa, o Rich vai quebrar a linha entre palavras (word-wrap) no seu texto para caber na largura do terminal.

Existem algumas formas de adicionar cores e estilos nos outputs. É possivel aplicar um estilo para todo output adicionando o argumento nomeado `style`. Por exemplo:

```python
console.print("Hello", "World!", style="bold red")
```

O resultado vai ser algo como:

![Hello World](https://github.com/textualize/rich/raw/main/imgs/hello_world.png)

Isso funciona bem para formatar cada linha do texto individualmente. Para maior controle sobre a formatação, o Rich renderiza um markup especial com uma sintaxe similar ao [bbcode](https://en.wikipedia.org/wiki/BBCode). Veja o exemplo a seguir:

```python
console.print("Where there is a [bold cyan]Will[/bold cyan] there [u]is[/u] a [i]way[/i].")
```

![Console Markup](https://github.com/textualize/rich/raw/main/imgs/where_there_is_a_will.png)

Voce pode usar o objeto do Console para gerar facilmente uma saída para o terminal sofisticada. Veja a documentação da [API do Console](https://rich.readthedocs.io/en/latest/console.html) para mais detalhes.

## Inspect do Rich

O Rich tem uma função [inspect](https://rich.readthedocs.io/en/latest/reference/init.html?highlight=inspect#rich.inspect) que gera um relatório de qualquer objeto no Python, como classes, instâncias ou funções nativas.

```python
>>> my_list = ["foo", "bar"]
>>> from rich import inspect
>>> inspect(my_list, methods=True)
```

![Log](https://github.com/textualize/rich/raw/main/imgs/inspect.png)

Confira a [documentação do inspect](https://rich.readthedocs.io/en/latest/reference/init.html#rich.inspect) para mais detalhes.

# A biblioteca Rich

O Rich possui vários _renderizáveis_ nativos que podem ser usados para criar outputs elegantes no seu CLI e ajudar a debugar o código.

Clique nos itens a seguir para expandir os detalhes:

<details>
<summary>Log</summary>

O objeto Console tem um método `log()` com uma interface similar ao `print()` mas que também imprime uma coluna com a hora atual, nome do arquivo e linha onde foi executado. Por padrão, o Rich vai fazer highlight de sintaxe para extruturas do Python e para repr strings. Se você usar o `log()` para imprimir uma _collection_ (por exemplo um dicionário ou uma lista), o Rich vai imprimir formatado de uma forma que caiba no espaço disponível. Veja a seguir alguns exemplos dessas funções:

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

O código acima vai produzir algo parecido com:

![Log](https://github.com/textualize/rich/raw/main/imgs/log.png)

Note o argumento `log_locals` que imprime uma tabela com as variáveis locais no contexto em que o método `log()` foi chamado.

O método `log()` pode ser usado para logar no terminal em aplicações de processos longos como servidores, mas é também uma ferramenta ótima para debugar.

</details>
<details>
<summary>Logging Handler</summary>

Você também pode usar a [classe Handler](https://rich.readthedocs.io/en/latest/logging.html) nativa para formatar e colorir o output do módulo `logging` do Python. Veja aqui um exemplo do output:

![Logging](https://github.com/textualize/rich/raw/main/imgs/logging.png)

</details>

<details>
<summary>Emoji</summary>

Para imprimir um emoji no console, coloque o nome do emoji entre dois ":" (dois pontos). Por exemplo:

```python
>>> console.print(":smiley: :vampire: :pile_of_poo: :thumbs_up: :raccoon:")
😃 🧛 💩 👍 🦝
```

Por favor use esse recurso com sabedoria.

</details>

<details>
<summary>Tabelas</summary>

O Rich pode imprimir [tables](https://rich.readthedocs.io/en/latest/tables.html) flexíveis usando caracteres unicode como bordas. Existem várias opções de formatação de bordas, estilos, alinhamento das celulas, etc.

![table movie](https://github.com/textualize/rich/raw/main/imgs/table_movie.gif)

A animação acima foi gerada com o arquivo [table_movie.py](https://github.com/textualize/rich/blob/main/examples/table_movie.py) da pasta de exemplos.

Veja um exemplo mais simples:

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

Que gera o seguinte resultado:

![table](https://github.com/textualize/rich/raw/main/imgs/table.png)

Observe que o markup é renderizado da mesma que em `print()` e `log()`. Na verdade, tudo que é renderizável pelo Rich pode ser incluído nos cabeçalhos ou linhas (até mesmo outras tabelas).

A classe `Table` é inteligente o suficiente para ajustar o tamanho das colunas para caber na largura do terminal, quebrando o texto em novas linhas quando necessário. Veja o mesmo exemplo a seguir, só que desta vez com um terminal menor do que o tamanho original da tabela:

![table2](https://github.com/textualize/rich/raw/main/imgs/table2.png)

</details>

<details>
<summary>Barra de Progresso</summary>

O Rich consegue renderizar de forma eficiente múltiplas [barras de progresso](https://rich.readthedocs.io/en/latest/progress.html) que podem ser usadas para rastrear o estado de processos longos.

Uma forma simples de usar é passando o iterável para a função `track` e iterar normalmente sobre o retorno. Veja o exemplo a seguir:

```python
from rich.progress import track

for step in track(range(100)):
    do_step(step)
```

Adicionar múltiplas barras de progresso também é simples. Veja outro exemplo que existe na documentação:

![progress](https://github.com/textualize/rich/raw/main/imgs/progress.gif)

As colunas podem ser configuradas pra mostrar qualquer detalho necessário. As colunas nativas incluem a porcentagem completa, tamanho de arquivo, velocidade do arquivo e tempo restante. O exemplo a seguir mostra o progresso de um download:

![progress](https://github.com/textualize/rich/raw/main/imgs/downloader.gif)

Para testar isso no seu terminal, use o arquivo [examples/downloader.py](https://github.com/textualize/rich/blob/main/examples/downloader.py) para fazer o download de múltiplas URLs simultaneamente, exibindo o progresso de cada download.

</details>

<details>
<summary>Status</summary>

Em casos em que é dificil calcular o progresso da tarefa, você pode usar o método [status](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console.status) que exibe uma animação de um "spinner" e a mensagem. A animação não impede em nada o uso do `console`. Veja o exemplo a seguir:

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

Este código resultará no seguinte output no terminal:

![status](https://github.com/textualize/rich/raw/main/imgs/status.gif)

As animações do "spinner" foram emprestadas do [cli-spinners](https://www.npmjs.com/package/cli-spinners). É possível escolher um estilo de "spinner" usando o parametro `spinner`. Execute o comando a seguir para ver todos os tipos de "spinner" disponíveis.

```
python -m rich.spinner
```

O comando acima deve exibir o seguinte no seu terminal:

![spinners](https://github.com/textualize/rich/raw/main/imgs/spinners.gif)

</details>

<details>
<summary>Árvore</summary>

O Rich pode renderizar [árvores](https://rich.readthedocs.io/en/latest/tree.html) com linhas de identação. Uma árvore é a forma ideal de exibir uma estrutura de arquivos ou qualquer outra apresentação hierárquica de dados.

Os titulos dos itens da árvore podem ser textos simples ou qualquer coisa que o Rich pode renderizar. Execute o comando a seguir para uma demonstração:

```
python -m rich.tree
```

Isso gera o seguinte resultado:

![markdown](https://github.com/textualize/rich/raw/main/imgs/tree.png)

Veja o exemplo em [tree.py](https://github.com/textualize/rich/blob/main/examples/tree.py) de um código que gera uma árvore de exibição de um dicionário, semelhante ao comando `tree` do linux.

</details>

<details>
<summary>Colunas</summary>

O Rich pode renderizar conteúdos em [colunas](https://rich.readthedocs.io/en/latest/columns.html) bem formatadas com tamanhos iguais ou otimizados. O exemplo a seguir é uma cópia básica do comando `ls` (presente no MacOS / Linux) que mostra o conteúdo de uma pasta organizado em colunas:

```python
import os
import sys

from rich import print
from rich.columns import Columns

directory = os.listdir(sys.argv[1])
print(Columns(directory))
```

O screenshot a seguir é do resultado do [exemplo de colunas](https://github.com/textualize/rich/blob/main/examples/columns.py) formatando em colunas os dados extraídos de uma API:

![columns](https://github.com/textualize/rich/raw/main/imgs/columns.png)

</details>

<details>
<summary>Markdown</summary>

O Rich pode renderizar [markdown](https://rich.readthedocs.io/en/latest/markdown.html) e faz um bom trabalho de conversão do formato para o terminal.

Para renderizar markdown, importe a classe `Markdown` e instancie com a string que contém o código markdown. Depois, imprima o objeto no console. Por exemplo:

```python
from rich.console import Console
from rich.markdown import Markdown

console = Console()
with open("README.md") as readme:
    markdown = Markdown(readme.read())
console.print(markdown)
```

Isso produzirá um resultado como:

![markdown](https://github.com/textualize/rich/raw/main/imgs/markdown.png)

</details>

<details>
<summary>Highlight de Sintaxe</summary>

O Rich usa a biblioteca [pygments](https://pygments.org/) para implementar o [highlight de sintaxe](https://rich.readthedocs.io/en/latest/syntax.html). O uso é similar à renderização de markdown, instancie um objeto da classe `Syntax` imprima no console. Por exemplo:

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

Este código gerará o seguinte resultado:

![syntax](https://github.com/textualize/rich/raw/main/imgs/syntax.png)

</details>

<details>
<summary>Rastreio de Erros (tracebacks)</summary>

O Rich renderiza [tracebacks formatados](https://rich.readthedocs.io/en/latest/traceback.html) que são fáceis de ler e mostra mais código do que os tracebacks padrão do Python. É possivel configurar o Rich como o gerenciador padrão de tracebacks para que todas as excessões inesperadas sejam renderizadas pelo Rich.

Veja o resultado disso no OSX (resultados semelhantes no Linux):

![traceback](https://github.com/textualize/rich/raw/main/imgs/traceback.png)

</details>

Todos os renderizáveis do Rich usam o [Protocolo do Console](https://rich.readthedocs.io/en/latest/protocol.html), que você pode usar para implementar o seu próprio conteúdo Rich.

# Rich para empresas

Disponível como parte da assinatura Tidelift.

Os mantenedores do Rich e milhares de outros pacotes estão trabalhando com o Tidelift para disponibilizar suporte comercial e manutenção de projetos de código aberto usados nas suas aplicações. Economize tempo, reduza riscos e melhore a qualidade do código enquanto paga os mantenedores dos pacotes exatos que você usa. [Mais detalhes.](https://tidelift.com/subscription/pkg/pypi-rich?utm_source=pypi-rich&utm_medium=referral&utm_campaign=enterprise&utm_term=repo)

# Projetos usando Rich

Aqui estão alguns projetos que usam o Rich:

- [BrancoLab/BrainRender](https://github.com/BrancoLab/BrainRender)
  a python package for the visualization of three dimensional neuro-anatomical data
  um pacote python para visualisação tridimensional de dados neuro-atômicos.
- [Ciphey/Ciphey](https://github.com/Ciphey/Ciphey)
  ferramenta de descriptografia autoatizada.
- [emeryberger/scalene](https://github.com/emeryberger/scalene)
  um analisador de CPU e memória de alta performance e alta precisão para Python
- [hedythedev/StarCli](https://github.com/hedythedev/starcli)
  Explore projetos de destaque no GitHub pela linha de comando do terminal
- [intel/cve-bin-tool](https://github.com/intel/cve-bin-tool)
  Essa ferramenta verifica a vulnerabilidade de diversos componentes populares (openssl, libpng, libxml2, expat e outros) presentes no seu sistema e alerta para possíveis vulnerabilidades conhecidas.
- [nf-core/tools](https://github.com/nf-core/tools)
  pacote Python com ferramentas auxiliares par a comunidade nf-core.
- [cansarigol/pdbr](https://github.com/cansarigol/pdbr)
  pdb + Rich para auxiliar no debug
- [plant99/felicette](https://github.com/plant99/felicette)
  Imagem de satélites para iniciantes.
- [seleniumbase/SeleniumBase](https://github.com/seleniumbase/SeleniumBase)
  Automatize & teste 10x mais rápido com Selenium & pytest. Baterias inclusas.
- [smacke/ffsubsync](https://github.com/smacke/ffsubsync)
  Automagicamente sincronize legendas com vídeos.
- [tryolabs/norfair](https://github.com/tryolabs/norfair)
  Biblioteca Python para adicionar rastreio em tempo real de objetos 2D em qualquer detector.
- [ansible/ansible-lint](https://github.com/ansible/ansible-lint) Ansible-lint verifica boas práticas e comportamento que podem ser melhorados.
- [ansible-community/molecule](https://github.com/ansible-community/molecule) Framework de test para Ansible Molecule
- +[Muitos outros](https://github.com/textualize/rich/network/dependents)!

<!-- This is a test, no need to translate -->
