"""
Utilities that are generally useful throughout the whole package.
"""
import pytz
import datetime
from emds.exceptions import NaiveDatetimeError

UTC_TZINFO = pytz.timezone("UTC")

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

def check_for_naive_dtime(dtime):
    """
    Given a datetime.datetime instance, check to see if it is naive. If it is
    raise an exception. If not, return the datetime instance untouched.

    :rtype: datetime.datetime
    :returns: The datetime.datetime instance that was passed, unmodified.
    :raises: :py:exc:`emds.exceptions.NaiveDatetimeError` if the datetime
        instance is naive.
    """
    if not dtime.tzinfo:
        raise NaiveDatetimeError(
            "Naive datetime.datetime encountered, when a timezone aware one "
            "is required (replace tzinfo on the datetime)."
        )
    else:
        return dtime