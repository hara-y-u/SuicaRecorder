# -*- coding: utf-8 -*-

import unittest
import suicarecorder.history as history
import binascii
import datetime
import suicarecorder.station as station


class HistoryTest(unittest.TestCase):
    def test_from_block(self):
        h = history.from_block(
            binascii.unhexlify('050f000f1b4d0c4f0000f100000a6c00')
        )

        self.assertEqual(u'車載端末', unicode(h.console, encoding='utf-8'))
        self.assertEqual(u'バス', unicode(h.purpose, encoding='utf-8'))
        self.assertEqual(datetime.date(13, 10, 13), h.date)
        self.assertEqual(241, h.balance)
        self.assertEqual(station.for_codes(12, 79), h.entered_station)
        self.assertEqual(station.for_codes(0, 0), h.exited_station)


if __name__ == '__main__':
    unittest.main()
