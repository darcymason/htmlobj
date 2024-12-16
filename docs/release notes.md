# Release Notes

## v1.30.0

* Fixed bug in Python keyword check
* Added py.typed
* Fixed bug in attribute values if `escape` False
* Increased test coverage


## v1.20.0

* Added `HTML.from_html` and `HTML.from_url` methods to create an `HTML` instance from an existing HTML source
* Added HTML.codify method to produce Python code from an `HTML` instance. In combination with one of the `HTML.from_` methods, can make Python code to reproduce existing HTML similar to what you need.
* Added ability to handle 'blank' attrs like 'nowrap' using e.g. `nowrap=None` attribute.
* Added `class_` as alternative to `klass` in avoiding Python's `class` keyword


## Release notes from `html3` and `html` libaries

- 1.18 Fixed support of python 3.8
- 1.17 First release of html3
- 1.16 detect and raise a more useful error when some WSGI frameworks
  attempt to call HTML.read(). Also added ability to add new content using
  the += operator.
- 1.15 fix Python 3 compatibility (unit tests)
- 1.14 added plain XML support
- 1.13 allow adding (X)HTML instances (tags) as new document content
- 1.12 fix handling of XHTML empty tags when generating unicode
  output (thanks Carsten Eggers)
- 1.11 remove setuptools dependency
- 1.10 support plain ol' distutils again
- 1.9 added unicode support for Python 2.x
- 1.8 added Python 3 compatibility
- 1.7 added Python 2.5 compatibility and escape argument to tag
  construction
- 1.6 added .raw_text() and and WSGI compatibility
- 1.5 added XHTML support
- 1.3 added more documentation, more tests
- 1.2 added special-case klass / class attribute
- 1.1 added escaping control
- 1.0 was the initial release