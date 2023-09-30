"""Class to parse existing html into htmlobj classes"""
from html.parser import HTMLParser  # subclass Python's parser
from htmlobj import HTML


class HtmlParser(HTMLParser):
    """Parse html into htmlobj.HTML classes"""

    start_tag_only = ["input", "br", "img", "option", "link"]

    def __init__(self, convert_charrefs=False):
        self.h = HTML()
        super().__init__(convert_charrefs=convert_charrefs)

    def handle_starttag(self, tag, attrs):
        new_h = getattr(self.h, tag)
        new_h(**dict(attrs))
        if tag not in self.start_tag_only:
            new_h.__enter__()

    def handle_startendtag(self, tag, attrs):
        new_h = getattr(self.h, tag)
        new_h(**dict(attrs))

    def handle_charref(self, name):
        # data = html.unescape(f"&    {name};")
        self.handle_data(f"&#{name};")

    def handle_entityref(self, name):
        # data = html.unescape(f"&#{name};")
        self.handle_data(f"&{name};")

    def handle_data(self, data):
        self.h.raw_text(data)

    def handle_endtag(self, tag):
        if tag not in self.start_tag_only:
            self.h.__exit__(None, None, None)

    def handle_comment(self, data: str) -> None:
        return super().handle_comment(data)


if __name__ == "__main__":
    import sys

    usage = """
    python html_parser.py <source> [<lines to display>]

    where source (required) is one of:
    url:  a url to an HTML source, like a web page
    str: a string containing HTML text to parse
    
    <lines to display> is an optional number of lines to output

    The output is a `codify`d version of the HTML source,
    i.e. it is Python code using htmlobj to re-create the HTML
    """

    num_args = len(sys.argv)
    if not 2 <= num_args <= 3:
        print(usage)
        sys.exit(-1)

    if num_args > 1:
        param = sys.argv[1]
        if param.startswith("http"):
            h = HTML.from_url(param)
        else:
            h = HTML.from_html(param)

    code = h.codify()
    code_lines = code.splitlines()
    lines_to_display = len(code_lines)  # show all by default
    if num_args > 2:
        lines_to_display = int(sys.argv[2])

    print("\n".join(code_lines[:lines_to_display]))
