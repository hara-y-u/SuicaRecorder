# -*- coding: utf-8 -*-

import reader
from cement.core import foundation
import logging

app = foundation.CementApp('suicarecorder')
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)


def receive_histories(histories):
    for history in histories:
        print unicode('%s' % history)


def run():
    try:
        app.setup()
        app.run()
        reader.read_histories(receive_histories, logger)
    finally:
        app.close()


if __name__ == '__main__':
    run()
