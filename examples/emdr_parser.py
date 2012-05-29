#!/usr/bin/env python
"""
This examples connect to the EMDR feed and de-serializes everything coming
down the tubes.

Requirements
------------

* pyzmq
"""
import zlib
import zmq
from emds.formats import unified

receiver_uri = 'tcp://relay-linode-atl-1.eve-emdr.com:8050'

context = zmq.Context()
subscriber = context.socket(zmq.SUB)

# Connect to the first publicly available relay.
subscriber.connect(receiver_uri)
# Disable filtering.
subscriber.setsockopt(zmq.SUBSCRIBE, "")

print("Connected to %s" % receiver_uri)

while True:
    # Receive raw market JSON strings.
    market_json = zlib.decompress(subscriber.recv())
    market_list = unified.parse_from_json(market_json)

    # If you want to see the string representation for everything coming
    # down the pipe, this is how.
    #print data

    if market_list.list_type == 'orders':
        # This is a market order message.
        print "* Recieved Orders from: %s" % market_list.order_generator

        for order in market_list:
            # You can mess with the MarketOrder in here.
            pass
    else:
        # This is a history message.
        print "* Received History from: %s" % market_list.history_generator

        for history in market_list:
            # You can mess with the MarketHistoryEntry in here.
            pass