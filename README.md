htmlobj
=======

Python object to easily create complex html

## Example:

```python
from htmlobj import HTML

```python
from htmlobj import HTML

h = HTML("html")
h.head.title("My Page")  # chain tags if only 1 subitem
with h.body:  # use `with` for multiple subitems
    h.p.u("Paragraph 1 underlined")
    h.p.b("Paragraph 2 bold")

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
<p><b>Paragraph 2 bold</b></p>
</body>
</html>
```

## Installation

```
pip install htmlobj
```

See [Getting Started](docs/getting_started.md) for more examples and detailed usage information.

## Development

To install the development version of htmlobj:

    git clone https://github.com/darcymason/htmlobj

    # create a virtual environment and install all required dev dependencies
    cd htmlobj
    make devenv

To run the tests, use `make tests` or `make coverage` for a complete report.

To generate the documentation pages use `make docs` or `make serve-docs` for
starting a webserver with the generated documentation
