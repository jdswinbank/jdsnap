import datetime
import unittest

from jdsnap import (date_from_name, DEFAULT_DATEFMT,
                    DAY, WEEK, MONTH, YEAR)

class TestParseDate(unittest.TestCase):
    def setUp(self):
        self.date = datetime.datetime(2014, 1, 1, 0, 0, 0)

    def test_parse_simple(self):
        date = date_from_name("prefix-%s" %
                              (self.date.strftime(DEFAULT_DATEFMT)), "prefix-")
        self.assertEqual(self.date, date)

    def test_parse_no_prefix(self):
        date = date_from_name("%s" % (self.date.strftime(DEFAULT_DATEFMT)), "")
        self.assertEqual(self.date, date)

    def test_parse_custom_format(self):
        date = date_from_name("prefix-%s" %
                              (self.date.strftime("%d-%m-%Y_%S-%M-%H")),
                              "prefix-", datefmt="%d-%m-%Y_%S-%M-%H")
        self.assertEqual(self.date, date)


class TestConstants(unittest.TestCase):
    def test_relative_sizes(self):
        self.assertTrue(DAY < WEEK < MONTH < YEAR)
