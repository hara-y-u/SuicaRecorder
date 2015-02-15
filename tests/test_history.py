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

        self.train_history = history.from_block(
            binascii.unhexlify('160100021e42e536e336e31600088400')
        )
        self.train_history.previous = self.bus_history

        self.product_sales_history = history.from_block(
            binascii.unhexlify('c74600001e498940b64a460c00089d00')
        )
        self.product_sales_history.previous = self.train_history

    def test_init(self):
        h = self.bus_history
        self.assertEqual(u'bus', h.type)
        self.assertEqual(u'車載端末', h.console)
        self.assertEqual(u'バス (IruCa系)', h.process)
        self.assertEqual(datetime.date(2013, 10, 13), h.date)
        self.assertEqual(None, h.time)
        self.assertEqual(None, h.charge)
        self.assertEqual(None, h.deposit)
        self.assertEqual(241, h.balance)
        self.assertEqual(None, h.entered_station)
        self.assertEqual(None, h.exited_station)
        self.assertEqual(2668, h.id)

        h = self.train_history
        self.assertEqual(u'train', h.type)
        self.assertEqual(u'改札機', h.console)
        self.assertEqual(u'運賃支払(改札出場)', h.process)
        self.assertEqual(datetime.date(2015, 2, 2), h.date)
        self.assertEqual(None, h.time)
        self.assertEqual(None, h.charge)
        self.assertEqual(5618, h.deposit)
        self.assertEqual(5859, h.balance)
        self.assertEqual(station.for_codes(229, 54), h.entered_station)
        self.assertEqual(station.for_codes(227, 54), h.exited_station)
        self.assertEqual(2180, h.id)

        h = self.product_sales_history
        self.assertEqual(u'product_sales', h.type)
        self.assertEqual(u'物販端末', h.console)
        self.assertEqual(u'物販', h.process)
        self.assertEqual(datetime.date(2015, 2, 9), h.date)
        self.assertEqual(datetime.time(17, 10), h.time)
        self.assertEqual(2717, h.charge)
        self.assertEqual(None, h.deposit)
        self.assertEqual(3142, h.balance)
        self.assertEqual(None, h.entered_station)
        self.assertEqual(None, h.exited_station)
        self.assertEqual(2205, h.id)

    def test_to_csv(self):
        h = self.train_history
        self.assertEqual(
            h.to_csv(),
            u'2180,改札機,運賃支払(改札出場),2015-02-02,,5859,,5618,'
            u'中野坂上 [東京地下鉄-4号線丸ノ内],銀座 [東京地下鉄-3号線銀座]'
        )

    def test_from_list(self):
        h1 = self.train_history
        csv_str1 = h1.to_csv()
        list = csv_str1.split(',')
        h2 = history.from_list(list)
        csv_str2 = h2.to_csv()
        self.assertIsInstance(h2.id, int)
        self.assertIsInstance(h2.console, unicode)
        self.assertIsInstance(h2.date, datetime.date)
        self.assertEqual(csv_str1, csv_str2)

if __name__ == '__main__':
    unittest.main()
