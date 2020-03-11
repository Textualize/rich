import pytest

from rich.color import Color, ColorType
from rich import errors
from rich.style import Style, StyleStack


def test_str():
    assert str(Style()) == "none"
    assert str(Style(bold=True)) == "bold"
    assert str(Style(color="red", bold=True)) == "bold red"
    assert (
        str(
            Style(
                color="red",
                bgcolor="black",
                bold=True,
                dim=True,
                italic=True,
                underline=True,
                blink=True,
                blink2=True,
                reverse=True,
                conceal=True,
                strike=True,
            )
        )
        == "bold dim italic underline blink blink2 reverse conceal strike red on black"
    )


def test_repr():
    assert repr(Style(bold=True, color="red")) == '<style "bold red">'


def test_eq():
    assert Style(bold=True, color="red") == Style(bold=True, color="red")
    assert Style(bold=True, color="red") != Style(bold=True, color="green")
    assert Style().__eq__("foo") == NotImplemented


def test_hash():
    assert isinstance(hash(Style()), int)


def test_color_property():
    assert Style(color="red").color == Color("red", ColorType.STANDARD, 1, None)


def test_bgcolor_property():
    assert Style(bgcolor="black").bgcolor == Color("black", ColorType.STANDARD, 0, None)


def test_parse():
    assert Style.parse("") == Style()
    assert Style.parse("red") == Style(color="red")
    assert Style.parse("not bold") == Style(bold=False)
    assert Style.parse("bold red on black") == Style(
        color="red", bgcolor="black", bold=True
    )
    with pytest.raises(errors.StyleSyntaxError):
        Style.parse("on")
    with pytest.raises(errors.StyleSyntaxError):
        Style.parse("on nothing")
    with pytest.raises(errors.StyleSyntaxError):
        Style.parse("rgb(999,999,999)")
    with pytest.raises(errors.StyleSyntaxError):
        Style.parse("not monkey")


def test_get_html_style():
    assert (
        Style(
            reverse=True,
            dim=True,
            color="red",
            bgcolor="blue",
            bold=True,
            italic=True,
            underline=True,
            strike=True,
        ).get_html_style()
        == "color: #7f7fbf; background-color: #800000; font-weight: bold; font-style: italic; text-decoration: underline; text-decoration: line-through"
    )


def test_chain():
    assert Style.chain(Style(color="red"), Style(bold=True)) == Style(
        color="red", bold=True
    )


def test_copy():
    style = Style(color="red", bgcolor="black", italic=True)
    assert style == style.copy()
    assert style is not style.copy()


def test_render():
    assert Style(color="red").render("foo", color_system=None) == "foo"
    assert (
        Style(color="red", bgcolor="black", bold=True).render("foo")
        == "\x1b[1;31;40mfoo\x1b[0m"
    )
    assert Style().render("foo") == "foo"


def test_test():
    Style(color="red").test("hello")


def test_add():
    assert Style(color="red") + None == Style(color="red")
    assert Style().__add__("foo") == NotImplemented


def test_iadd():
    style = Style(color="red")
    style += Style(bold=True)
    assert style == Style(color="red", bold=True)
    style += None
    assert style == Style(color="red", bold=True)
    assert style.__iadd__("foo") == NotImplemented


def test_style_stack():
    stack = StyleStack(Style(color="red"))
    repr(stack)
    assert stack.current == Style(color="red")
    stack.push(Style(bold=True))
    assert stack.current == Style(color="red", bold=True)
    stack.pop()
    assert stack.current == Style(color="red")
