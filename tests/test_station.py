import unittest
from suicarecorder.station import Station
import suicarecorder.station as station


class StationTest(unittest.TestCase):
    def test__load_stations(self):
        self.assertIsNotNone(Station._load_stations())
        self.assertIsNotNone(Station.stations)

    def test_find_by_codes(self):
        self.assertEqual(
            Station.find_by_codes(line_code=0, station_code=1).area_code,
            0
        )


class ModuleFnTest(unittest.TestCase):
    def test_for_codes(self):
        self.assertEqual(
            station.for_codes(line_code=0, station_code=1).area_code,
            0
        )


if __name__ == '__main__':
    unittest.main()
