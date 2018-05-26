# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch

from asterisk_mirror.stepper import Stepper

from threading import Thread
import time

class TestStepper(unittest.TestCase):
    def test_init(self):
        stepper = Stepper([1,2,3])
        assert stepper.step_pin == 1
        assert stepper.direction_pin == 2
        assert stepper.enable_pin == 3

    def test_rotate_by_steps(self):
        stepper = Stepper(base_time=0.0001)
        # rotate 100 steps 
        steps = stepper.rotate_by_steps(100, 10)
        assert steps == 100
        assert stepper.current_step == 100
        # rotate -50 steps
        steps = stepper.rotate_by_steps(-50, 10)
        assert steps == -50
        assert stepper.current_step == 50

    def test_reset(self):
        stepper = Stepper(base_time=0.00001)
        # rotate 10steps -> reset -10steps
        steps = stepper.rotate_by_steps(10)
        assert stepper.current_step == 10
        steps = stepper.reset()
        assert stepper.current_step == 0
        assert steps == -10
        # rotate 1200steps -> reset 400steps
        test_steps = int(stepper.number_of_steps*3/4)
        steps = stepper.rotate_by_steps(test_steps)
        assert stepper.current_step == test_steps
        steps = stepper.reset()
        assert stepper.current_step == 0
        assert steps == stepper.number_of_steps-test_steps
        # rotate -400steps -> reset 400steps
        test_steps = int(-stepper.number_of_steps/4)
        steps = stepper.rotate_by_steps(test_steps)
        assert stepper.current_step == stepper.number_of_steps+test_steps
        steps = stepper.reset()
        #print("steps=", steps, ", current=", stepper.current_step)
        assert stepper.current_step == 0
        assert steps == -test_steps

    def test_interrupt(self):
        stepper = Stepper()
        def interrupt():
            # interrupt stepper thread after 50ms
            time.sleep(0.005)
            stepper.interrupt()
        # 1st test
        thread = Thread(target=interrupt)
        thread.start()
        steps = stepper.rotate_by_steps(100)
        #print("steps=", steps, ", current=", stepper.current_step)
        assert steps in range(4,7)
        assert stepper.current_step == steps
        # 2nd test
        stepper.reset()
        thread = Thread(target=interrupt)
        thread.start()
        steps = stepper.rotate_by_steps(-100)
        #print("steps=", steps, ", current=", stepper.current_step)
        assert steps in range(-6,-3)
        assert stepper.current_step == stepper.number_of_steps + steps

    def test_rotate_by_angle(self):
        stepper = Stepper(base_time=0.00001)
        # rotate 180 degrees
        steps = stepper.rotate_by_angle(1.0)
        assert steps == 800
        assert stepper.current_step == 800
        # rotate -270 degrees
        steps = stepper.rotate_by_angle(-1.5)
        assert steps == -1200
        assert stepper.current_step == 1200

    def test_set_angle(self):
        stepper = Stepper(base_time=0.00001)
        # 180 degrees
        steps = stepper.set_angle(1.0)
        assert steps == 800
        assert stepper.current_step == 800
        # 45 degrees
        steps = stepper.set_angle(0.25)
        assert steps == -600
        assert stepper.current_step == 200
        # -90 degrees
        steps = stepper.set_angle(-0.5)
        assert steps == -600
        assert stepper.current_step == 1200

    # def test_setAngle(self):
    #     with patch('asterisk_mirror.stepper.Stepper') as StepperMock:
    #         stepper = StepperMock([1, 2, 3])
    #         stepper.foo()
    #         stepper.foo.assert_called()

if __name__ == '__main__':
    unittest.main()