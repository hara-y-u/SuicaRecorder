import unittest
import os
from suicarecorder.config import Config
import suicarecorder.config as config

CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(CONFIG_DIR, 'fixture/config.json')


class ConfigTest(unittest.TestCase):
    def setUp(self):
        self.config = Config(CONFIG_FILE)
        self.config.load()

    def test_load(self):
        self.assertEqual(self.config['output_dir'], '~/.suicarecorder-test')

    def test_get(self):
        self.assertEqual(self.config.get('output_dir'),
                         '~/.suicarecorder-test')
        self.assertEqual(self.config.get('hoge'), 'This has no default')


class ConfigModuleTest(unittest.TestCase):
    def test_get(self):
        self.assertEqual(config.get('output_dir', CONFIG_FILE),
                         '~/.suicarecorder-test')
        self.assertEqual(config.get('hoge', CONFIG_FILE),
                         'This has no default')
