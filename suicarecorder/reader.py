import nfc
import history

NUM_BLOCKS = 20
SERVICE_CODE = 0x090f


class UnsupportedTagError(Exception):
    def __init__(self, tag_class):
        self.tag_class = tag_class

    def __str__(self):
        return repr(self.tag_class.__name__)


class Reader:
    def __init__(self, device, logger):
        self.device = device
        self.clf = nfc.ContactlessFrontend(device)
        self.logger = logger

    def histories_from_tag(self, tag, num_blocks=NUM_BLOCKS):
        if not isinstance(tag, nfc.tag.tt3.Type3Tag):
            self.logger.error('Not Type3 Tag.')
            raise UnsupportedTagError(tag.__class__)
            return

        histories = []
        for i in range(num_blocks):
            block = tag.read([i], SERVICE_CODE)
            histories.append(history.from_block(block))
        return histories

    def read_histories(self, callback, on_error):
        def receive_tag(tag):
            self.logger.debug('connect: %s' % tag)
            try:
                callback(self.histories_from_tag(tag))
            except Exception as e:
                self.logger.error('%s' % e)
                on_error(e)
            finally:
                self.clf.close()

        return self.clf.connect(rdwr={'on-connect': receive_tag})


def read_histories(callback, logger, on_error=lambda(e): False, device='usb'):
    reader = Reader(device, logger)
    return reader.read_histories(callback, on_error)
