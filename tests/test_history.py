# -*- coding: utf-8 -*-

import unittest
import suicarecorder.history as history
import binascii
import datetime
import suicarecorder.station as station


class HistoryTest(unittest.TestCase):
    def setUp(self):
        self.history = history.from_block(
            binascii.unhexlify('050f000f1b4d0c4f0000f100000a6c00')
        )

    def test_from_block(self):
        h = self.history

        self.assertEqual(u'車載端末', h.console)
        self.assertEqual(u'バス (IruCa系)', h.process)
        self.assertEqual(datetime.date(13, 10, 13), h.date)
        self.assertEqual(241, h.balance)
        self.assertEqual(station.for_codes(12, 79), h.entered_station)
        self.assertEqual(station.for_codes(0, 0), h.exited_station)


if __name__ == '__main__':
    unittest.main()
