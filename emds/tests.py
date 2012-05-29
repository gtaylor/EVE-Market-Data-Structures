"""
Unit tests for the data structures and other top-level modules.
"""
import unittest
import datetime
from emds.data_structures import MarketOrder, MarketOrderList, MarketHistoryList, MarketHistoryEntry

class MarketOrderListTestCase(unittest.TestCase):

    def test_order_counting(self):
        """
        Test the various counting order counting methods.
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

class MarketHistoryListTestCase(unittest.TestCase):

    def test_entry_counting(self):
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