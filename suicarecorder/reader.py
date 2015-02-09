import nfc
import history

NUM_BLOCKS = 20
SERVICE_CODE = 0x090f


class Reader:
    def __init__(self, device, logger):
        self.device = device
        self.clf = nfc.ContactlessFrontend(device)
        self.logger = logger

    def histories_from_tag(self, tag, num_blocks=NUM_BLOCKS):
        if not isinstance(tag, nfc.tag.tt3.Type3Tag):
            self.logger.error('Not Type3 Tag.')
            return

        histories = []
        for i in range(num_blocks):
            try:
                block = tag.read([i], SERVICE_CODE)
                histories.append(history.from_block(block))
            except Exception as e:
                self.logger.error('%s' % e)

        return histories

    def read_histories(self, callback):
        def receive_tag(tag):
            self.logger.debug('connect: %s' % tag)
            try:
                callback(self.histories_from_tag(tag))
            finally:
                self.clf.close()

        self.clf.connect(rdwr={'on-connect': receive_tag})


def read_histories(callback, logger, device='usb'):
    reader = Reader(device, logger)
    return reader.read_histories(callback)
