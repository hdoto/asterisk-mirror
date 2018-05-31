# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch, MagicMock

from asterisk_mirror.config import AsteriskConfig

class TestAsteriskConfig(unittest.TestCase):
    def test_singleton(self):
        a = AsteriskConfig()
        b = AsteriskConfig()
        assert id(a) == id(b)

    def test_load(self):
        # /root/asterisk-mirror.cfg not found...
        AsteriskConfig().load()
        assert AsteriskConfig().get('System.transition') == '300'
        assert AsteriskConfig().get('MorseLogic.message') == 'asterisk'

        # tests/asterisk-mirror.cfg will be load
        AsteriskConfig().load(['tests/asterisk-mirror.cfg'])
        assert AsteriskConfig().get('System.transition') == '60'
        assert AsteriskConfig().get('MorseLogic.message') == 'hello h.o world!'

    def test_load_with_type(self):
        config = AsteriskConfig().load()
        assert config.get('System.transition', int) == 300
        assert config.get('System.transition', float) == 300.0
        assert config.get('FlucLogic.fluctuate', bool) == False
