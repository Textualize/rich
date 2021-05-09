from typing import List

try:
    import attr
except ImportError:
    print("This example requires attrs library")
    print("pip install attrs")
    raise


@attr.define
class Point3D:
    x: float
    y: float
    z: float = 0


@attr.define
class Triangle:
    point1: Point3D
    point2: Point3D
    point3: Point3D


@attr.define
class Model:
    name: str
    triangles: List[Triangle] = attr.Factory(list)


if __name__ == "__main__":
    model = Model(
        name="Alien#1",
        triangles=[
            Triangle(
                Point3D(x=20, y=50),
                Point3D(x=50, y=15, z=-45.34),
                Point3D(3.1426, 83.2323, -16),
            )
        ],
    )

    from rich.console import Console

    console = Console()

    console.print(
        "\nRich can pretty print [b]attrs[/b] objects ( https://www.attrs.org/en/stable/ )\n",
        justify="center",
    )

    console.rule("attrs without Rich")

    print(model)

    console.rule("attrs with Rich")

    console.print(model)
