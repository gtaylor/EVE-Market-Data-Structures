.. _quickstart:

Quickstart
==========

Market data is comprised of *orders* and *history*. Orders represent individual
buy/sell orders, and history entries are points of data on the cost and
availability of a given item.

In both cases, the data structures are similar
in that there is a container class (
:py:class:`MarketOrderList <emds.data_structures.MarketOrderList>` and
:py:class:`MarketHistoryList <emds.data_structures.MarketHistoryList>`),
an item+region grouper class (
:py:class:`MarketItemsInRegionList <emds.data_structures.MarketItemsInRegionList>` and
:py:class:`HistoryItemsInRegionList <emds.data_structures.HistoryItemsInRegionList>`),
and a unit of data (
:py:class:`MarketOrder <emds.data_structures.MarketOrder>` and
:py:class:`MarketHistoryEntry <emds.data_structures.MarketHistoryEntry>`).

The two top-level classes are best thought of as containers for any number
of orders or history entries.
:py:class:`MarketOrderList <emds.data_structures.MarketOrderList>`
and :py:class:`MarketHistoryList <emds.data_structures.MarketHistoryList>`
contain nothing but some basic info about where the data came from, along
with some convenience methods for manipulating and retrieving said data.

Beneath the top level List classes are two classes
(:py:class:`MarketItemsInRegionList <emds.data_structures.MarketItemsInRegionList>` and
:py:class:`HistoryItemsInRegionList <emds.data_structures.HistoryItemsInRegionList>`),
that group orders together
based on Item ID and Region ID. For example, all orders of Type ID 12345
in Region ID 6789 are grouped together, much like they are in the in-game
market browser. Within these two classes are the individual order and
history instances (
:py:class:`MarketOrderList <emds.data_structures.MarketOrderList>` and
:py:class:`MarketHistoryList <emds.data_structures.MarketHistoryList>`).

The hierarchy ends up looking like this:

* :py:class:`MarketOrderList <emds.data_structures.MarketOrderList>`

  * :py:class:`MarketItemsInRegionList <emds.data_structures.MarketItemsInRegionList>`

    * :py:class:`MarketOrder <emds.data_structures.MarketOrder>`


* :py:class:`MarketHistoryList <emds.data_structures.MarketHistoryList>`

  * :py:class:`HistoryItemsInRegionList <emds.data_structures.HistoryItemsInRegionList>`

    * :py:class:`MarketHistoryList <emds.data_structures.MarketHistoryList>`

The importance of timezone awareness
------------------------------------

EVE Online deals with nothing but UTC times. Python's default
:py:meth:`datetime.datetime.now` and :py:meth:`datetime.datetime.utcnow`
return objects without ``tzinfo`` set, which means that the objects are
considered "naive", with regards to what timezone they are in.

EMDS requires that all times being passed into the data structures have
a timezone specified via the ``tzinfo`` attribute. Simple using
``now()`` or ``utcnow()`` will result in exceptions being raised, so don't do
that.

If you're simply wanting to get the current time in UTC, you can use our
helper function::

    >>> from emds.common_utils import now_dtime_in_utc
    >>> now_dtime_in_utc()
    datetime.datetime(...)

If you have an existing naive datetime.datetime (has no ``tzinfo`` value)
whose hour value is set to represent UTC, you can use pytz to "enlighten"
the naive datetime instance::

    >>> import pytz; import datetime
    >>> utc = pytz.timezone("UTC")
    >>> naive_utcnow = datetime.datetime.utcnow()
    >>> enlightend_utcnow = naive_utcnow.replace(tzinfo=utc)

This does no conversion of the ``hour`` value, it simply replaces the ``None``
tzinfo value with the UTC tzinfo object. The datetime object now unambiguously
says it is in UTC, whereas before, it was a naive object that just had an
hour value of some sort in an un-specified timezone.

.. note:: You probably don't want to ever bother with datetime.datetime.now().
    This returns local time, which is just not something you want to get
    involved with.

Creating/populating market order lists
--------------------------------------

Creating and populating market order lists is as simple as instantiating a
:py:class:`MarketOrderList <emds.data_structures.MarketOrderList>` object
and using its :py:meth:`add_order <emds.data_structures.MarketOrderList.add_order>`
method.

