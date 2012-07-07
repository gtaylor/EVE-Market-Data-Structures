"""
Unit tests for the data structures and other top-level modules.
"""
import unittest
import datetime
from emds.data_structures import MarketOrder, MarketOrderList, MarketHistoryList, MarketHistoryEntry, MarketItemsInRegionList

class MarketOrderListTestCase(unittest.TestCase):

    def test_order_counting(self):
        """
        Test the various order counting methods.
        """
        order_list = MarketOrderList()
        # There should be no orders so far.
        self.assertEqual(0, len(order_list))
        order_list.add_order(MarketOrder(
            order_id=2413387906,
            is_bid=True,
            region_id=10000068,
            solar_system_id=30005316,
            station_id=60011521,
            type_id=10000068,
            price=52875,
            volume_entered=10,
            volume_remaining=4,
            minimum_volume=1,
            order_issue_date=datetime.datetime.utcnow(),
            order_duration=90,
            order_range=5,
            generated_at=datetime.datetime.utcnow()
        ))
        # Added one order.
        self.assertEqual(1, len(order_list))
        # Adding a different item in the same region.
        order_list.add_order(MarketOrder(
            order_id=2413387907,
            is_bid=True,
            region_id=10000068,
            solar_system_id=30005316,
            station_id=60011521,
            type_id=10000067,
            price=52875,
            volume_entered=10,
            volume_remaining=4,
            minimum_volume=1,
            order_issue_date=datetime.datetime.utcnow(),
            order_duration=90,
            order_range=5,
            generated_at=datetime.datetime.utcnow()
        ))
        self.assertEqual(2, len(order_list))
        # Adding an item to a different region.
        order_list.add_order(MarketOrder(
            order_id=2413387907,
            is_bid=True,
            region_id=10000067,
            solar_system_id=30005316,
            station_id=60011521,
            type_id=10000067,
            price=52875,
            volume_entered=10,
            volume_remaining=4,
            minimum_volume=1,
            order_issue_date=datetime.datetime.utcnow(),
            order_duration=90,
            order_range=5,
            generated_at=datetime.datetime.utcnow()
        ))
        self.assertEqual(3, len(order_list))

        # Make sure that iterating over a MarketOrderList returns the correct
        # instance type.
        for olist in order_list:
            self.assertIsInstance(olist, MarketItemsInRegionList)

    def test_contains(self):
        """
        Tests the __contains__ method via the 'in' Python keyword.

        __contains__ lookup is based on the order ID, unlike market history,
        which is based off of type ID.
        """
        order_list = MarketOrderList()
        # Order isn't there yet, so this Order ID shouldn't be found.
        self.assertFalse(2413387906 in order_list)
        new_order = MarketOrder(
            order_id=2413387906,
            is_bid=True,
            region_id=10000068,
            solar_system_id=30005316,
            station_id=60011521,
            type_id=10000068,
            price=52875,
            volume_entered=10,
            volume_remaining=4,
            minimum_volume=1,
            order_issue_date=datetime.datetime.utcnow(),
            order_duration=90,
            order_range=5,
            generated_at=datetime.datetime.utcnow()
        )
        # Add an order to search for.
        order_list.add_order(new_order)
        # Search by order ID.
        self.assertTrue(2413387906 in order_list)
        # Use the MarketOrder instead of the order ID int.
        self.assertTrue(new_order in order_list)

