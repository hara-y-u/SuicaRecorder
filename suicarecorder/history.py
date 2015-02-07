# -*- coding: utf-8 -*-

import struct
import station
import datetime

DEFAULT_CONSOLE = u'不明端末'

CONSOLES = {
    3: u'精算機',
    4: u'携帯型端末',
    5: u'車載端末',
    7: u'券売機',
    8: u'券売機',
    9: u'入金機',
    18: u'券売機',
    20: u'券売機等',
    21: u'券売機等',
    22: u'改札機',
    23: u'簡易改札機',
    24: u'窓口端末',
    25: u'窓口端末',
    26: u'改札端末',
    27: u'携帯電話',
    28: u'乗継精算機',
    29: u'連絡改札機',
    31: u'簡易入金機',
    70: u'VIEW ALTTE',
    72: u'VIEW ALTTE',
    199: u'物販端末',
    200: u'自販機'
}

DEFAULT_PROCESS = u'不明処理'

PROCESSES = {
    1: u'運賃支払(改札出場)',
    2: u'チャージ',
    3: u'券購(磁気券購入)',
    4: u'精算',
    5: u'精算 (入場精算)',
    6: u'窓出 (改札窓口処理)',
    7: u'新規 (新規発行)',
    8: u'控除 (窓口控除)',
    13: u'バス (PiTaPa系)',
    15: u'バス (IruCa系)',
    17: u'再発 (再発行処理)',
    19: u'支払 (新幹線利用)',
    20: u'入A (入場時オートチャージ)',
    21: u'出A (出場時オートチャージ)',
    31: u'入金 (バスチャージ)',
    35: u'券購 (バス路面電車企画券購入)',
    70: u'物販',
    72: u'特典 (特典チャージ)',
    73: u'入金 (レジ入金)',
    74: u'物販取消',
    75: u'入物 (入場物販)',
    198: u'物現 (現金併用物販)',
    203: u'入物 (入場現金併用物販)',
    132: u'精算 (他社精算)',
    133: u'精算 (他社入場精算)'
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
            'console': CONSOLES.get(be[0], DEFAULT_CONSOLE),
            'process': PROCESSES.get(be[1], DEFAULT_PROCESS),
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
