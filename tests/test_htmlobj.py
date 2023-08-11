from textwrap import dedent

from htmlobj.htmlobj import HTML
from htmlobj.xhtml import XHTML
from htmlobj.xml import XML


def test_from_html():
    """HTML.from_html works as expected"""

    source_html = (
        '<table class="tbl"><td class="xxtd" nowrap>Parse me!</td></table>'
    )
    h = HTML.from_html(source_html)

    assert "".join(x.strip() for x in str(h).splitlines()) == source_html
    assert True


def test_empty_tag():
    "generation of an empty HTML tag"
    assert str(HTML().br) == "<br>"


def test_empty_tag_xml():
    "generation of an empty XHTML tag"
    assert str(XHTML().br) == "<br />"


def test_tag_add():
    "test top-level tag creation"
    assert str(HTML("html", "text")) == "<html>\ntext\n</html>"


def test_tag_add_no_newline():
    "test top-level tag creation"
    assert str(HTML("html", "text", newlines=False)) == "<html>text</html>"


def test_iadd_tag():
    "test iadd'ing a tag"
    h = XML("xml")
    h += XML("some-tag", "spam", newlines=False)
    h += XML("text", "spam", newlines=False)
    assert (
        str(h) == "<xml>\n<some-tag>spam</some-tag>\n<text>spam</text>\n</xml>"
    )


def test_iadd_text():
    "test iadd'ing text"
    h = HTML("html", newlines=False)
    h += "text"
    h += "text"
    assert str(h) == "<html>texttext</html>"


def test_xhtml_match_tag():
    "check forced generation of matching tag when empty"
    assert str(XHTML().p) == "<p></p>"


def test_just_tag():
    "generate HTML for just one tag"
    assert str(HTML().br) == "<br>"


def test_just_tag_xhtml():
    "generate XHTML for just one tag"
    assert str(XHTML().br) == "<br />"


def test_xml():
    "generate XML"
    assert str(XML().br) == "<br />"
    assert str(XML().p) == "<p />"
    assert str(XML().br("text")) == "<br>text</br>"


def test_para_tag():
    "generation of a tag with contents"
    h = HTML()
    h.p("hello")
    assert str(h) == "<p>hello</p>"


def test_escape():
    "escaping of special HTML characters in text"
    h = HTML()
    h.text("<>&")
    assert str(h) == "&lt;&gt;&amp;"


def test_no_escape():
    "no escaping of special HTML characters in text"
    h = HTML()
    h.text("<>&", False)
    assert str(h) == "<>&"


def test_escape_attr():
    "escaping of special HTML characters in attributes"
    h = HTML()
    h.br(id='<>&"')
    assert str(h) == '<br id="&lt;&gt;&amp;&quot;">'


def test_subtag_context():
    'generation of sub-tags using "with" context'
    h = HTML()
    with h.ol:
        h.li("foo")
        h.li("bar")
    assert str(h) == "<ol>\n<li>foo</li>\n<li>bar</li>\n</ol>"


def test_subtag_direct():
    "generation of sub-tags directly on the parent tag"
    h = HTML()
    ol = h.ol
    ol.li("foo")
    ol.li.b("bar")
    assert str(h) == "<ol>\n<li>foo</li>\n<li><b>bar</b></li>\n</ol>"


def test_subtag_direct_context():
    'generation of sub-tags directly on the parent tag in "with" context'
    h = HTML()
    with h.ol as ol:
        ol.li("foo")
        ol.li.b("bar")
    assert str(h) == "<ol>\n<li>foo</li>\n<li><b>bar</b></li>\n</ol>"


def test_subtag_no_newlines():
    "prevent generation of newlines against default"
    h = HTML()
    ol = h.ol(newlines=False)
    ol.li("foo")
    ol.li("bar")
    assert str(h) == "<ol><li>foo</li><li>bar</li></ol>"


def test_add_text():
    "add text to a tag"
    h = HTML()
    p = h.p("hello, world!\n")
    p.text("more text")
    assert str(h), "<p>hello == world!\nmore text</p>"


def test_add_text_newlines():
    "add text to a tag with newlines for prettiness"
    h = HTML()
    p = h.p("hello, world!", newlines=True)
    p.text("more text")
    assert str(h), "<p>\nhello == world!\nmore text\n</p>"


def test_doc_newlines():
    "default document adding newlines between tags"
    h = HTML()
    h.br  # noqa: B018
    h.br  # noqa: B018
    assert str(h) == "<br>\n<br>"


def test_doc_no_newlines():
    "prevent document adding newlines between tags"
    h = HTML(newlines=False)
    h.br  # noqa: B018
    h.br  # noqa: B018
    assert str(h) == "<br><br>"


def test_table():
    'multiple "with" context blocks'
    h = HTML()
    with h.table(border="1"):
        for _ in range(2):
            with h.tr:
                h.td("column 1")
                h.td("column 2")
    assert str(h) == dedent(
        """\
        <table border="1">
        <tr><td>column 1</td><td>column 2</td></tr>
        <tr><td>column 1</td><td>column 2</td></tr>
        </table>"""
    )
