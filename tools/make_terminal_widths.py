from functools import partial
from typing import List
import os.path
from urllib.request import urlopen

from rich.progress import Progress


def download(url: str) -> str:
    """Copy data from a url to a local file."""

    # This will break if the response doesn't contain content length
    filename = url.rsplit("/")[-1]
    if os.path.exists(filename):
        print(f"{filename} exists")
        return filename
    progress = Progress()
    task = progress.add_task(filename)
    with progress:
        response = urlopen(url)
        progress.update(task, total=int(response.info()["Content-length"]))
        with open(filename, "wb") as dest_file:
            for data in iter(partial(response.read, 32768), b""):
                dest_file.write(data)
                progress.advance(task, len(data))
    return filename


def get_data():
    east_asian_filename = download(
        "http://www.unicode.org/Public/UNIDATA/EastAsianWidth.txt"
    )
    download(
        "http://www.unicode.org/Public/UNIDATA/extracted/DerivedGeneralCategory.txt"
    )
    print(parse_east_asian(east_asian_filename))


def parse_east_asian(filename: str) -> List[int]:
    codepoints: List[int] = []
    for line in open(filename, "rt"):
        if line.startswith("#") or not line.strip():
            continue
        print(line)
        first_field = line.split()[0]
        if ";" not in first_field:
            continue
        codepoint_range, details = first_field.split(";", 1)
        if ".." in codepoint_range:
            start, end = codepoint_range.split("..")
            codepoints.extend(range(int(start, 16), int(end, 16) + 1))
        else:
            codepoints.append(int(codepoint_range, 16))

    return codepoints


def run():
    get_data()


if __name__ == "__main__":
    run()

