"""
Various parser-related exceptions.
"""

class ParseError(Exception):
    """
    Raise this when some unrecoverable error happens while parsing serialized
    market data.
    """
    pass
