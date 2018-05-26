# -*- coding: utf-8 -*-

import uuid
import signal
from threading import Thread, Event, Timer
from typing import List

from asterisk_mirror.stepper import Stepper
from asterisk_mirror.logics import MorseLogic, YearLogic, FlucLogic

# innner methods
def _merge_dict(source: str, destination: str):
    for key, value in source.items():
        if isinstance(value, dict):
            node = destination.setdefault(key, {})
            _merge_dict(value, node)
        else:
            destination[key] = value
    return destination

# AsteriskMirror
class AsteriskMirror:
    default_config = {
        'system': {
            'pins': [13, 19, 9], # step pin, direction pin, enable pin
            'transition': 30
        }
    }
    timer_interval = 30 # sec.

    def __init__(self, config: dict={}):
        print("AsteriskMirror: creating...")
        # configurations
        self.config = _merge_dict(config, self.default_config)
        self.stop_event = Event()
        self.main_thread = None
        self.timer_thread = None
        self.stepper = Stepper(self.config['system']['pins'])
        self.logics = []
        self.logic_index = -1

        # append logics
        self.logics.append(MorseLogic(self.stepper, "ASTERISK"))
        self.logics.append(YearLogic(self.stepper))
        self.logics.append(FlucLogic(self.stepper))
        
    def start(self):
        if self.main_thread is not None:
            print("AsteriskMirror: already started.")
            return
        print ("AsteriskMirror: starting...")
        # renew threads
        if self.timer_thread is not None:
            self.stop_event.set()
        self.timer_thread = Thread(target=self.timer_run)
        self.stop_event.clear()
        self.main_thread = Thread(target=self.run)

        # start threads
        self.main_thread.start()
        self.timer_thread.start()

    def stop(self):
        print("AsteriskMirror: stopping...")
        self.stop_event.set()
        self.stepper.interrupt()
        self.timer_thread = None
        self.main_thread = None

    def timer_run(self):
        while not self.stop_event.is_set():
            # set a new index of logics
            self.logic_index = (self.logic_index+1)%len(self.logics)
            print("AsteriskMirror: changes logic:", self.logics[self.logic_index])
            # interrupt stepper thread and main thread
            self.stepper.interrupt()
            self.stop_event.wait(self.timer_interval)

    def run(self):
        #print("AsteriskMirror.run starting...")
        while not self.stop_event.is_set():
            if self.logic_index >= 0 and len(self.logics) > 0:
                logic = self.logics[self.logic_index]
                logic.run()
            else:
                # wait until a right logic-index will be set
                self.stop_event.wait(1)

# main
def main():
    mirror = AsteriskMirror()
    mirror.start()

    def handler(signal, frame):
        mirror.stop()
    signal.signal(signal.SIGINT, handler)


if __name__ == '__main__':
    main()