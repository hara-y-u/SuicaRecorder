# -*- coding: utf-8 -*-

import unittest
from suicarecorder.reader import Reader
import binascii
import datetime
import logging
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)


class ReaderTest(unittest.TestCase):
    def setUp(self):
        self.reader = Reader(logger)

    def test_histories_from_tag(self):
        block = binascii.unhexlify('050f000f1b4d0c4f0000f100000a6c00')
        print self.reader.histories_from_tag


if __name__ == '__main__':
    unittest.main()
