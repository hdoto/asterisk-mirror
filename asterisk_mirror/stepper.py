# -*- coding: utf-8 -*-

from threading import Event, Thread, Condition
import time

import importlib.util
try:
    importlib.util.find_spec('RPi.GPIO')
    import RPi.GPIO as GPIO
except ImportError:
    import fake_rpi
    fake_rpi.toggle_print(False)
    from fake_rpi.RPi import GPIO

# Stepper
# Usage:
#  stepper = Stepper([1,2,3])
#  stepper.step(10)      # 10ステップすすむ
#  stepper.set_angle(1.0) # 下を向く
#
class Stepper:
    def __init__(self, pins: list=[13, 19, 9], base_time: float=0.001, interrupt_event=None):
        # CONFIG
        self.step_pin = pins[0]
        self.direction_pin = pins[1]
        self.enable_pin = pins[2]
        self.base_time = base_time
        self.interrupt_event = Event() if interrupt_event is None else interrupt_event
        self.current_step = 0
        self.number_of_steps = 200 * 8 # 1/8 steps

        # GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.output(self.enable_pin, False)

        print("Stepper [", "step_pin:", self.step_pin, ", dir_pin:", self.direction_pin, ", enable_pin:", self.enable_pin, "]")

    def __del__(self):
        self.exit()

    def exit(self):
        self.interrupt()
        self.disable()
        GPIO.cleanup()

    def wait(self, time: float):
        #print("Stepper: waiting:", time)
        self.interrupt_event.wait(time)
    
    def interrupt(self):
        print("Stepper: interrupting...")
        self.interrupt_event.set()
    
    def clear(self):
        print("Stepper: clearing...")
        self.interrupt_event.clear()
    
    def is_interrupted(self) -> bool:
        return self.interrupt_event.is_set()
    
    def reset(self, speed: float=1.0) -> int :
        self.clear()
        steps = -self.current_step if self.current_step<self.number_of_steps/2 else self.number_of_steps-self.current_step
        #print("steps=", steps, ", current=", self.current_step)
        return self.rotate_by_steps(steps, speed)

    def enable(self, enables: bool=True):
        GPIO.output(self.enable_pin, not enables)
    
    def disable(self):
        self.enable(False)

    def step(self, dir: int=1):
        GPIO.output(self.direction_pin, dir<0)
        GPIO.output(self.step_pin, True)
        GPIO.output(self.step_pin, False)
        self.current_step = (self.current_step+dir) % self.number_of_steps

    def rotate_by_steps(self, steps: int, speed: float=1.0, easing: str='linear') -> int:
        #print("Stepper: rotate:", steps, "interrupted:", self.is_interrupted())
        if steps == 0:
            return 0
        
        # enable motor
        self.enable()
        wait_time = self.base_time/speed
        # repeat steps
        step = (1 if steps>0 else -1)
        for actual_steps in range(step, steps+step, step):
            #print("step:", step, " wait:", wait_time)
            self.step(step)
            self.interrupt_event.wait(wait_time)
            if self.is_interrupted():
                print("Stepper: interrupted.")
                break
        # disable motor
        self.disable()
        return actual_steps

    def rotate_to_balance(self) -> int:
        return 0

    def rotate_by_angle(self, radian: float, speed: float=1.0, easing: str='linear') -> int:
        steps = int(self.number_of_steps*radian/2.0)
        return self.rotate_by_steps(steps, speed, easing)

    def set_angle(self, radian: float, speed: float=1.0, easing: str='linear') -> int:
        steps = int(self.number_of_steps*radian/2.0) - self.current_step
        # print("steps = " + str(steps) + ", current = " + str(self.current_step))
        return self.rotate_by_steps(steps, speed, easing)
