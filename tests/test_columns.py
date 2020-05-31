import io

from rich.columns import Columns
from rich.console import Console

COLUMN_DATA = [
    "Ursus americanus",
    "American buffalo",
    "Bison bison",
    "American crow",
    "Corvus brachyrhynchos",
    "American marten",
    "Martes americana",
    "American racer",
    "Coluber constrictor",
    "American woodcock",
    "Scolopax minor",
    "Anaconda (unidentified)",
    "Eunectes sp.",
    "Andean goose",
    "Chloephaga melanoptera",
    "Ant",
    "Anteater, australian spiny",
    "Tachyglossus aculeatus",
    "Anteater, giant",
    "Myrmecophaga tridactyla",
]


def render():
    console = Console(file=io.StringIO(), width=100)
    columns = Columns(COLUMN_DATA)
    console.print(columns)
    console.print()
    columns.column_first = True
    console.print(columns)
    console.print()
    columns.right_to_left = True
    console.print(columns)
    console.print()
    columns.equal = True
    columns.expand = True
    console.print(columns)
    console.print()
    render_result = console.file.getvalue()
    return render_result


def test_render():
    expected = "Ursus americanus           American buffalo       Bison bison            American crow          \nCorvus brachyrhynchos      American marten        Martes americana       American racer         \nColuber constrictor        American woodcock      Scolopax minor         Anaconda (unidentified)\nEunectes sp.               Andean goose           Chloephaga melanoptera Ant                    \nAnteater, australian spiny Tachyglossus aculeatus Anteater, giant        Myrmecophaga tridactyla\n\nUrsus americanus           Corvus brachyrhynchos   Coluber constrictor Eunectes sp.           \nAnteater, australian spiny American buffalo        American marten     American woodcock      \nAndean goose               Tachyglossus aculeatus  Bison bison         Martes americana       \nScolopax minor             Chloephaga melanoptera  Anteater, giant     American crow          \nAmerican racer             Anaconda (unidentified) Ant                 Myrmecophaga tridactyla\n\nEunectes sp.            Coluber constrictor Corvus brachyrhynchos   Ursus americanus          \nAmerican woodcock       American marten     American buffalo        Anteater, australian spiny\nMartes americana        Bison bison         Tachyglossus aculeatus  Andean goose              \nAmerican crow           Anteater, giant     Chloephaga melanoptera  Scolopax minor            \nMyrmecophaga tridactyla Ant                 Anaconda (unidentified) American racer            \n\nMartes americana                 American crow                     Ursus americanus                 \nAnt                              Eunectes sp.                      American woodcock                \nCorvus brachyrhynchos            American buffalo                  Anteater, giant                  \nAndean goose                     Scolopax minor                    American racer                   \nBison bison                      Myrmecophaga tridactyla           Anteater, australian spiny       \nAnaconda (unidentified)          Coluber constrictor               American marten                  \n                                 Tachyglossus aculeatus            Chloephaga melanoptera           \n\n"
    assert render() == expected


if __name__ == "__main__":
    result = render()
    print(result)
    print(repr(result))
