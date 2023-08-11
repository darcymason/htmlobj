htmlobj
=======

`htmlobj` allows you to easily create complex HTML (or XML, xHTML) using nothing but Python code.  It is an alternative to using templates in web frameworks, which usually have their own language syntax.

## Example:

``` py
from htmlobj import HTML

h = HTML("html")
h.head.title("My Page")  # can chain tags if only 1 subitem
with h.body:  # use `with` for multiple subitems
    h.p.u("Paragraph 1 underlined")
    with h.p("Paragraph 2 ", class_="p2"):  # add attributes too
        h.b("bold")  
        h.text(", not bold") # add additional text
print(h)
```

Which outputs:

```html
<html>
<head>
<title>My Page</title>
</head>
<body>
<p><u>Paragraph 1 underlined</u></p>
<p class="p2">Paragraph 2 <b>bold</b>, not bold</p>
</body>
</html>
```

Note that the `class_` attribute has a trailing underscore because `class` is a Python keyword.


## New Features

`htmlobj` is a re-packaging of [html3](https://github.com/pavelliavonau/html3/),  with further Python 3 modernization and additional functionality added.

One added feature is creating an `htmlobj.HTML` instance from existing html, either as a string (`HTML.from_html`), or from a url (`HTML.from_url`):

``` py
h = HTML.from_url("https://example.com/")
```

This will often be used in combination with another new feature, `HTML.codify`, to *generate Python code* using `htmlobj`, for you.  Start with a page that is similar to what you want to create, then modify as needed, e.g. to programatically fill in data for that page.

``` py
print(h.codify())
```

which gives output like:

```
h = HTML()
with h.html:
    with h.head:
        h.title("Example Domain")
        h.meta(charset="utf-8")
        h.meta(http-equiv="Content-type", content="text/html; charset=utf-8")
...
```

You can then copy this output as a starting point for you own code, to make a webpage similar to the one passed to `from_url`.

Note:  you can also achieve a `from_url` / `codify` combination from the command line by running `htmlobj.html_parser` with `python -m`:

```
python -m htmlobj.html_parser https://example.com > my_code.py
```


## Installation

```
pip install htmlobj
```


## Next Steps

See [Getting Started](https://darcymason.github.io/htmlobj/getting_started/) for more examples and detailed usage information.

