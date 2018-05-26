# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch, MagicMock

from asterisk_mirror.logics import AsteriskLogic, MorseLogic, YearLogic
from asterisk_mirror.stepper import Stepper

import time
from threading import Thread
from datetime import datetime

class TestAsteriskLogic(unittest.TestCase):
    def test_logic_execution(self):
        stepper = Stepper()
        logic = AsteriskLogic(stepper)
        logic.execute = MagicMock()
        thread = Thread(target=logic.run)
        thread.start()
        time.sleep(0.01)
        logic.execute.assert_called()
        stepper.interrupt()

class TestMorseLogic(unittest.TestCase):
    # https://cryptii.com/morse-code-translator
    test_morses = {
        "SOS":        "... --- ...",
        "asterisk":   ".- ... - . .-. .. ... -.-",
        "1234567890": ".---- ..--- ...-- ....- ..... -.... --... ---.. ----. -----",
        ".,!?-/()&:;=+_\"@":
            ".-.-.- --..-- -.-.-- ..--.. -....- -..-. -.--. -.--.- .-... ---... -.-.-. -...- .-.-. ..--.- .-..-. .--.-.",
        "The quick brown fox jumps over 13 lazy dogs.":
            "- .... . / --.- ..- .. -.-. -.- / -... .-. --- .-- -. / ..-. --- -..- / .--- ..- -- .--. ... / --- ...- . .-. / .---- ...-- / .-.. .- --.. -.-- / -.. --- --. ... .-.-.-",
        "h.o (hdoto) is an artist group based in Linz, Tokyo and Osaka.":
            ".... .-.-.- --- / -.--. .... -.. --- - --- -.--.- / .. ... / .- -. / .- .-. - .. ... - / --. .-. --- ..- .--. / -... .- ... . -.. / .. -. / .-.. .. -. --.. --..-- / - --- -.- -.-- --- / .- -. -.. / --- ... .- -.- .- .-.-.-"
    }

    def test_encode_morse(self):
        for message, morse in self.test_morses.items():
            logic = MorseLogic(Stepper(), message)
            assert logic.morse == morse

    def test_execute(self):
        def add_rotate_steps(rotate_steps:int):
            #print("steps: ", rotate_steps, flush=True)
            self.rotate_steps += rotate_steps
        def add_wait_duration(wait_duration:float):
            #print("wait: ", wait_duration, flush=True)
            self.wait_duration += wait_duration

        with patch('asterisk_mirror.stepper.Stepper') as StepperMock:
            stepper = StepperMock()
            stepper.is_interrupted.return_value = False
            stepper.rotate_by_steps.side_effect = add_rotate_steps
            stepper.wait.side_effect = add_wait_duration
            for message, morse in self.test_morses.items():
                self.rotate_steps = 0
                self.wait_duration = 0
                #print("message:", message)
                logic = MorseLogic(stepper, message)
                logic.execute()
                # dot: 1, dash: 3, inter-elem: 1, inter-letters: 3, inter-words: 7
                # steps = dot+dash*3
                rotate_steps = (morse.count('.') + morse.count('-')*3) * logic.dot_steps
                # wait_duration = dot*2 + dash*4 + space*2 + slash*4
                duration = morse.count('.')*2 + morse.count('-')*4 + morse.count(' ')*2 + morse.count('/')*4
                #print("wait:", self.wait_duration, ", steps:", self.rotate_steps)
                #print("duration:", int(round(self.wait_duration/logic.dot_interval)+self.rotate_steps/logic.dot_steps), "->", duration)
                assert self.rotate_steps == rotate_steps
                assert int(round(self.wait_duration/logic.dot_interval)+rotate_steps/logic.dot_steps) == duration

class TestYearLogic(unittest.TestCase):
    def _calc(self) -> int:
        return 0
    
    def test_20180602(self):
        with patch('asterisk_mirror.stepper.Stepper') as StepperMock:
            stepper = StepperMock()
            logic = YearLogic(stepper, datetime(2018, 6, 2))
            logic.execute()
            # angle: 0.83286 rad -> 150 deg
            # echo "scale=5; ( `date -ju 0602000018 +%s` - `date -ju 0101000018 +%s` ) / ( `date -ju 0101000019 +%s` - `date -ju 0101000018 +%s` ) * 2.0" | bc
            args, _ = stepper.set_angle.call_args
            # print("call_args:", args[0]*180)
            assert round(args[0]*180) == 150


if __name__ == '__main__':
    unittest.main()