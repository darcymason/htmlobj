"""Simple, elegant HTML, XHTML and XML generation.
"""

import html
from keyword import iskeyword  # Python's lib


INDENT = "    "  # for codify


class HTML:
    """Easily generate HTML.

    ```python
    h = HTML()
    with h.table:
        with h.tr:
            h.td("cell 1")
            h.td("cell 2")
    h.p.u("List")
    with h.ul:
        for i in range(3):
            h.li(f"Item {i}")

    print(h)
    ```

    Output:
    ```
    '<table><tr><td>cell 1</td>...'
    ```
    """

    newline_default_on = set("table ol ul dl span html head body ".split())
    """html tags which use newlines by default"""

    def __init__(
        self,
        name: str | None = None,
        text: str | None = None,
        stack: list | None = None,
        newlines: bool = True,
        escape: bool = True,
    ):
        """Create a new `HTML` instance

        Args:
            name (str | None, optional): html tag name to start with. Defaults to None.
            text (str | None, optional): Text for inside html tag. Defaults to None.
            stack (list | None, optional): Internal use - stack of contents. Defaults to None.
            newlines (bool, optional): Whether to put newlines in string output. Defaults to True.
            escape (bool, optional): Whether to 'escape' special html characters. Defaults to True.
        """

        self._name = name
        self._content = []
        self._attrs = {}
        # insert newlines between content?
        if stack is None:
            stack = [self]
            self._top = True
            self._newlines = newlines
        else:
            self._top = False
            self._newlines = name in self.newline_default_on
        self._stack = stack
        if text is not None:
            self.text(text, escape)

    @classmethod
    def from_html(self, html: str) -> "HTML":
        """Parse the given html string and return a corresponding instance of this class

        Args:
            html (str): The html text to create the `htmlobj.HTML` instance from

        Returns:
            HTML: A new instance of the `HTML` class
        """

        from .html_parser import HtmlParser  # here to avoid circular import

        parser = HtmlParser()
        parser.feed(html)
        return parser.h

    @classmethod
    def from_url(self, url: str) -> "HTML":
        """Parse the HTML from the given url and return a new instance of this class

        Args:
            url (str): A web-site url as accepted by urllib

        Returns:
            HTML (HTML): a new instance of the `HTML` class
        """

        import urllib.request

        with urllib.request.urlopen(url) as response:
            html = response.read().decode(
                response.headers.get_content_charset()
            )
            # print("\n".join(html.splitlines()[:40]))
        return self.from_html(html)

    def __getattr__(self, name: str) -> "str | HTML":
        # Called when adding a new tag, e.g. `h.tag`, or `h.newline`
        if name == "newline":
            e = "\n"
        else:
            e = self.__class__(name, stack=self._stack)
        if self._top:
            self._stack[-1]._content.append(e)
        else:
            self._content.append(e)
        return e

    def __iadd__(self, other: "str | HTML") -> "HTML":
        """Operator for `+=`. Add content to the current HTML object

        Args:
            other (str | HTML): text, or `HTML` instance to add

        Returns:
            HTML: A reference to this instance
        """

        if self._top:
            self._stack[-1]._content.append(other)
        else:
            self._content.append(other)
        return self

    def text(self, text: str, escape: bool = True) -> "HTML":
        """Add text to the current HTML object.

        Args:
            text (str): The text to add inside the html tag
            escape (bool, optional): Whether to 'escape' the html for special characters. Defaults to True.
        """
        if escape:
            text = html.escape(text)
        # adding text
        if self._top:
            self._stack[-1]._content.append(text)
        else:
            self._content.append(text)

    def raw_text(self, text: str) -> "HTML":
        """Add raw, unescaped text to the `HTML` object.

        Args:
            text (str): The text to add inside the html tag

        Returns:
            HTML: A reference to this `HTML` instance
        """

        return self.text(text, escape=False)

    def __call__(self, *args, **kwargs) -> "HTML":
        """'Magic method' called when adding attrs in brackets e.g. h.tag(...)

        Raises:
            TypeError: if called with `read` (problem with some WSGI providers)

        Returns:
            HTML: A reference to this `HTML` instance
        """

        if self._name == "read":
            if len(args) == 1 and isinstance(args[0], int):
                raise TypeError(
                    f"you appear to be calling read({args}) on a HTML instance"
                )
            elif len(args) == 0:
                raise TypeError(
                    "you appear to be calling read() on a HTML instance"
                )

        # customising a tag with content or attributes
        escape = kwargs.pop("escape", True)
        if args:
            if escape:
                self._content = [html.escape(c) for c in args]
            else:
                self._content = args
        if "newlines" in kwargs:
            # special-case to allow control over newlines
            self._newlines = kwargs.pop("newlines")
        for k,v in kwargs.items():
            if k.endswith("_") and iskeyword(k[:-1]):
                k = k[:-1]
            elif k == "klass":
                k = "class"
            self._attrs[k] = html.escape(v, True) if v and escape else v
        
        return self

    def __enter__(self) -> "HTML":
        # we're now adding tags to me!
        self._stack.append(self)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        # we're done adding tags to me!
        self._stack.pop()

    def __repr__(self) -> str:
        return f"<HTML {self._name} 0x{id(self):x}>"

    def _codify_text(self, lines, indent_str, text):
        text = repr(text)
        if lines[-1].strip().startswith("h.raw_text"):
            # Append current onto it: take away ') and add new one
            lines[-1] = f"{lines[-1][:-2]}{text[1:]})"
        else:
            lines.append(f"{indent_str}h.raw_text({text})")

    def _codify(self, lines: list, indent: int):
        """Called by `codify` to do the real work

        Updates `lines` as recursively calls itself
        """
        indent_str = "    " * indent
        # Strip out newlines so don't turn into h.text("\n")
        content = [
            c for c in self._content if isinstance(c, HTML) or c.strip() != ""
        ]
        if self._name is None:  # Should only be for top-level one
            for c in content:
                if isinstance(c, HTML):
                    c._codify(lines, indent)
                else:
                    self._codify_text(lines, indent_str, c)
            return
        attr_strs = [
            f'{key if not iskeyword(key) else key+"_"}="{val}"'
            if val is not None
            else f"{key}=None"
            for key, val in self._attrs.items()
        ]

        attrs_str = ", ".join(attr_strs)

        has_sub_objs = any(isinstance(c, HTML) for c in content)
        bracket_attrs_str = f"({attrs_str})" if attrs_str else ""
        with_line = f"{indent_str}with h.{self._name}{bracket_attrs_str}:"

        if not has_sub_objs:
            if not content:
                lines.append(f"{indent_str}h.{self._name}{bracket_attrs_str}")
            elif len(content) == 1:
                lines.append(
                    f'{indent_str}h.{self._name}("{content[0]}"{", " + attrs_str if attrs_str else ""})'
                )
            else:
                lines.append(with_line)
                for c in content:
                    self._codify_text(lines, indent_str + INDENT, c)

        else:
            lines.append(with_line)
            for c in content:
                if isinstance(c, HTML):
                    c._codify(lines, indent + 1)
                else:
                    self._codify_text(lines, indent_str + INDENT, c)

    def codify(self) -> str:
        """Turn the `HTML` object into Python code

        Returns:
            str: Python code to generate this `HTML` instance

        Note:
            `codify` is usually used when the HTML instance has been
            created using `from_url` or `from_html`
        """

        lines = ["h = HTML()"]
        self._codify(lines, 0)
        return "\n".join(lines)

    def _stringify(self, str_type) -> str:
        # turn me and my content into text
        join_chr = "\n" if self._newlines else ""
        if self._name is None:
            return join_chr.join(str_type(c) for c in self._content)
        attr_strs = [
            f'{key}="{val}"' if val is not None else f"{key}"
            for key, val in self._attrs.items()
        ]
        l = [self._name] + attr_strs
        s = f"<{' '.join(l)}>{join_chr}"
        if self._content:
            s += join_chr.join(str_type(c) for c in self._content)
            s += join_chr + f"</{self._name}>"
        return s

    def __str__(self) -> str:
        return self._stringify(str)


if __name__ == "__main__":
    h = HTML()
    h.td(class_="testclass")
    print(h)