class MarketHistoryListTestCase(unittest.TestCase):

    def test_entry_counting(self):
        """
        Test the various history counting counting methods.
        """
        history_list = MarketHistoryList()
        # There are no history entries yet.
        self.assertEqual(0, len(history_list))
        history_list.add_entry(MarketHistoryEntry(
            type_id=2413387906,
            region_id=10000068,
            historical_date=datetime.datetime.utcnow(),
            num_orders=5,
            low_price=5.0,
            high_price=10.5,
            average_price=7.0,
            total_quantity=200,
            generated_at=datetime.datetime.utcnow(),
        ))
        # Just added one.
        self.assertEqual(1, len(history_list))
        # Adding another item type in the same region.
        history_list.add_entry(MarketHistoryEntry(
            type_id=2413387905,
            region_id=10000068,
            historical_date=datetime.datetime.utcnow(),
            num_orders=5,
            low_price=5.0,
            high_price=10.5,
            average_price=7.0,
            total_quantity=200,
            generated_at=datetime.datetime.utcnow(),
        ))
        self.assertEqual(2, len(history_list))
        # Adding to another region.
        history_list.add_entry(MarketHistoryEntry(
            type_id=2413387905,
            region_id=10000067,
            historical_date=datetime.datetime.utcnow(),
            num_orders=5,
            low_price=5.0,
            high_price=10.5,
            average_price=7.0,
            total_quantity=200,
            generated_at=datetime.datetime.utcnow(),
        ))
        # There are now three total.
        self.assertEqual(3, len(history_list))

    def test_contains(self):
        """
        Tests the __contains__ method via the 'in' Python keyword.

        __contains__ lookup is based off of the item's type ID. This is
        different from MarketOrderList, which uses order ID.
        """
        history_list = MarketHistoryList()
        # This type ID hasn't been added yet, so this should be False.
        self.assertFalse(2413387906 in history_list)
        new_history = MarketHistoryEntry(
            type_id=2413387906,
            region_id=10000068,
            historical_date=datetime.datetime.utcnow(),
            num_orders=5,
            low_price=5.0,
            high_price=10.5,
            average_price=7.0,
            total_quantity=200,
            generated_at=datetime.datetime.utcnow(),
        )
        history_list.add_entry(new_history)
        # The entry was added, so this should succeed.
        self.assertTrue(2413387906 in history_list)
        # Use the object form.
        self.assertTrue(new_history in history_list)

class MarketHistoryListTestCase(unittest.TestCase):

    def test_entry_counting(self):
        """
        Test the various history counting counting methods.
        """
        history_list = MarketHistoryList()
        # There are no history entries yet.
        self.assertEqual(0, len(history_list))
        history_list.add_entry(MarketHistoryEntry(
            type_id=2413387906,
            region_id=10000068,
            historical_date=datetime.datetime.utcnow(),
            num_orders=5,
            low_price=5.0,
            high_price=10.5,
            average_price=7.0,
            total_quantity=200,
            generated_at=datetime.datetime.utcnow(),
        ))
        # Just added one.
        self.assertEqual(1, len(history_list))
        # Adding another item type in the same region.
        history_list.add_entry(MarketHistoryEntry(
            type_id=2413387905,
            region_id=10000068,
            historical_date=datetime.datetime.utcnow(),
            num_orders=5,
            low_price=5.0,
            high_price=10.5,
            average_price=7.0,
            total_quantity=200,
            generated_at=datetime.datetime.utcnow(),
        ))
        self.assertEqual(2, len(history_list))
        # Adding to another region.
        history_list.add_entry(MarketHistoryEntry(
            type_id=2413387905,
            region_id=10000067,
            historical_date=datetime.datetime.utcnow(),
            num_orders=5,
            low_price=5.0,
            high_price=10.5,
            average_price=7.0,
            total_quantity=200,
            generated_at=datetime.datetime.utcnow(),
        ))
        # There are now three total.
        self.assertEqual(3, len(history_list))

    def test_contains(self):
        """
        Tests the __contains__ method via the 'in' Python keyword.

        __contains__ lookup is based off of the item's type ID. This is
        different from MarketOrderList, which uses order ID.
        """
        history_list = MarketHistoryList()
        # This type ID hasn't been added yet, so this should be False.
        self.assertFalse(2413387906 in history_list)
        new_history = MarketHistoryEntry(
            type_id=2413387906,
            region_id=10000068,
            historical_date=datetime.datetime.utcnow(),
            num_orders=5,
            low_price=5.0,
            high_price=10.5,
            average_price=7.0,
            total_quantity=200,
            generated_at=datetime.datetime.utcnow(),
        )
        history_list.add_entry(new_history)
        # The entry was added, so this should succeed.
        self.assertTrue(2413387906 in history_list)
        # Use the object form.
        self.assertTrue(new_history in history_list)