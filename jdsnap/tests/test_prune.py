import datetime
import unittest

from jdsnap import Archive, filter_archives, YEAR, MONTH, WEEK, DAY

class TestPruning(unittest.TestCase):
    def test_single_archive(self):
        """
        We never prune a single archive.
        """
        archives = [Archive("prefix-2014-01-01_00-00-00",
                            datetime.datetime(2014, 1, 1))]
        intervals = [YEAR, MONTH, WEEK, DAY]
        keep = filter_archives(archives, intervals)
        self.assertEqual(len(keep), 1)

    def test_double_archive(self):
        """
        We never prune given only two archives.
        """
        archives = [Archive("prefix-1", datetime.datetime(2014, 1, 1)),
                    Archive("prefix-2", datetime.datetime(2014, 1, 2))]
        intervals = [YEAR, MONTH, WEEK, DAY]
        keep = filter_archives(archives, intervals)
        self.assertEqual(len(keep), 2)

class ManualTestCase(unittest.TestCase):
    """
    Example list used in development.
    """
    archives = [Archive("prefix", datetime.datetime(2010, 1, 1)),
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
                Archive("prefix", datetime.datetime(2012, 7, 24))]
    intervals = [YEAR, MONTH, WEEK, DAY]
    current_date = datetime.datetime(2012, 7, 24, 22, 10, 0)

    def test_list_defaults(self):
        """
        Should reduce to 12 archives with default settings.
        """
        keep = filter_archives(self.archives, self.intervals,
                               current_date=self.current_date)
        self.assertEqual(len(keep), 12)

    def test_list_recent(self):
        """
        Store the last week's worth of data.
        """
        intervals = [YEAR, MONTH, WEEK, DAY]
        keep = filter_archives(self.archives, self.intervals,
                               keep_all_within=WEEK,
                               current_date=self.current_date)
        self.assertEqual(len(keep), 17)
