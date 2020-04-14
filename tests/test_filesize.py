from rich import filesize


def test_traditional():
    assert filesize.decimal(0) == "0 bytes"
    assert filesize.decimal(1) == "1 byte"
    assert filesize.decimal(2) == "2 bytes"
    assert filesize.decimal(1000) == "1.0 kB"
    assert filesize.decimal(1.5 * 1000 * 1000) == "1.5 MB"


def test_pick_unit_and_suffix():
    assert filesize.pick_unit_and_suffix(50, ["foo", "bar", "baz"], 100) == (1, "bytes")
    assert filesize.pick_unit_and_suffix(1500, ["foo", "bar", "baz"], 100) == (
        10000,
        "foo",
    )
