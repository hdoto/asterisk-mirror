# -*- coding: utf-8 -*-

import time
from datetime import datetime

from asterisk_mirror.config import AsteriskConfig

# ----------------------------------------------------------------------
# ステッピングモータの動きを表す基底ロジック
# ----------------------------------------------------------------------
class AsteriskLogic:
    def __init__(self, stepper):
        self.stepper = stepper
    
    def __str__(self) -> str:
        return self.__class__.__name__

    def execute(self):
        raise Exception
    
    def run(self):
        print("AsteriskLogic: start logic:", self)
        self.stepper.clear()
        while not self.stepper.is_interrupted():
            started = time.time()
            # execute the logic
            self.execute()
            # wait if the exec time is less than 0.5sec
            wait_time = 0.5 - (time.time()-started)
            if wait_time > 0:
                print("AsteriskLogic: wait:", wait_time)
                self.stepper.wait(wait_time)

# ----------------------------------------------------------------------
# モールス符号の動きをするロジック
# ----------------------------------------------------------------------
class MorseLogic(AsteriskLogic):
    morse_map = {
        "A" : ".-",
        "B" : "-...",
        "C" : "-.-.",
        "D" : "-..",
        "E" : ".",
        "F" : "..-.",
        "G" : "--.",
        "H" : "....",
        "I" : "..",
        "J" : ".---",
        "K" : "-.-",
        "L" : ".-..",
        "M" : "--",
        "N" : "-.",
        "O" : "---",
        "P" : ".--.",
        "Q" : "--.-",
        "R" : ".-.",
        "S" : "...",
        "T" : "-",
        "U" : "..-",
        "V" : "...-",
        "W" : ".--",
        "X" : "-..-",
        "Y" : "-.--",
        "Z" : "--..",
        "1" : ".----",
        "2" : "..---",
        "3" : "...--",
        "4" : "....-",
        "5" : ".....",
        "6" : "-....",
        "7" : "--...",
        "8" : "---..",
        "9" : "----.",
        "0" : "-----",
        "." : ".-.-.-",
        "," : "--..--",
        "?" : "..--..",
        "!" : "-.-.--",
        "-" : "-....-",
        "/" : "-..-.",
        "(" : "-.--.",
        ")" : "-.--.-",
        "&" : ".-...",
        ":" : "---...",
        ";" : "-.-.-.",
        "=" : "-...-",
        "+" : ".-.-.",
        "-" : "-....-",
        "_" : "..--.-",
        "\"" : ".-..-.",
        "@" : ".--.-.",
        " " : "/"
    }

    def _encode_morse(self, message):
        encoded = ""
        for char in message[:]:
            encoded += self.morse_map[char.upper()] + " "
        return encoded[:-1]

    def __init__(self, stepper):
        super().__init__(stepper)
        config = AsteriskConfig()
        self.set_message(config.get('MorseLogic.message'))
        self.speed = config.get('MorseLogic.speed', float)
        self.dot_steps = config.get('MorseLogic.steps', int)
        self.dot_interval = 0.001 / (self.speed/2) * self.dot_steps
        print("MorseLogic [", "message:", self.message, ", speed:", self.speed, "]")

    def set_message(self, message):
        self.message = message
        self.morse = self._encode_morse(message)

    def execute(self):
        print("MorseLogic: message:", self.message)
        #print("MorseLogic: morse:", self.morse)
        #print("MorseLogic:", "steps:", self.dot_steps, ", interval:", self.dot_interval)
        for ch in list(self.morse):
            print(ch, flush=True, end='')
            if (ch == '.'):
                self.stepper.rotate_by_steps(self.dot_steps, self.speed/2)
                self.stepper.wait(self.dot_interval)
            elif (ch == '-'):
                self.stepper.rotate_by_steps(self.dot_steps*3, self.speed/2)
                self.stepper.wait(self.dot_interval)
            elif (ch == ' '):
                self.stepper.wait(self.dot_interval*2) # 3-1
            else:
                self.stepper.wait(self.dot_interval*4) # 7-3

            if self.stepper.is_interrupted():
                break
        print('', flush=True)
        self.stepper.wait(self.dot_interval*8) # 15-7

# ----------------------------------------------------------------------
# 1年のうちの今位置に移動するロジック
# ----------------------------------------------------------------------
class YearLogic(AsteriskLogic):
    def __init__(self, stepper, target=None):
        super().__init__(stepper)
        self.target = target
        self.speed = AsteriskConfig().get('YearLogic.speed', float)
        print("YearLogic [", "target:", target, "]")

    def execute(self):
        now = datetime.now() if self.target == None else self.target
        begin = datetime(now.year, 1, 1)
        last  = datetime(now.year+1, 1, 1)
        angle = 2.0 * (now-begin) / (last-begin)
        print("YearLogic: angle:", angle)
        self.stepper.set_angle(angle, self.speed)
        self.stepper.wait(10)

# ----------------------------------------------------------------------
# 1/fゆらぎの動きをするロジック
# ----------------------------------------------------------------------
class FlucLogic(AsteriskLogic):
    def __init__(self, stepper):
        super().__init__(stepper)
        self.speed = AsteriskConfig().get('FlucLogic.speed', float)
        print("FlucLogic [", "speed:", self.speed, "]")

    def execute(self):
        self.stepper.enable()
        while not self.stepper.is_interrupted():
            self.stepper.step(1)
            self.stepper.wait(0.01 / self.speed)
