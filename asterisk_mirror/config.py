# -*- coding: utf-8 -*-

from configparser import ConfigParser
from threading import Lock

_CONFIG_FILE = '/boot/asterisk-mirror.cfg'

_CONFIG_DEFAULT = '''
[System]
# GPIO pin assignments
step_pin = 13
direction_pin = 19
enable_pin = 9

# scene transition interval (secs)
transition = 300

# logics
logics = MorseLogic, YearLogic, FlucLogic

[MorseLogic]
# a message to encode morse-codes
message = asterisk

# stepper speed
speed = 1.0

# stepper counts
steps = 40

[YearLogic]
# stepper speed
speed = 1.0

[FlucLogic]
# stepper speed
speed = 1.0

# rotate fluctuation
fluctuate = False

# fluctuation rate
rate = 0.5

'''

class AsteriskConfig:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.load()
        return cls._instance

    def __init__(self):
        pass

    def load(self, files: list=[_CONFIG_FILE]):
        print("AsteriskConfig: load files:", files)
        parser = ConfigParser()
        parser.read_string(_CONFIG_DEFAULT)
        parser.read(files)
        self.configs = {}
        for section in parser.sections():
            self.configs[section] = dict(parser.items(section))
        return self

    def get(self, keys: str, cast=None):
        value = self.configs
        for key in keys.split('.'):
            if not key in value:
                return None
            value = value[key]
        
        #print(keys, ":", value, "->", cast)
        if cast is int:
            return int(value)
        elif cast is float:
            return float(value)
        elif cast is bool:
            return value.lower() == "true"
        else:
            return value
