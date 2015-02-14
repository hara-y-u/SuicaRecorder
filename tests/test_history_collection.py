import unittest
import binascii
from suicarecorder.history_collection import HistoryCollection
import suicarecorder.history as history
from suicarecorder.dummy_card_server import BLOCKS


class HistoryCollectionTest(unittest.TestCase):
    def setUp(self):
        hs = [history.from_block(binascii.unhexlify(b)) for b in BLOCKS]
        self.histories = HistoryCollection(hs)

    def test_sort_by(self):
        hs = self.histories
        hs.sort_by('id')
        for i, h in enumerate(hs):
            if 0 < i:
                self.assertTrue(hs[i-1].id < h.id)

    def test_prepare_previous(self):
        hs = self.histories
        hs.sort_by('id')
        for i, h in enumerate(hs):
            if i < len(hs) - 1:
                self.assertEqual(hs[i+1].previous, h)

    def test_brought_balance(self):
        hs = self.histories
        hs.brought_balance = 300
        hs.sort_by('id')
        self.assertEqual(hs[0].previous.balance, 300)
        self.assertEqual(hs[0].balance, 5859)
        self.assertEqual(hs[0].deposit, 5559)


if __name__ == '__main__':
    unittest.main()
