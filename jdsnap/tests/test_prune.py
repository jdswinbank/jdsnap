import datetime
import unittest

from jdsnap.archive import Archive
from jdsnap.date import YEAR, MONTH, WEEK, DAY
from jdsnap.prune import filter_archives


class TestPruning(unittest.TestCase):
    def test_single_archive(self):
        """
        We never prune a single archive.
        """
        archives = [
            Archive("prefix-2014-01-01_00-00-00", datetime.datetime(2014, 1, 1))
        ]
        intervals = [YEAR, MONTH, WEEK, DAY]
        keep = filter_archives(archives, intervals)
        self.assertEqual(len(keep), 1)

    def test_double_archive(self):
        """
        We never prune given only two archives.
        """
        archives = [
            Archive("prefix-1", datetime.datetime(2014, 1, 1)),
            Archive("prefix-2", datetime.datetime(2014, 1, 2)),
        ]
        intervals = [YEAR, MONTH, WEEK, DAY]
        keep = filter_archives(archives, intervals)
        self.assertEqual(len(keep), 2)


class ManualTestCase(unittest.TestCase):
    """
    Example list used in development.
    """

    archives = [
        Archive("prefix", datetime.datetime(2010, 1, 1)),
        Archive("prefix", datetime.datetime(2010, 7, 1)),
        Archive("prefix", datetime.datetime(2011, 1, 1)),
        Archive("prefix", datetime.datetime(2011, 2, 1)),
        Archive("prefix", datetime.datetime(2012, 1, 1)),
        Archive("prefix", datetime.datetime(2012, 5, 1)),
        Archive("prefix", datetime.datetime(2012, 5, 15)),
        Archive("prefix", datetime.datetime(2012, 5, 16)),
        Archive("prefix", datetime.datetime(2012, 6, 1)),
        Archive("prefix", datetime.datetime(2012, 7, 1)),
        Archive("prefix", datetime.datetime(2012, 7, 7)),
        Archive("prefix", datetime.datetime(2012, 7, 8)),
        Archive("prefix", datetime.datetime(2012, 7, 14)),
        Archive("prefix", datetime.datetime(2012, 7, 15)),
        Archive("prefix", datetime.datetime(2012, 7, 16)),
        Archive("prefix", datetime.datetime(2012, 7, 17)),
        Archive("prefix", datetime.datetime(2012, 7, 18)),
        Archive("prefix", datetime.datetime(2012, 7, 19)),
        Archive("prefix", datetime.datetime(2012, 7, 20)),
        Archive("prefix", datetime.datetime(2012, 7, 21)),
        Archive("prefix", datetime.datetime(2012, 7, 22)),
        Archive("prefix", datetime.datetime(2012, 7, 23)),
        Archive("prefix", datetime.datetime(2012, 7, 23)),
        Archive("prefix", datetime.datetime(2012, 7, 24)),
    ]
    intervals = [YEAR, MONTH, WEEK, DAY]
    current_date = datetime.datetime(2012, 7, 24, 22, 10, 0)

    def test_list_defaults(self):
        """
        Should reduce to 16 archives with default settings.
        """
        keep = filter_archives(
            self.archives, self.intervals, current_date=self.current_date
        )
        self.assertEqual(len(keep), 16)


class AutoTestCase(unittest.TestCase):
    INTERVALS = [YEAR, MONTH, WEEK, DAY]
    STEP = 1  # Number of days between backups
    YEARS = 10  # Number of years for which the backup system runs
    START_DATE = datetime.datetime(2016, 8, 1, 1, 1, 1)

    # Over ten years of archiving, we expect a total of 32 archives.
    #
    # - 9 annual
    # - 12 monthly
    # - 4 weekly
    # - 6 daily
    RESULT = 31

    def setUp(self):
        self.archives = []
        self.current_date = self.START_DATE

    def test_single_prune(self):
        for i in range(0, 365 * self.YEARS, self.STEP):
            self.archives.append(Archive("prefix-" + str(i), self.current_date))
            self.current_date += self.STEP * DAY
        keep = filter_archives(
            self.archives, self.INTERVALS, current_date=self.current_date
        )
        result = [x for x in self.archives if x in keep]
        self.assertEqual(len(result), self.RESULT)

    def test_continuous_prune(self):
        for i in range(0, 365 * self.YEARS, self.STEP):
            self.archives.append(Archive("prefix-" + str(i), self.current_date))
            self.current_date += self.STEP * DAY
            keep = filter_archives(
                self.archives, self.INTERVALS, current_date=self.current_date
            )
            result = [x for x in self.archives if x in keep]
        self.assertEqual(len(result), self.RESULT)
