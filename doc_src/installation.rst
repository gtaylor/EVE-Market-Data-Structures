.. _installation:

Installation
============

The only hard requirement for using EMDS is Python 2.6, though, Python 2.7
is strongly recommended. PyPy should also work just fine.

To install EMDS, you may use ``pip``::

    pip install emds

or ``easy_install``::

    easy_install emds

JSON modules
------------

EMDS can run with any of the following JSON modules:

* ujson_
* simplejson_
* Python 2.6+ built-in json_ module

The first module detected in the list above (in order) will be the one that
is used. ujson is the fastest, and simplejson is likely to be the best
combination of being up to date and very mature.

.. _ujson: http://pypi.python.org/pypi/ujson/
.. _simplejson: http://pypi.python.org/pypi/simplejson/
.. _json: http://docs.python.org/library/json.html