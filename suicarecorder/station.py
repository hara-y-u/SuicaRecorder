import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, 'data')
DATA_FILE = 'station_codes.json'
DATA_PATH = os.path.join(DATA_DIR, DATA_FILE)


class Station(object):
    data = None
    default = {
        'area_code': 0, 'line_code': 0, 'station_code': 0,
        'company_name': 'No Company', 'line_name': 'No Line',
        'station_name': 'No Station', 'note': ''
    }

    def __init__(self, data):
        for k, v in data.items():
            self.__dict__[k] = v

    @classmethod
    def _load_data(cls):
        if not cls.data:
            f = open(DATA_PATH, 'r')
            cls.data = json.load(f)
        return cls.data

    @classmethod
    def find_by_codes(cls, line_code, station_code):
        stations = cls._load_data()
        for s in stations:
            if(s['line_code'] is line_code and
               s['station_code'] is station_code):
                return cls(s)
        return cls(cls.default)
