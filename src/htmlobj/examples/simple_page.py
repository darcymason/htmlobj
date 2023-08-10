from htmlobj import HTML


def make_row(text1, text2):
    """Make an `HTML` object to add to another one"""
    h = HTML()
    with h.tr:
        h.td(text1)
        h.td(text2)
    return h


h = HTML("html")  # can pass root tag to HTML()
h.head.title("My Page")  # chain tags if only 1 subitem
with h.body:  # use `with` for multiple subitems
    h.p.u("Table example")
    with h.table(
        cellpadding="5", border="1", style="border-collapse:collapse"
    ):
        with h.tr:
            h.td("Cell 1")
            with h.td("Start text, ", class_="tdlink"):
                h.a("url link", href="somewhere/")
                h.text(", more text")  # or `h += ...`
        with h.tr as row2:  # Alternate form `with ... as`
            row2.td("R2C1")
            row2.td("R2C2 (red)", style="color: red")
        h += make_row("R3C1", "R3C2")  # `+=` add another HTML obj or text

    h.p.u("List")
    with h.ul:
        for i, item in enumerate(["Apples", "Bananas", "Carrots", "Dates"]):
            h.li(
                f"Item {i+1}: {item}",
                style="background-color: lightgrey" if i % 2 else "",
            )


from tempfile import NamedTemporaryFile
import webbrowser


with NamedTemporaryFile("w", delete=False, suffix=".html") as f:
    url = "file://" + f.name
    f.write(f"<!DOCTYPE html>\n{h}")
webbrowser.open(url)
