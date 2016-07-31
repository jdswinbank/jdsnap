import datetime

__all__ = ["DAY", "WEEK", "MONTH", "YEAR"]

DAY = datetime.timedelta(days=1)
WEEK = datetime.timedelta(weeks=1)
MONTH = datetime.timedelta(days=30)
YEAR = datetime.timedelta(days=365.25)
