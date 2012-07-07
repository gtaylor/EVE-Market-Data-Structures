"""
General market data related exceptions.
"""

class EMDSError(Exception):
    """
    Top-level parent class, to allow people to catch for error handling.
    """
    pass


class InvalidMarketOrderDataError(EMDSError):
    """
    Raise this when invalid market order data is passed to any of the market
    data structure's constructors or methods.
    """
    pass


class ItemAlreadyPresentError(EMDSError):
    """
    Raised when MarketOrderList.set_item_missing_in_region is called, but
    the item is already present in the region.
    """
    pass


class NaiveDatetimeError(EMDSError):
    """
    Raised when a naive datetime.datetime object is encountered, where a
    tzinfo aware one is required.
    """
    pass