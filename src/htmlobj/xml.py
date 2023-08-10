from .xhtml import XHTML


class XML(XHTML):
    """Easily generate XML.

    All tags with no contents are reduced to self-terminating tags.
    """

    newline_default_on = set()  # no tags are special

    def _stringify(self, str_type):
        # turn me and my content into text
        # honor empty and non-empty elements
        join = "\n" if self._newlines else ""
        if self._name is None:
            return join.join(map(str_type, self._content))
        a = ['%s="%s"' % i for i in self._attrs.items()]
        l = [self._name] + a
        s = "<%s>%s" % (" ".join(l), join)
        if self._content:
            s += join.join(map(str_type, self._content))
            s += join + "</%s>" % self._name
        else:
            s = "<%s />%s" % (" ".join(l), join)
        return s
