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
        hs = self.histories.sort_by('id')
        print hs
        for i, h in enumerate(hs):
            if 0 < i:
                self.assertTrue(hs[i-1].id < h.id)


if __name__ == '__main__':
    unittest.main()
