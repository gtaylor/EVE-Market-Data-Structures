import datetime
import pytz
from emds.compat import json
from emds.data_structures import MarketOrderList, MarketHistoryList
from emds.formats import unified
from emds.formats.common_utils import enlighten_dtime, UTC_TZINFO, parse_datetime
from emds.formats.tests import BaseSerializationCase
from emds.formats.unified.unified_utils import gen_iso_datetime_str

class UtilsTests(BaseSerializationCase):
    """
    Tests some of the stuff in unified_utils.
    """

    def test_gen_iso_datetime_str(self):
        """
        Make sure gen_iso_datetime_str() is behaving correctly.
        """

        est = pytz.timezone("EST")
        some_date = datetime.datetime(
            year=1985, month=11, day=15,
            hour=6, minute=0,
            tzinfo=est)

        # Generate an ISO datetime string, and parse it. This will convert it
        # from EST to UTC.
        parsed_dtime = parse_datetime(gen_iso_datetime_str(some_date))
        # EST is -5, so the hour should now be 11.
        self.assertEqual(parsed_dtime.hour, 11)
        # tzinfo will be UTC, since we converted it upon parsing.
        self.assertIs(parsed_dtime.tzinfo, UTC_TZINFO)

    def test_enlighten_dtime(self):
        """
        Makes sure our datetime 'enlightening' is behaving correctly.
        """

        est = pytz.timezone("EST")
        aware_dtime = datetime.datetime(
            year=1985, month=11, day=15,
            hour=6, minute=0,
            tzinfo=est)

        enlightened_dtime = enlighten_dtime(aware_dtime)
        # The tzinfo should be untouched.
        self.assertIs(aware_dtime.tzinfo, enlightened_dtime.tzinfo)

        # This is a naive object, but has UTC values for hour.
        utcnow = datetime.datetime.now()
        # No tzinfo was present, so that is replaced. hour should be the same.
        enlightened_utcnow = enlighten_dtime(utcnow)
        self.assertEqual(enlightened_utcnow.hour, utcnow.hour)
        self.assertIs(enlightened_utcnow.tzinfo, UTC_TZINFO)


