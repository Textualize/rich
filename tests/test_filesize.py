from rich import filesize


def test_traditional():
    assert filesize.decimal(0) == "0 bytes"
    assert filesize.decimal(1) == "1 byte"
    assert filesize.decimal(2) == "2 bytes"
    assert filesize.decimal(1000) == "1.0 kB"
    assert filesize.decimal(1.5 * 1000 * 1000) == "1.5 MB"
    assert filesize.decimal(0, precision=2) == "0 bytes"
    assert filesize.decimal(1111, precision=0) == "1 kB"
    assert filesize.decimal(1111, precision=1) == "1.1 kB"
    assert filesize.decimal(1111, precision=2) == "1.11 kB"
    assert filesize.decimal(1111, separator="") == "1.1kB"


def test_pick_unit_and_suffix():
    units = ["bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    assert filesize.pick_unit_and_suffix(50, units, 1024) == (1, "bytes")
    assert filesize.pick_unit_and_suffix(2048, units, 1024) == (1024, "KB")
