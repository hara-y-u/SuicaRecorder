# -*- coding: utf-8 -*-

import unittest
import suicarecorder.history as history
import binascii
import datetime
import suicarecorder.station as station


class HistoryTest(unittest.TestCase):
    def setUp(self):
        self.bus_history = history.from_block(
            binascii.unhexlify('050f000f1b4d0c4f0000f100000a6c00')
        )
        self.product_sales_history = history.from_block(
            binascii.unhexlify('c74600001e498940b64a460c00089d00')
        )
        self.train_history = history.from_block(
            binascii.unhexlify('160100021e42e536e336e31600088400')
        )

    def test_from_block(self):
        h = self.bus_history
        self.assertEqual(u'車載端末', h.console)
        self.assertEqual(u'バス (IruCa系)', h.process)
        self.assertEqual(datetime.date(2013, 10, 13), h.date)
        self.assertEqual(None, h.time)
        self.assertEqual(241, h.balance)
        self.assertEqual(None, h.entered_station)
        self.assertEqual(None, h.exited_station)
        self.assertEqual(2668, h.id)

        h = self.product_sales_history
        self.assertEqual(u'物販端末', h.console)
        self.assertEqual(u'物販', h.process)
        self.assertEqual(datetime.date(2015, 2, 9), h.date)
        self.assertEqual(datetime.time(17, 10), h.time)
        self.assertEqual(3142, h.balance)
        self.assertEqual(None, h.entered_station)
        self.assertEqual(None, h.exited_station)
        self.assertEqual(2205, h.id)

        h = self.train_history
        self.assertEqual(u'改札機', h.console)
        self.assertEqual(u'運賃支払(改札出場)', h.process)
        self.assertEqual(datetime.date(2015, 2, 2), h.date)
        self.assertEqual(None, h.time)
        self.assertEqual(5859, h.balance)
        self.assertEqual(station.for_codes(229, 54), h.entered_station)
        self.assertEqual(station.for_codes(227, 54), h.exited_station)
        self.assertEqual(2180, h.id)


if __name__ == '__main__':
    unittest.main()
