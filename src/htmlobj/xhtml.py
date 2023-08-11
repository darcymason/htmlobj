from .htmlobj import HTML


class XHTML(HTML):
    """Easily generate XHTML."""

    empty_elements = set(
        "base meta link hr br param img area input col \
        colgroup basefont isindex frame".split()
    )

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