class UnifiedSerializationTests(BaseSerializationCase):
    """
    Tests for serializing and de-serializing orders in Unified format.
    """

    def test_order_serialization(self):
        # Encode the sample order list.
        encoded_orderlist = unified.encode_to_json(self.order_list)
        # Should return a string JSON representation.
        self.assertIsInstance(encoded_orderlist, basestring)
        # De-code the JSON to instantiate a list of MarketOrder instances that
        # should be identical to self.orderlist.
        decoded_list = unified.parse_from_json(encoded_orderlist)
        self.assertIsInstance(decoded_list, MarketOrderList)
        re_encoded_list = unified.encode_to_json(decoded_list)
        # Re-encode the decoded orderlist. Match the two encoded strings. They
        # should still be the same.
        self.assertEqual(
            encoded_orderlist,
            re_encoded_list,
            "Encoded and re-encoded orders don't match."
        )

    def test_history_serialization(self):
        # Encode the sample history instance.
        encoded_history = unified.encode_to_json(self.history)
        # Should return a string JSON representation.
        self.assertIsInstance(encoded_history, basestring)
        # De-code the JSON to instantiate a MarketHistoryList instances that
        # should be identical to self.orderlist.
        decoded_list = unified.parse_from_json(encoded_history)
        self.assertIsInstance(decoded_list, MarketHistoryList)
        re_encoded_history = unified.encode_to_json(decoded_list)
        # Re-encode the decoded history. Match the two encoded strings. They
        # should still be the same.
        self.assertEqual(
            encoded_history,
            re_encoded_history,
            "Encoded and re-encoded history don't match."
        )

    def test_simple_order_deserialization(self):
        """
        Test a basic case of deserializing an order message.
        """
        data = """
            {
              "resultType" : "orders",
              "version" : "0.1alpha",
              "uploadKeys" : [
                { "name" : "emk", "key" : "abc" },
                { "name" : "ec" , "key" : "def" }
              ],
              "generator" : { "name" : "Yapeal", "version" : "11.335.1737" },
              "currentTime" : "2011-10-22T15:46:00+00:00",
              "columns" : ["price","volRemaining","range","orderID","volEntered","minVolume","bid","issueDate","duration","stationID","solarSystemID"],
              "rowsets" : [
                {
                  "generatedAt" : "2011-10-22T15:43:00+00:00",
                  "regionID" : 10000065,
                  "typeID" : 11134,
                  "rows" : [
                    [8999,1,32767,2363806077,1,1,false,"2011-12-03T08:10:59+00:00",90,60008692,30005038],
                    [11499.99,10,32767,2363915657,10,1,false,"2011-12-03T10:53:26+00:00",90,60006970,null],
                    [11500,48,32767,2363413004,50,1,false,"2011-12-02T22:44:01+00:00",90,60006967,30005039]
                  ]
                },
                {
                  "generatedAt" : "2011-10-22T15:42:00+00:00",
                  "regionID" : null,
                  "typeID" : 11135,
                  "rows" : [
                    [8999,1,32767,2363806077,1,1,false,"2011-12-03T08:10:59+00:00",90,60008692,30005038],
                    [11499.99,10,32767,2363915657,10,1,false,"2011-12-03T10:53:26+00:00",90,60006970,null],
                    [11500,48,32767,2363413004,50,1,false,"2011-12-02T22:44:01+00:00",90,60006967,30005039]
                  ]
                }
              ]
            }
        """
        decoded_list = unified.parse_from_json(data)
        self.assertIsInstance(decoded_list, MarketOrderList)

    def test_orderless_region(self):
        """
        Tests deserializing a region that has no orders.
        """
        data = """
            {
              "resultType" : "orders",
              "version" : "0.1alpha",
              "uploadKeys" : [
                { "name" : "emk", "key" : "abc" },
                { "name" : "ec" , "key" : "def" }
              ],
              "generator" : { "name" : "Yapeal", "version" : "11.335.1737" },
              "currentTime" : "2011-10-22T15:46:00+00:00",
              "columns" : ["price","volRemaining","range","orderID","volEntered","minVolume","bid","issueDate","duration","stationID","solarSystemID"],
              "rowsets" : [
                {
                  "generatedAt" : "2011-10-22T15:43:00+00:00",
                  "regionID" : 10000065,
                  "typeID" : 11134,
                  "rows" : [
                    [8999,1,32767,2363806077,1,1,false,"2011-12-03T08:10:59+00:00",90,60008692,30005038],
                    [11499.99,10,32767,2363915657,10,1,false,"2011-12-03T10:53:26+00:00",90,60006970,null],
                    [11500,48,32767,2363413004,50,1,false,"2011-12-02T22:44:01+00:00",90,60006967,30005039]
                  ]
                },
                {
                  "generatedAt" : "2011-10-22T15:42:00+00:00",
                  "regionID" : 10000066,
                  "typeID" : 11135,
                  "rows" : []
                }
              ]
            }
        """
        # Parse JSON, spit out an order list.
        decoded_list = unified.parse_from_json(data)
        self.assertIsInstance(decoded_list, MarketOrderList)
        # There should be two item+region combos.
        self.assertEqual(len(decoded_list._orders.keys()), 2)
        # Now make sure there are three.
        self.assertEqual(len(decoded_list), 3)
        # These are regionID_itemID. Make sure the keys are set correctly.
        self.assertItemsEqual(
            ['10000065_11134', '10000066_11135'],
            decoded_list._orders.keys()
        )

        # Re-encode for JSON and do some basic checks for sanity.
        re_encoded_list = unified.encode_to_json(decoded_list)
        # We're back to a dict. Check to make sure our custom JSON encoder
        # didn't butcher the entry-less region (10000066).
        re_decoded_list = json.loads(re_encoded_list)
        self.assertEqual(2, len(re_decoded_list['rowsets']))

        for rowset in re_decoded_list['rowsets']:
            # We only want to check the entry rowset with type 11135.
            if rowset['typeID'] != 11135:
                continue

            # There should always be one rowset, even if it ends up being empty.
            first_rowset = re_decoded_list['rowsets'][0]
            # Check for the empty rowsets with all data intact.
            self.assertListEqual(rowset['rows'], [])
            self.assertTrue(first_rowset.has_key('generatedAt'))
            self.assertTrue(first_rowset.has_key('regionID'))
            self.assertTrue(first_rowset.has_key('typeID'))

    def test_simple_history_deserialization(self):
        """
        Test a basic case of deserializing a history message.
        """
        data = """
            {
              "resultType" : "history",
              "version" : "0.1alpha",
              "uploadKeys" : [
                { "name" : "emk", "key" : "abc" },
                { "name" : "ec" , "key" : "def" }
              ],
              "generator" : { "name" : "Yapeal", "version" : "11.335.1737" },
              "currentTime" : "2011-10-22T15:46:00+00:00",
              "columns" : ["date","orders","quantity","low","high","average"],
              "rowsets" : [
                {
                  "generatedAt" : "2011-10-22T15:42:00+00:00",
                  "regionID" : 10000065,
                  "typeID" : 11134,
                  "rows" : [
                    ["2011-12-03T00:00:00+00:00",40,40,1999,499999.99,35223.50],
                    ["2011-12-02T00:00:00+00:00",83,252,9999,11550,11550]
                  ]
                }
              ]
            }
        """
        decoded_list = unified.parse_from_json(data)
        self.assertIsInstance(decoded_list, MarketHistoryList)
        self.assertEqual(len(decoded_list), 2)

    def test_empty_history_reencoding(self):
        """
        Uses a repeated encoding-decoding cycle to determine whether we're
        handling empty rows within rowsets correctly.
        """
        data = """
            {
              "resultType" : "history",
              "version" : "0.1alpha",
              "uploadKeys" : [
                { "name" : "emk", "key" : "abc" },
                { "name" : "ec" , "key" : "def" }
              ],
              "generator" : { "name" : "Yapeal", "version" : "11.335.1737" },
              "currentTime" : "2011-10-22T15:46:00+00:00",
              "columns" : ["date","orders","quantity","low","high","average"],
              "rowsets" : [
                {
                  "generatedAt" : "2011-10-22T15:42:00+00:00",
                  "regionID" : 10000065,
                  "typeID" : 11134,
                  "rows" : []
                }
              ]
            }
        """
        decoded_list = unified.parse_from_json(data)
        re_encoded_list = unified.encode_to_json(decoded_list)
        re_decoded_list = json.loads(re_encoded_list)
        # There should always be one rowset, even if it ends up being empty.
        self.assertEqual(1, len(re_decoded_list['rowsets']))
        first_rowset = re_decoded_list['rowsets'][0]
        # Check for the empty rowsets with all data intact.
        self.assertListEqual(first_rowset['rows'], [])
        self.assertTrue(first_rowset.has_key('generatedAt'))
        self.assertTrue(first_rowset.has_key('regionID'))
        self.assertTrue(first_rowset.has_key('typeID'))