import unittest

import pandas as pd

from tse_visualizer.plotting import convert_jalali_index_to_gregorian


class TestPlottingHelpers(unittest.TestCase):
    def test_convert_jalali_index_to_gregorian(self):
        jalali_dates = pd.Index(["1401-01-01", "1401-01-02"])
        converted = convert_jalali_index_to_gregorian(jalali_dates)

        self.assertEqual(str(converted[0].date()), "2022-03-21")
        self.assertEqual(str(converted[1].date()), "2022-03-22")


if __name__ == "__main__":
    unittest.main()
