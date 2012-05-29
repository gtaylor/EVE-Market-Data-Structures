from emds.data_structures import MarketOrderList, MarketHistoryList
from emds.formats import unified
from emds.formats.tests import BaseSerializationCase

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
        # This should be the non-empty region. We have the two different
        # conditions because ujson strips spaces, whereas simplejson doesn't
        # by default.
        self.assertTrue('"rows": [[' in re_encoded_list or '"rows":[[' in re_encoded_list)
        # This should be our empty region.
        self.assertTrue('"rows": []' in re_encoded_list or '"rows":[]' in re_encoded_list)

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
