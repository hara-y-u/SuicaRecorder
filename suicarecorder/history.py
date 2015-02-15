# -*- coding: utf-8 -*-

import struct
import station
import re
import datetime
from collections import OrderedDict

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

PRODUCT_SALES_PROCESSES = {70, 73, 74, 75, 198, 203}
BUS_PROCESSES = {13, 15, 31, 35}

PROPERTIES = OrderedDict([
    ('id', u'ID'),
    ('console', u'端末'),
    ('process', u'処理'),
    ('date', u'日付'),
    ('time', u'時刻'),
    ('balance', u'残高'),
    ('charge', u'支払'),
    ('deposit', u'入金'),
    ('entered_station', u'入場駅'),
    ('exited_station', u'退場駅')
])

DEFAULT_FORMAT = \
    '\n'.join(['%s: %s' % (v, '%(' + '%s' % k + ')s')
               for k, v in PROPERTIES.items()])

BLOCK_FORMAT = '2B2H4BH4B'


class History(object):
    def __init__(self, values):
        for k, v in values.items():
            self.__dict__[k] = v
        self.previous = None

    @classmethod
    def process_as_big_endian(cls, data):
        return struct.unpack('>' + BLOCK_FORMAT, data)

    @classmethod
    def process_as_little_endian(cls, data):
        return struct.unpack('<' + BLOCK_FORMAT, data)

    @classmethod
    def date_from_bytes(cls, date_bytes):
        return datetime.date(
            year=((date_bytes >> 9) & 0x7f) + 2000,
            month=(date_bytes >> 5) & 0x0f,
            day=(date_bytes >> 0) & 0x1f
        )

    @classmethod
    def join_bytes(cls, bytes):
        return int(''.join('%02x' % i for i in bytes), 16)

    @classmethod
    def time_from_bytes(cls, time_bytes):
        return datetime.time(
            hour=(time_bytes >> 11) & 0x1f,
            minute=(time_bytes >> 5) & 0x3f
        )

    @classmethod
    def default_values_from_blocks(cls, be, le):
        console_num = be[0]
        process_num = be[1]
        return {
            'console_num': console_num,
            'console': CONSOLES.get(console_num, DEFAULT_CONSOLE),
            'process_num': process_num,
            'process': PROCESSES.get(process_num, DEFAULT_PROCESS),
            'date': cls.date_from_bytes(be[3]),
            'time': None,
            'balance': le[8],
            'entered_line_key': None,
            'entered_station_key': None,
            'entered_station': None,
            'exited_line_key': None,
            'exited_station_key': None,
            'exited_station': None,
            'id': cls.join_bytes([be[9], be[10], be[11]]),
            'region': be[12]
        }

    @classmethod
    def from_block(cls, block):
        be = cls.process_as_big_endian(block)
        le = cls.process_as_little_endian(block)
        process_num = be[1]

        values = cls.default_values_from_blocks(be, le)

        if process_num in PRODUCT_SALES_PROCESSES:
            values.update({
                'type': 'product_sales',
                'time': cls.time_from_bytes(cls.join_bytes([be[4], be[5]]))
            })
        elif process_num in BUS_PROCESSES:
            values.update({'type': 'bus'})
        else:
            values.update({
                'type': 'train',
                'entered_line_key': be[4],
                'entered_station_key': be[5],
                'entered_station': station.for_codes(be[4], be[5]),
                'exited_line_key': be[6],
                'exited_station_key': be[7],
                'exited_station': station.for_codes(be[6], be[7])
            })

        return cls(values)

    @property
    def delta(self):
        if self.previous:
            return self.balance - self.previous.balance

    @property
    def charge(self):
        if self.delta and self.delta < 0:
            return -1 * self.delta

    @property
    def deposit(self):
        if self.delta and self.delta > 0:
            return self.delta

    @property
    def attrs(self):
        class_items = self.__class__.__dict__.iteritems()
        props = dict((k, getattr(self, k))
                     for k, v in class_items
                     if k != 'attrs' and isinstance(v, property))
        return dict(props.items() + self.__dict__.items())

    def format(self, text=None, data=None):
        return (text or DEFAULT_FORMAT) % (data or self.attrs)

    def __str__(self):
        return self.format(DEFAULT_FORMAT, self.attrs)

    csv_header = ','.join(PROPERTIES.values())

    def csv_value(self, key):
        value = self.attrs.get(key)
        if not value:
            return ''
        else:
            return re.sub(',', '\,', '%s' % value)

    def to_csv(self):
        values = [self.csv_value(k) for k in PROPERTIES.keys()]
        return ','.join(values)

    @classmethod
    def from_list(cls, list):
        return cls(dict(zip(PROPERTIES.keys(), list)))


def from_block(block):
    return History.from_block(block)


def from_list(list):
    return History.from_list(list)
