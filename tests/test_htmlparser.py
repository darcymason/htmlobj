import pathlib
from textwrap import dedent
from htmlobj.html_parser import main


HERE = pathlib.Path(__file__).resolve().parent


def test_from_file():
    """html_parser can render an html file to code"""
    expected = dedent(
        """\
        h = HTML()
        with h.html:
            with h.head:
                h.title("My Page")
            with h.body:
                with h.p:
                    with h.u:
                        h.raw_text('Paragraph&nbsp;1 underlined')
                with h.p(class_="p2"):
                    h.raw_text('Paragraph 2, &#62;1 ')
                    h.b("bold")
                    h.raw_text(', not bold')"""
    )


    html_file = HERE / "test_files" / "simple1.html"
    args = ["", html_file.as_uri(), "12"]  # 8 lines
    result = main(args)

    assert result == expected
