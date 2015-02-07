import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, 'data')
DATA_FILE = 'station_codes.json'
DATA_PATH = os.path.join(DATA_DIR, DATA_FILE)


class Station(object):
    stations = None
    default = {
        'area_code': 0, 'line_code': 0, 'station_code': 0,
        'company_name': 'No Company', 'line_name': 'No Line',
        'station_name': 'No Station', 'note': ''
    }
    _default = None

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
        if not cls._default:
            cls._default = cls(cls.default)
        return cls._default

    @classmethod
    def find_by_codes(cls, line_code, station_code):
        stations = cls._load_stations()
        for s in stations:
            if(s.line_code is line_code and
               s.station_code is station_code):
                return s
        return cls.default_instance()

    def __str__(self):
        return '%(station_name)s [%(company_name)s-%(line_name)s]' % \
            self.__dict__


def for_codes(line_code, station_code):
    return Station.find_by_codes(line_code, station_code)
