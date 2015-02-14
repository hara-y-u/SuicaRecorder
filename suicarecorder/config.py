import os
import json

BASE_DIR = '~/.suicarecorder'

FILE_PATH = os.path.join(BASE_DIR, 'config.json')

DEFAULTS = {
    'output_dir': BASE_DIR
}


class Config(dict):
    def __init__(self, file_path=FILE_PATH):
        self.file_path = file_path
        self._dict = None

    @property
    def dict(self):
        if not self._dict:
            if os.path.isfile(self.file_path):
                with open(self.file_path, 'r') as f:
                    self._dict = json.load(f, 'utf-8')
            else:
                self._dict = {}
        return self._dict

    def load(self):
        for k, v in self.dict.items():
            self.__setitem__(k, v)

        return self

    def get(self, key):
        return dict.get(self, key, DEFAULTS.get(key))


_CONFIGS = {}


def get(key, config_file_path=None):
    file_path = config_file_path or FILE_PATH
    if not _CONFIGS.get(file_path):
        _CONFIGS[file_path] = Config(file_path).load()
    return _CONFIGS[file_path].get(key)
