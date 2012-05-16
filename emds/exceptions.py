"""
General market data related exceptions.
"""

class InvalidMarketOrderDataError(Exception):
    """
    Raise this when invalid market order data is passed to any of the market
    data structure's constructors or methods.
    """
    pass