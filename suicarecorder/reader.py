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

    def read_tag(self, callback):
        self.clf.connect(rdwr={'on-connect': callback})

    def read_histories(self, callback, num_blocks=NUM_BLOCKS):
        def receive_tag(tag):
            self.logger.debug('connect: %s' % tag)
            try:
                callback(self.histories_from_tag(tag))
            finally:
                self.clf.close()

        self.read_tag(receive_tag)


def read_histories(callback, logger):
    reader = Reader('usb', logger)
    return reader.read_histories(callback)
