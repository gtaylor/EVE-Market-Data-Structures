"""
Various parser-related exceptions.
"""
from emds.exceptions import EMDSError

class ParseError(EMDSError):
    """
    Raise this when some unrecoverable error happens while parsing serialized
    market data.
    """
    pass
