from rich.control import Control, strip_control_codes


def test_control():
    control = Control("FOO")
    assert str(control) == "FOO"


def test_strip_control_codes():
    assert strip_control_codes("") == ""
    assert strip_control_codes("foo\rbar") == "foobar"
    assert strip_control_codes("Fear is the mind killer") == "Fear is the mind killer"
