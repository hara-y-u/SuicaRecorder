import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, 'data')
DATA_FILE = 'station_codes.json'
DATA_PATH = os.path.join(DATA_DIR, DATA_FILE)


class Station(object):
    stations = []
    default = {
        'area_code': 0, 'line_code': 0, 'station_code': 0,
        'company_name': 'No Company', 'line_name': 'No Line',
        'station_name': 'No Station', 'note': ''
    }
    _default_instance = None

    def __init__(self, data):
        for k, v in data.items():
            self.__dict__[k] = v

    @classmethod
    def _load_stations(cls):
        if not cls.stations:
            cls.stations = []
            with open(DATA_PATH, 'r') as f:
                for data in json.load(f, 'utf-8'):
                    cls.stations.append(cls(data))
        return cls.stations

    @classmethod
    def default_instance(cls):
        if not cls._default_instance:
            cls._default_instance = cls(cls.default)
        return cls._default_instance

    @classmethod
    def find(cls, attrs):
        stations = cls._load_stations()
        for s in stations:
            if all(s.__dict__[k] == v for k, v in attrs.items()):
                return s
        return cls.default_instance()

    @classmethod
    def find_by_codes(cls, line_code, station_code):
        return cls.find({
            'line_code': line_code,
            'station_code': station_code
        })

    @classmethod
    def find_by_names(cls, station_name, company_name, line_name):
        return cls.find({
            'station_name': station_name,
            'company_name': company_name,
            'line_name': line_name
        })

    @classmethod
    def find_by_station_string(cls, station_string):
        match = re.match(u'(?P<station>[\w]+)'
                         u'\((?P<company>[\w]+)\-(?P<line>[\w]+)\)',
                         station_string, re.U)
        return cls.find_by_names(match.group('station'),
                                 match.group('company'),
                                 match.group('line'))

    def __str__(self):
        return '%(station_name)s(%(company_name)s-%(line_name)s)' % \
            self.__dict__


def for_codes(line_code, station_code):
    return Station.find_by_codes(line_code, station_code)


def for_station_string(station_string):
    return Station.find_by_station_string(station_string)
