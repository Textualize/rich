import pathlib


def get_capture_text(*paths: str) -> str:
    with open(
        pathlib.Path(__file__).parent.joinpath("captures", *paths), mode="rb"
    ) as file:
        return file.read().decode()


def set_capture_text(*paths: str, output: str) -> None:
    with open(
        pathlib.Path(__file__).parent.joinpath("captures", *paths), mode="wb"
    ) as file:
        file.write(output.encode())
