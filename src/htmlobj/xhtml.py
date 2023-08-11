from .htmlobj import HTML


class XHTML(HTML):
    """Easily generate XHTML. Tags in `empty_elements` are self-terminated.
    
    Example: 
    ```py
    >>> from htmlobj import XHTML
    >>> h = XHTML()
    >>> h.p
    >>> h.br
    >>> print(h)
    <p></p>
    <br />
    ```
    """

    empty_elements = set(
        "base meta link hr br param img area input col \
        colgroup basefont isindex frame".split()
    )
    """Elements which can be self-closing, e.g. &lt;br /&gt;"""

    def _stringify(self, str_type):
        # turn me and my content into text
        # honor empty and non-empty elements
        join_chr = "\n" if self._newlines else ""
        if self._name is None:
            return join_chr.join(map(str_type, self._content))
        a = [f'{k}="{val}"' for k, val in self._attrs.items()]
        l = [self._name] + a
        s = f'<{" ".join(l)}>{join_chr}'
        if self._content or not (self._name.lower() in self.empty_elements):
            s += join_chr.join(map(str_type, self._content))
            s += join_chr + f"</{self._name}>"
        else:  # self-ending <tag />
            s = f'<{" ".join(l)} />{join_chr}'
        return s
