import datetime

__all__ = ["DAY", "WEEK", "MONTH", "YEAR", "DEFAULT_DATEFMT", "date_from_name"]

DAY = datetime.timedelta(days=1)
WEEK = datetime.timedelta(weeks=1)
MONTH = datetime.timedelta(days=30)
YEAR = datetime.timedelta(days=365.25)

DEFAULT_DATEFMT = "%Y-%m-%d_%H-%M-%S"

def date_from_name(archive_name, prefix, datefmt=DEFAULT_DATEFMT):
    """
    Parse date from archive name.

    Given an archive named (prefix)-(date), extract and return the date as a
    (timezone unencumbered) datetime.
    """
    return datetime.datetime.strptime(archive_name[len(prefix):], datefmt)
