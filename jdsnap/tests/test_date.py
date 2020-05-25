import unittest

from jdsnap.date import DAY, WEEK, MONTH, YEAR


class TestConstants(unittest.TestCase):
    def test_relative_sizes(self):
        self.assertTrue(DAY < WEEK < MONTH < YEAR)
