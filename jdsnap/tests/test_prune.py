import datetime
import unittest

from jdsnap import filter_archive_list, YEAR, MONTH, WEEK, DAY

class TestPruning(unittest.TestCase):
    def test_single_archive(self):
        """
        We never prune a single archive.
        """
        archives = ["prefix-2014-01-01_00-00-00"]
        intervals = [YEAR, MONTH, WEEK, DAY]
        keep = filter_archive_list(archives, intervals, "prefix-")
        self.assertEqual(len(keep), 1)

    def test_double_archive(self):
        """
        We never prune given only two archives.
        """
        archives = ["prefix-2014-01-01_00-00-00", "prefix-2014-01-02_00-00-00"]
        intervals = [YEAR, MONTH, WEEK, DAY]
        keep = filter_archive_list(archives, intervals, "prefix-")
        self.assertEqual(len(keep), 2)

class ManualTestCase(unittest.TestCase):
    """
    Example list used in development.
    """
    archives = ['prefix-2010-01-01_00-00-00',
                'prefix-2010-07-01_00-00-00',
                'prefix-2011-01-01_00-00-00',
                'prefix-2011-12-01_00-00-00',
                'prefix-2012-01-01_00-00-00',
                'prefix-2012-05-01_00-00-00',
                'prefix-2012-05-15_00-00-00',
                'prefix-2012-05-16_00-00-00',
                'prefix-2012-06-01_00-00-00',
                'prefix-2012-07-01_00-00-00',
                'prefix-2012-07-07_00-00-00',
                'prefix-2012-07-08_00-00-00',
                'prefix-2012-07-14_00-00-00',
                'prefix-2012-07-15_00-00-00',
                'prefix-2012-07-16_00-00-00',
                'prefix-2012-07-17_00-00-00',
                'prefix-2012-07-18_00-00-00',
                'prefix-2012-07-19_00-00-00',
                'prefix-2012-07-20_00-00-00',
                'prefix-2012-07-21_00-00-00',
                'prefix-2012-07-22_00-00-00',
                'prefix-2012-07-23_00-00-00',
                'prefix-2012-07-23_01-00-00',
                'prefix-2012-07-24_00-00-00']

    def test_list_defaults(self):
        """
        Should reduce to 12 archives with default settings.
        """
        intervals = [YEAR, MONTH, WEEK, DAY]
        current_date = datetime.datetime(2012, 7, 24, 22, 10, 0)
        keep = filter_archive_list(self.archives, intervals,
                                   "prefix-", current_date=current_date)
        self.assertEqual(len(keep), 12)

    def test_list_recent(self):
        """
        Store the last week's worth of data.
        """
        intervals = [YEAR, MONTH, WEEK, DAY]
        current_date = datetime.datetime(2012, 7, 24, 22, 10, 0)
        keep = filter_archive_list(self.archives, intervals, "prefix-",
                                   keep_all=WEEK, current_date=current_date)
        self.assertEqual(len(keep), 17)
