# -*- coding: utf-8 -*-

import struct
import station
import datetime

CONSOLES = {
    0x03: u'精算機',
    0x04: u'携帯型端末',
    0x05: u'車載端末',
    0x12: u'券売機',
    0x16: u'改札機',
    0x1c: u'乗継精算機',
    0xc8: u'自販機'
}

PROCESSES = {
    0x01: u'運賃支払',
    0x02: u'チャージ',
    0x0f: u'バス',
    0x46: u'物販'
}

DEFAULT_FORMAT = u'''
端末: %(console)s
処理: %(process)s
日付: %(date)s
残高: %(balance)d
入場: %(entered_station)s
退場: %(exited_station)s
'''


class History(object):
    def __init__(self, values):
        for k, v in values.items():
            self.__dict__[k] = v

    @classmethod
    def process_as_big_endian(cls, data):
        return struct.unpack('>2B2H4BH4B', data)

    @classmethod
    def process_as_little_endian(cls, data):
        return struct.unpack('<2B2H4BH4B', data)

    @classmethod
    def date_from_bytes(cls, bytes_date):
        return datetime.date(
            year=(bytes_date >> 9) & 0x7f,
            month=(bytes_date >> 5) & 0x0f,
            day=(bytes_date >> 0) & 0x1f
        )

    @classmethod
    def from_block(cls, block):
        be = cls.process_as_big_endian(block)
        le = cls.process_as_little_endian(block)

        values = {
            'console': CONSOLES.get(be[0], u'不明端末'),
            'process': PROCESSES.get(be[1], u'不明用途'),
            'date': cls.date_from_bytes(be[3]),
            'balance': le[8],
            'entered_station': station.for_codes(be[4], be[5]),
            'exited_station': station.for_codes(be[6], be[7])
        }

        return cls(values)

    def format(self, text=None, data=None):
        return (text or DEFAULT_FORMAT) % (data or self.__dict__)

    def __str__(self):
        return self.format(DEFAULT_FORMAT, self.__dict__)


def from_block(block):
    return History.from_block(block)
