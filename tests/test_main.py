# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch, MagicMock

from asterisk_mirror.main import AsteriskMirror

import time

class TestAsterisk(unittest.TestCase):
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