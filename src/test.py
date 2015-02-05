#!/usr/bin/env python
# -*- coding: utf-8 -*-

import binascii
import nfc

service_code = 0x090f


def connected(tag):
    # タグのIDなどを出力する
    print tag

    if isinstance(tag, nfc.tag.tt3.Type3Tag):
        try:
            # ブロック0番の内容を16進数で出力する
            print "block: %s" % binascii.hexlify(tag.read([0], service_code))
        except Exception as e:
            print "error: %s" % e
        else:
            print "error: tag isn't Type3Tag"


# タッチ時のハンドラを設定して待機する
clf = nfc.ContactlessFrontend('usb')
clf.connect(rdwr={'on-connect': connected})
