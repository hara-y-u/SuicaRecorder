# -*- coding: utf-8 -*-

import unittest
import suicarecorder.reader as reader
import suicarecorder.dummy_card_server as dummy_card_server
from suicarecorder.history import History
import logging


class ReaderTest(unittest.TestCase):
    def test_read_tistories(self):
        logger = logging.getLogger(__name__)
        ch = logging.StreamHandler()
        logger.addHandler(ch)

        def receive_histories(histories):
            self.assertIsInstance(histories, list)
            self.assertEqual(len(histories), 20)
            for history in histories:
                self.assertIsInstance(history, History)

        dummy_card_server.start()
        reader.read_histories(receive_histories, logger, device='udp')


if __name__ == '__main__':
    unittest.main()
