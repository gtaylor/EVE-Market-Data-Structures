.. _formats:

.. include:: global.txt

Serializing to/from Unified Format
==================================

EMDS currently only supports `Unified Uploader Data Interchange Format`_ (UUDIF).
While there are other "proprietary" formats that are geared towards individual
market sites, the goal of EMDS is to offer a set of data structures and
serializers for the community-backed formats.

In the spirit of supporting the community-drafted and backed formats
(currently UUDIF), this is all we'll support until/unless a new format comes
along, is vetted by the community, and receives traction.

Dumping order and history lists to UUDIF
----------------------------------------

Regardless of whether you are dealing with a
:py:class:`MarketOrderList <emds.data_structures.MarketOrderList>`
or a
:py:class:`MarketHistoryList <emds.data_structures.MarketHistoryList>`
, serializing to UUDIF works the same::

    from emds.formats import unified

    order_list = MarketOrderList()
    # Add your orders here.
    # ...

    # This spits out the JSON UUDIF message string. encode_to_json() accepts
    # MarketOrderList and MarketHistoryList instances.
    encoded_order_list = unified.encode_to_json(order_list)

Parsing UUDIF order and history messages
----------------------------------------

Parsing a UUDIF message results in either a
:py:class:`MarketOrderList <emds.data_structures.MarketOrderList>`
or a
:py:class:`MarketHistoryList <emds.data_structures.MarketHistoryList>`
instance being returned::

    from emds.formats import unified

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
    # This spits out a MarketOrderList instance that is ready to be
    # iterated over.
    order_list = unified.parse_from_json(data)