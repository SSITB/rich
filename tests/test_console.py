import io

import pytest

from rich.color import ColorSystem
from rich.console import Console, ConsoleOptions
from rich import errors
from rich.segment import Segment
from rich.style import Style
from rich.theme import Theme


def test_console_options_update():
    options = ConsoleOptions(
        min_width=10, max_width=20, is_terminal=False, encoding="utf-8"
    )
    options1 = options.update(width=15)
    assert options1.min_width == 15 and options1.max_width == 15

    options2 = options.update(min_width=5, max_width=15, justify="right")
    assert (
        options2.min_width == 5
        and options2.max_width == 15
        and options2.justify == "right"
    )

    options_copy = options.update()
    assert options_copy == options and options_copy is not options


def test_init():
    console = Console(color_system=None)
    assert console._color_system == None
    console = Console(color_system="standard")
    assert console._color_system == ColorSystem.STANDARD
    console = Console(color_system="auto")


def test_size():
    console = Console()
    w, h = console.size
    assert console.width == w

    console = Console(width=99, height=101)
    w, h = console.size
    assert w == 99 and h == 101


def test_repr():
    console = Console()
    assert isinstance(repr(console), str)
    assert isinstance(str(console), str)


def test_print():
    console = Console(file=io.StringIO(), color_system="truecolor")
    console.print("foo")
    assert console.file.getvalue() == "foo\n"


def test_print_empty():
    console = Console(file=io.StringIO(), color_system="truecolor")
    console.print()
    assert console.file.getvalue() == "\n"


def test_markup_highlight():
    console = Console(file=io.StringIO(), color_system="truecolor")
    console.print("'[bold]foo[/bold]'")
    assert (
        console.file.getvalue()
        == "\x1b[32m'\x1b[0m\x1b[1;32mfoo\x1b[0m\x1b[32m'\x1b[0m\n"
    )


def test_print_style():
    console = Console(file=io.StringIO(), color_system="truecolor")
    console.print("foo", style="bold")
    assert console.file.getvalue() == "\x1b[1mfoo\x1b[0m\n"


def test_show_cursor():
    console = Console(file=io.StringIO())
    console.show_cursor(False)
    console.print("foo")
    console.show_cursor(True)
    assert console.file.getvalue() == "\x1b[?25lfoo\n\x1b[?25h"


def test_get_style():
    console = Console()
    console.get_style("repr.brace") == Style(bold=True)


def test_get_style_error():
    console = Console()
    with pytest.raises(errors.MissingStyle):
        console.get_style("nosuchstyle")
    with pytest.raises(errors.MissingStyle):
        console.get_style("foo bar")


def test_render_error():
    console = Console()
    with pytest.raises(errors.NotRenderableError):
        list(console.render([], console.options))


class BrokenRenderable:
    def __console__(self, console, options):
        pass


def test_render_broken_renderable():
    console = Console()
    broken = BrokenRenderable()
    with pytest.raises(errors.NotRenderableError):
        list(console.render(broken, console.options))


def test_export_text():
    console = Console(record=True, width=100)
    console.print("[b]foo")
    text = console.export_text()
    expected = "foo\n"
    assert text == expected


def test_export_html():
    console = Console(record=True, width=100)
    console.print("[b]foo")
    html = console.export_html()
    expected = "<!DOCTYPE html>\n<head>\n<style>\n.r1 {font-weight: bold}\nbody {\n    color: #000000;\n    background-color: #ffffff;\n}\n</style>\n</head>\n<html>\n<body>\n    <code>\n        <pre style=\"font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace\"><span class=\"r1\">foo</span>\n</pre>\n    </code>\n</body>\n</html>\n"
    assert html == expected


def test_export_html_inline():
    console = Console(record=True, width=100)
    console.print("[b]foo")
    html = console.export_html(inline_styles=True)
    expected = "<!DOCTYPE html>\n<head>\n<style>\n\nbody {\n    color: #000000;\n    background-color: #ffffff;\n}\n</style>\n</head>\n<html>\n<body>\n    <code>\n        <pre style=\"font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace\"><span style=\"font-weight: bold\">foo</span>\n</pre>\n    </code>\n</body>\n</html>\n"
    assert html == expected