.. code-block:: python

    from emds.data_structures import MarketOrder, MarketOrderList
    from emds.common_utils import now_dtime_in_utc

    order_list = MarketOrderList()
    order_list.add_order(MarketOrder(
        order_id=2413387906,
        is_bid=True,
        region_id=10000123,
        solar_system_id=30005316,
        station_id=60011521,
        type_id=2413387906,
        price=52875,
        volume_entered=10,
        volume_remaining=4,
        minimum_volume=1,
        order_issue_date=now_dtime_in_utc(),
        order_duration=90,
        order_range=5,
        generated_at=now_dtime_in_utc()
    ))

Behind the scenes, this is creating a
:py:class:`MarketItemsInRegionList <emds.data_structures.MarketItemsInRegionList>`
instance that will contain all orders with Type ID ``2413387906`` and Region ID
``10000123``. Orders are grouped based on their Type and Region IDs.

Iterating over market order lists
---------------------------------

Assuming you have a :py:class:`MarketOrderList <emds.data_structures.MarketOrderList>`
instance you want to pull order data from, there are two primary ways to
do so.

If you are only concerned with pulling all orders out, without caring whether
certain regions+item combos are empty, simply use the
:py:meth:`MarketOrderList.get_all_orders_ungrouped <emds.data_structures.MarketOrderList.get_all_orders_ungrouped>`
generator::

    order_list = MarketOrderList()
    # Add your orders here.
    # ...
    for order in order_list.get_all_orders_ungrouped():
        # order is a MarketOrder instance.
        print order.order_id, order.type_id, order.region_id

If you need to know that certain item+region combinations held no orders,
you'll need to iterate through the orders in all of the MarketOrderList's
:py:class:`MarketItemsInRegionList <emds.data_structures.MarketItemsInRegionList>`
instances::

    order_list = MarketOrderList()
    # Add your orders here.
    # ...
    for ir_group in order_list.get_all_order_groups():
        # ir_group is a MarketItemsInRegionList, which contains orders
        # You can check to see if there are any orders
        num_orders = len(ir_group)
        # If it's 0, you could mark it as such in your application.
        for order in ir_group:
            # order is a MarketOrder instance.
            print order.order_id, order.type_id, order.region_id


Creating/populating market history lists
----------------------------------------

Creating and populating market order lists is as simple as instantiating a
:py:class:`MarketHistoryList <emds.data_structures.MarketHistoryList>` object
and using its :py:meth:`add_entry <emds.data_structures.MarketHistoryList.add_entry>`
method.

.. code-block:: python

    from emds.data_structures import MarketHistoryEntry, MarketHistoryList
    from emds.common_utils import now_dtime_in_utc

    history_list = MarketHistoryList()
    history_list.add_entry(MarketHistoryEntry(
        type_id=2413387906,
        region_id=10000068,
        historical_date=now_dtime_in_utc(),
        num_orders=5,
        low_price=5.0,
        high_price=10.5,
        average_price=7.0,
        total_quantity=200,
        generated_at=now_dtime_in_utc(),
    ))

Behind the scenes, this is creating a
:py:class:`HistoryItemsInRegionList <emds.data_structures.HistoryItemsInRegionList>`
instance that will contain all entries with Type ID ``2413387906`` and Region ID
``10000068``. History entries are grouped based on their Type and Region IDs.

Iterating over market history lists
-----------------------------------

Assuming you have a :py:class:`MarketHistoryList <emds.data_structures.MarketHistoryList>`
instance you want to pull history data from, there are two primary ways to
do so.

If you are only concerned with pulling all history entries out, without caring
whether certain regions+item combos lack data, simply use the
:py:meth:`MarketHistoryList.get_all_entries_ungrouped <emds.data_structures.MarketHistoryList.get_all_entries_ungrouped>`
generator::

    history_list = MarketHistoryList()
    # Add your history entries here.
    # ...
    for entry in history_list.get_all_entries_ungrouped():
        # entry is a MarketHistoryEntry instance.
        print entry.type_id, entry.region_id, entry.average_price

If you need to know that certain item+region combinations held no history data,
you'll need to iterate through the entries in all of the MarketHistoryList's
:py:class:`HistoryItemsInRegionList <emds.data_structures.HistoryItemsInRegionList>`
instances::

    history_list = MarketHistoryList()
    # Add your history entries here.
    # ...
    for ir_group in history_list.get_all_entries_grouped():
        # ir_group is a HistoryItemsInRegion, which contains history entries
        # You can check to see if there are any entries
        num_entries = len(ir_group)
        # If it's 0, you could mark it as such in your application.
        for entry in ir_group:
            # entry is a MarketHistoryEntry instance.
            print entry.type_id, entry.region_id, entry.average_price