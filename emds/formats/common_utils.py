"""
Utilities that are generally useful across multiple parsers.
"""
import dateutil.parser
import pytz
from emds.formats.exceptions import ParseError

UTC_TZINFO = pytz.timezone("UTC")

def parse_datetime(time_str):
    """
    Wraps dateutil's parser function to set an explicit UTC timezone, and
    to make sure microseconds are 0. Unified Uploader format and EMK format
    bother don't use microseconds at all.

    :param str time_str: The date/time str to parse.
    :rtype: datetime.datetime
    :returns: A parsed, UTC datetime.
    """
    try:
        return dateutil.parser.parse(
            time_str
        ).replace(
            tzinfo=UTC_TZINFO,
            microsecond=0
        )
    except ValueError:
        # This was some kind of unrecognizable time string.
        raise ParseError("Invalid time string: %s" % time_str)