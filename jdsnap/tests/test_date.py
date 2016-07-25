import datetime
import unittest
import jdsnap

class TestParseDate(unittest.TestCase):
    def setUp(self):
        self.date = datetime.datetime(2014, 1, 1, 0, 0, 0)

    def test_parse_simple(self):
        date = jdsnap.date_from_name("prefix-%s" %
                                     (self.date.strftime("%Y-%m-%d_%H-%M-%S")),
                                     "prefix-")
        self.assertEqual(self.date, date)

    def test_parse_no_prefix(self):
        date = jdsnap.date_from_name("%s" %
                                     (self.date.strftime("%Y-%m-%d_%H-%M-%S")),
                                     "")
        self.assertEqual(self.date, date)

    def test_parse_custom_format(self):
        date = jdsnap.date_from_name("prefix-%s" %
                                     (self.date.strftime("%d-%m-%Y_%S-%M-%H")),
                                     "prefix-", fmtstring="%d-%m-%Y_%S-%M-%H")
        self.assertEqual(self.date, date)


class TestConstants(unittest.TestCase):
    def test_relative_sizes(self):
        self.assertTrue(jdsnap.DAY < jdsnap.WEEK < jdsnap.MONTH < jdsnap.YEAR)
