from rich._null_file import NullFile


def test_null_file():
    file = NullFile()
    with file:
        assert file.write("abc") == 0
        assert file.close() is None
        assert not file.isatty()
        assert file.read() == ""
        assert not file.readable()
        assert file.readline() == ""
        assert file.readlines() == []
        assert file.seek(0, 0) == 0
        assert not file.seekable()
        assert file.tell() == 0
        assert file.truncate() == 0
        assert file.writable() == False
        assert file.writelines([""]) is None
        assert next(file) == ""
        assert next(iter(file)) == ""
        assert file.fileno() == -1
        assert file.flush() is None
