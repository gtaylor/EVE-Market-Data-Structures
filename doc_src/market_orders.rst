.. _market-orders:

Market Orders
=============

Market data is comprised of *orders* and *history*. Orders represent individual
buy/sell orders, and history entries are points of data on the cost and
availability of a given item. In both cases, the data structures are similar
in that there is a container class (
:py:class:`MarketOrderList <emds.data_structures.MarketOrderList>` and
:py:class:`MarketHistoryList <emds.data_structures.MarketHistoryList>`)
and a unit of data (
:py:class:`MarketOrder <emds.data_structures.MarketOrder>` and
:py:class:`MarketHistoryEntry <emds.data_structures.MarketHistoryEntry>`).

While the container classes are not Python lists, they implement some
convenience methods to add, query, and work with the data.