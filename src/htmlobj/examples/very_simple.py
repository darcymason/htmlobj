from htmlobj import HTML

h = HTML()
with h.table(border="1", style="border-collapse:collapse"):
    with h.tr:
        h.td("cell 1")
        h.td("cell 2")
h.p.u("List")
with h.ul:
    for i in range(3):
        h.li(f"Item {i}")
print(h)
# -> '<table><tr><td>cell 1</td>...'

from tempfile import NamedTemporaryFile
import webbrowser


with NamedTemporaryFile("w", delete=False, suffix=".html") as f:
    url = "file://" + f.name
    f.write(f"<!DOCTYPE html>\n{h}")
webbrowser.open(url)
