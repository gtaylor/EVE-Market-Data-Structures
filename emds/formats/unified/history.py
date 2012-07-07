"""
Parser for the Unified uploader format market history.
"""
import logging
import datetime
from emds.compat import json
from emds.data_structures import MarketHistoryList, MarketHistoryEntry
from emds.formats.common_utils import parse_datetime, now_dtime_in_utc
from emds.formats.unified.unified_utils import _columns_to_kwargs, gen_iso_datetime_str

logger = logging.getLogger(__name__)

# This is the standard list of columns to return data in for encoding.
STANDARD_ENCODED_COLUMNS = [
    'date', 'orders', 'quantity', 'low', 'high', 'average',
]

# This is a dict that acts like a mapping table, with the key being the
# Unified uploader format field name, and the value being the corresponding
# kwarg to the MarketOrder class. This lets us instantiate the class directly
# from the data.
SPEC_TO_KWARG_CONVERSION = {
    'date': 'historical_date',
    'orders': 'num_orders',
    'low': 'low_price',
    'high': 'high_price',
    'average': 'average_price',
    'quantity': 'total_quantity',
}

def parse_from_dict(json_dict):
    """
    Given a Unified Uploader message, parse the contents and return a
    MarketHistoryList instance.

    :param dict json_dict: A Unified Uploader message as a dict.
    :rtype: MarketOrderList
    :returns: An instance of MarketOrderList, containing the orders
        within.
    """
    history_columns = json_dict['columns']

    history_list = MarketHistoryList(
        upload_keys=json_dict['uploadKeys'],
        history_generator=json_dict['generator'],
    )

    for rowset in json_dict['rowsets']:
        generated_at = parse_datetime(rowset['generatedAt'])
        region_id = rowset['regionID']
        type_id = rowset['typeID']
        history_list.set_empty_region(region_id, type_id, generated_at)

        for row in rowset['rows']:
            history_kwargs = _columns_to_kwargs(
                SPEC_TO_KWARG_CONVERSION, history_columns, row)
            historical_date = parse_datetime(history_kwargs['historical_date'])

            history_kwargs.update({
                'type_id': type_id,
                'region_id': region_id,
                'historical_date': historical_date,
                'generated_at': generated_at,
            })

            history_list.add_entry(MarketHistoryEntry(**history_kwargs))

    return history_list

def encode_to_json(history_list):
    """
    Encodes this MarketHistoryList instance to a JSON string.

    :param MarketHistoryList history_list: The history instance to serialize.
    :rtype: str
    """
    rowsets = []
    for items_in_region_list in history_list._history.values():
        region_id = items_in_region_list.region_id
        type_id = items_in_region_list.type_id
        generated_at = gen_iso_datetime_str(items_in_region_list.generated_at)

        rows = []
        for entry in items_in_region_list.entries:
            historical_date = gen_iso_datetime_str(entry.historical_date)

            # The order in which these values are added is crucial. It must
            # match STANDARD_ENCODED_COLUMNS.
            rows.append([
                historical_date,
                entry.num_orders,
                entry.total_quantity,
                entry.low_price,
                entry.high_price,
                entry.average_price,
            ])

        rowsets.append(dict(
            generatedAt = generated_at,
            regionID = region_id,
            typeID = type_id,
            rows = rows,
        ))

    json_dict = {
        'resultType': 'history',
        'version': '0.1',
        'uploadKeys': history_list.upload_keys,
        'generator': history_list.history_generator,
        'currentTime': gen_iso_datetime_str(now_dtime_in_utc()),
        # This must match the order of the values in the row assembling portion
        # above this.
        'columns': STANDARD_ENCODED_COLUMNS,
        'rowsets': rowsets,
    }

    return json.dumps(json_dict)