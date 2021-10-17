try:
    import click
except ImportError:
    print("Please install click for this example")
    print("    pip install click")
    exit()

from rich.traceback import install

install(suppress=[click])


@click.command()
@click.option("--count", default=1, help="Number of greetings.")
def hello(count):
    """Simple program that greets NAME for a total of COUNT times."""
    1 / 0
    for x in range(count):
        click.echo(f"Hello {name}!")


if __name__ == "__main__":
    hello()
