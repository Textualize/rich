import pytest

from rich import errors
from rich.color import Color, ColorSystem, ColorType
from rich.style import Style, StyleStack


def test_str():
    assert str(Style(bold=False)) == "not bold"
    assert str(Style(color="red", bold=False)) == "not bold red"
    assert str(Style(color="red", bold=False, italic=True)) == "not bold italic red"
    assert str(Style()) == "none"
    assert str(Style(bold=True)) == "bold"
    assert str(Style(color="red", bold=True)) == "bold red"
    assert str(Style(color="red", bgcolor="black", bold=True)) == "bold red on black"
    all_styles = Style(
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
        underline2=True,
        frame=True,
        encircle=True,
        overline=True,
    )
    expected = "bold dim italic underline blink blink2 reverse conceal strike underline2 frame encircle overline red on black"
    assert str(all_styles) == expected
    assert str(Style(link="foo")) == "link foo"


def test_ansi_codes():
    all_styles = Style(
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
        underline2=True,
        frame=True,
        encircle=True,
        overline=True,
    )
    expected = "1;2;3;4;5;6;7;8;9;21;51;52;53;31;40"
    assert all_styles._make_ansi_codes(ColorSystem.TRUECOLOR) == expected


def test_repr():
    assert (
        repr(Style(bold=True, color="red"))
        == "Style(color=Color('red', ColorType.STANDARD, number=1), bold=True)"
    )


def test_eq():
    assert Style(bold=True, color="red") == Style(bold=True, color="red")
    assert Style(bold=True, color="red") != Style(bold=True, color="green")
    assert Style().__eq__("foo") == NotImplemented


def test_hash():
    assert isinstance(hash(Style()), int)


def test_empty():
    assert Style.null() == Style()


def test_bool():
    assert bool(Style()) is False
    assert bool(Style(bold=True)) is True
    assert bool(Style(color="red")) is True
    assert bool(Style.parse("")) is False


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
    assert Style.parse("bold link https://example.org") == Style(
        bold=True, link="https://example.org"
    )
    with pytest.raises(errors.StyleSyntaxError):
        Style.parse("on")
    with pytest.raises(errors.StyleSyntaxError):
        Style.parse("on nothing")
    with pytest.raises(errors.StyleSyntaxError):
        Style.parse("rgb(999,999,999)")
    with pytest.raises(errors.StyleSyntaxError):
        Style.parse("not monkey")
    with pytest.raises(errors.StyleSyntaxError):
        Style.parse("link")


def test_link_id():
    assert Style().link_id == ""
    assert Style.parse("").link_id == ""
    assert Style.parse("red").link_id == ""
    style = Style.parse("red link https://example.org")
    assert isinstance(style.link_id, str)
    assert len(style.link_id) > 1


def test_get_html_style():
    expected = "color: #7f7fbf; text-decoration-color: #7f7fbf; background-color: #800000; font-weight: bold; font-style: italic; text-decoration: underline; text-decoration: line-through; text-decoration: overline"
    html_style = Style(
        reverse=True,
        dim=True,
        color="red",
        bgcolor="blue",
        bold=True,
        italic=True,
        underline=True,
        strike=True,
        overline=True,
    ).get_html_style()
    print(repr(html_style))
    assert html_style == expected


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


def test_iadd():
    style = Style(color="red")
    style += Style(bold=True)
    assert style == Style(color="red", bold=True)
    style += None
    assert style == Style(color="red", bold=True)


def test_style_stack():
    stack = StyleStack(Style(color="red"))
    repr(stack)
    assert stack.current == Style(color="red")
    stack.push(Style(bold=True))
    assert stack.current == Style(color="red", bold=True)
    stack.pop()
    assert stack.current == Style(color="red")


def test_pick_first():
    with pytest.raises(ValueError):
        Style.pick_first()


def test_background_style():
    assert Style(bold=True, color="yellow", bgcolor="red").background_style == Style(
        bgcolor="red"
    )


def test_without_color():
    style = Style(bold=True, color="red", bgcolor="blue")
    colorless_style = style.without_color
    assert colorless_style.color == None
    assert colorless_style.bgcolor == None
    assert colorless_style.bold == True
    null_style = Style.null()
    assert null_style.without_color == null_style


def test_meta():
    style = Style(bold=True, meta={"foo": "bar"})
    assert style.meta["foo"] == "bar"

    style += Style(meta={"egg": "baz"})

    assert style.meta == {"foo": "bar", "egg": "baz"}

    assert repr(style) == "Style(bold=True, meta={'foo': 'bar', 'egg': 'baz'})"


def test_from_meta():
    style = Style.from_meta({"foo": "bar"})
    assert style.color is None
    assert style.bold is None


def test_on():
    style = Style.on({"foo": "bar"}, click="CLICK") + Style(color="red")
    assert style.meta == {"foo": "bar", "@click": "CLICK"}


def test_clear_meta_and_links():
    style = Style.parse("bold red on black link https://example.org") + Style.on(
        click="CLICK"
    )

    assert style.meta == {"@click": "CLICK"}
    assert style.link == "https://example.org"
    assert style.color == Color.parse("red")
    assert style.bgcolor == Color.parse("black")
    assert style.bold
    assert not style.italic

    clear_style = style.clear_meta_and_links()

    assert clear_style.meta == {}
    assert clear_style.link == None
    assert clear_style.color == Color.parse("red")
    assert clear_style.bgcolor == Color.parse("black")
    assert clear_style.bold
    assert not clear_style.italic
