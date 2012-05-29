"""
Assorted compat utilities.
"""

# A prioritized list of JSON parsers.
try:
    # ujson is the fastest, and is the default for EMDR.
    import ujson as json
except ImportError:
    try:
        # The external simplejson package is faster for certain versions of
        # Python, and almost always more up to date.
        import simplejson as json
    except ImportError:
        # The default built-in simplejson for Python 2.6+.
        import json