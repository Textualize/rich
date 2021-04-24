import re


def camel_to_snake(name: str, _re_snake=re.compile("[a-z][A-Z]")) -> str:
    """Convert name from CamelCase to snake_case.

    Args:
        name (str): A symbol name, such as a class name.

    Returns:
        str: Name in camel case.
    """

    def repl(match) -> str:
        lower, upper = match.group()
        return f"{lower}_{upper.lower()}"

    return _re_snake.sub(repl, name).lower()


if __name__ == "__main__":
    print(camel_to_snake("HelloWorldEvent"))