"""Simple, elegant HTML, XHTML and XML generation.
"""

import html

# 2023-08: Darcy Mason:


INDENT = "    "  # for codify


class HTML:
    """Easily generate HTML.

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
    -> '<table><tr><td>cell 1</td>...'

    """

    newline_default_on = set("table ol ul dl span html head body ".split())

    def __init__(
        self, name=None, text=None, stack=None, newlines=True, escape=True
    ):
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
    def from_html(self, s: str) -> "HTML":
        """Given html text, parse and return as an instance of this class

        Params
        ------
        s: str
            The HTML text to create the `htmlobj.HTML` instance from
        """
        from .html_parser import HtmlParser  # here to avoid circular import

        parser = HtmlParser()
        parser.feed(s)
        return parser.h

    @classmethod
    def from_url(self, url):
        """Parse the HTML from the given url and return instance of this class"""
        import urllib.request

        with urllib.request.urlopen(url) as response:
            html = response.read().decode(
                response.headers.get_content_charset()
            )
            # print("\n".join(html.splitlines()[:40]))
        return self.from_html(html)

    def __getattr__(self, name):
        # adding a new tag or newline
        if name == "newline":
            e = "\n"
        else:
            e = self.__class__(name, stack=self._stack)
        if self._top:
            self._stack[-1]._content.append(e)
        else:
            self._content.append(e)
        return e

    def __iadd__(self, other):
        if self._top:
            self._stack[-1]._content.append(other)
        else:
            self._content.append(other)
        return self

    def text(self, text, escape=True):
        """Add text to the document. If "escape" is True any characters
        special to HTML will be escaped.
        """
        if escape:
            text = html.escape(text)
        # adding text
        if self._top:
            self._stack[-1]._content.append(text)
        else:
            self._content.append(text)

    def raw_text(self, text):
        """Add raw, unescaped text to the document. This is useful for
        explicitly adding HTML code or entities.
        """
        return self.text(text, escape=False)

    def __call__(self, *content, **kw):
        if self._name == "read":
            if len(content) == 1 and isinstance(content[0], int):
                raise TypeError(
                    f"you appear to be calling read({content}) on a HTML instance"
                )
            elif len(content) == 0:
                raise TypeError(
                    "you appear to be calling read() on a HTML instance"
                )

        # customising a tag with content or attributes
        escape = kw.pop("escape", True)
        if content:
            if escape:
                self._content = list(map(html.escape, content))
            else:
                self._content = content
        if "newlines" in kw:
            # special-case to allow control over newlines
            self._newlines = kw.pop("newlines")
        for k in kw:
            if k == "klass" or k == "class_":
                self._attrs["class"] = html.escape(kw[k], True)
            else:
                v = kw[k]
                self._attrs[k] = html.escape(v, True) if v else v
        return self

    def __enter__(self):
        # we're now adding tags to me!
        self._stack.append(self)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        # we're done adding tags to me!
        self._stack.pop()

    def __repr__(self):
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
            f'{key if key != "class" else "class_"}="{val}"'
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
        """Turn the HTML object into Python code to create it"""
        lines = ["h = HTML()"]
        self._codify(lines, 0)
        return "\n".join(lines)

    def _stringify(self, str_type):
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

    def __str__(self):
        return self._stringify(str)

    def __unicode__(self):
        return self._stringify(unicode)

    def __iter__(self):
        return iter([str(self)])
