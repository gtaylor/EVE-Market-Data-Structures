"""
Utilities that are generally useful across multiple parsers.
"""
import dateutil.parser
import pytz
import datetime
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
        ).replace(microsecond=0).astimezone(UTC_TZINFO)
    except ValueError:
        # This was some kind of unrecognizable time string.
        raise ParseError("Invalid time string: %s" % time_str)

def now_dtime_in_utc():
    """
    Returns a timezone aware UTC datetime.datetime instance for the current time.

    :rtype: datetime.datetime
    """
    return datetime.datetime.utcnow().replace(tzinfo=UTC_TZINFO)

def enlighten_dtime(dtime):
    """
    Given a datetime.datetime instance that has no tzinfo, assume that it's
    UTC and adjust it as such. If tzinfo is already set, leave it be.

    :param datetime.datetime dtime: A datetime instance, potentially timezone
        aware, potentially naive.
    :rtype: datetime.datetime
    :returns: A datetime.datetime instance with tzinfo set to something other
        than None.
    """
    if not dtime.tzinfo:
        return dtime.replace(tzinfo=UTC_TZINFO)
    else:
        return dtime