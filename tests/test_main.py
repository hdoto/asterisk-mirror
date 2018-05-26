# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch, MagicMock

from asterisk_mirror.main import AsteriskMirror

import time

class TestAasterisk(unittest.TestCase):
    def test_init(self):
        # create instance by default
        asterisk = AsteriskMirror()
        assert asterisk.config['system']['transition'] == 30
        
        # create instance with some configurations
        asterisk = AsteriskMirror({'system': {'pins': [1, 2, 3]}, 'foo': "bar"})
        assert asterisk.config['system']['pins'][0] == 1
        assert asterisk.config['foo'] == "bar"

    def test_start_and_stop(self):
        asterisk = AsteriskMirror()

        asterisk.start()
        time.sleep(0.01) # wait for starting threads
        assert asterisk.logic_index == 0
        assert asterisk.stop_event.is_set() == False

        asterisk.stop()
        time.sleep(0.01) # wait for stopping threads
        assert asterisk.stop_event.is_set() == True

if __name__ == '__main__':
    unittest.main()