# -*- coding: utf-8 -*-

import unittest
from suicarecorder.station import Station


class StationTest(unittest.TestCase):
    def test__load_data(self):
        self.assertIsNone(Station.data)
        self.assertIsNotNone(Station._load_data())
        self.assertIsNotNone(Station.data)

    def test_find_by_codes(self):
        self.assertEqual(
            Station.find_by_codes(line_code=0, station_code=1).area_code,
            0
        )


if __name__ == '__main__':
    unittest.main()
