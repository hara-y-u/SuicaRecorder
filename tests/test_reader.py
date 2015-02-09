# -*- coding: utf-8 -*-

import nfc
import unittest
import suicarecorder.reader as reader
from suicarecorder.history import History
import binascii
import logging
import threading

BLOCKS = [
    'c74600001e498940b64a460c00089d00',
    'c84600001e4985a041fa490d00089c00',
    'c74600001e489f653d153d0f00089b00',
    '160100021e48e52be5360e1200089a00',
    'c74600001e488a8c38f0d11200089800',
    '160100021e48e536e52aa51600089700',
    '161402011e48e5360000681700089500',
    'c74600001e47a280a853e00300089400',
    'c74600001e47a1e0a925b80400089300',
    'c74600001e46abe5d52ed30700089200',
    'c74600001e4686c186b2f80800089100',
    'c74600001e4482e192259c0a00089000',
    'c74600001e43af65d52f640b00088f00',
    '160100021e43e336e5365c0e00088e00',
    '160100021e43e536e3361f0f00088c00',
    'c74600001e42aa431090e20f00088a00',
    'c74600001e42a003406ed71300088900',
    '160100021e42e534e5367b1500088800',
    '160100021e42e336e534201600088600',
    '160100021e42e536e336e31600088400'
]


class ReaderTest(unittest.TestCase):
    def test_read_tistories(self):
        logger = logging.getLogger(__name__)
        ch = logging.StreamHandler()
        logger.addHandler(ch)

        def touch_a_card():
            card = nfc.ContactlessFrontend('udp')

            # Emulates RC-S380
            nfcf_idm = bytearray.fromhex('011004107f12ce22')
            nfcf_pmm = bytearray.fromhex('100b4b428485d0ff')
            nfcf_sys = bytearray.fromhex('0003')
            target = nfc.clf.TTF(br=212, idm=nfcf_idm,
                                 pmm=nfcf_pmm, sys=nfcf_sys)

            def ndef_read(block_number, rb, re):
                return binascii.unhexlify(BLOCKS[block_number])

            def connected(tag, cmd):
                tag.add_service(reader.SERVICE_CODE, ndef_read,
                                lambda: False)
                return True

            while card.connect(card={
                    'targets': [target],
                    'on-connect': connected
            }):
                pass

        def receive_histories(histories):
            self.assertIsInstance(histories, list)
            self.assertEqual(len(histories), 20)
            for history in histories:
                self.assertIsInstance(history, History)

        touch_th = threading.Thread(target=touch_a_card, name='touch_th')
        touch_th.setDaemon(True)
        touch_th.start()

        reader.read_histories(receive_histories, logger, 'udp')


if __name__ == '__main__':
    unittest.main()
