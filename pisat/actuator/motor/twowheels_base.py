#! python3

"""

pisat.actuator.motor.twowheels_base
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



[author]
Taiki Okada, From The Earth 10th @Tohoku univ.
Yunhyeon Jeong, From The Earth 9th @Tohoku univ.

[info]
pigpio API
    http://abyz.me.uk/rpi/pigpio/python.html

"""

from typing import *

import pigpio as gpio

from pisat.base.component import Component
from pisat.actuator.motor.motor_base import MotorBase


class TwoWheelsBase(Component):

    def __init__(self,
                 lmot:MotorBase,
                 rmot:MotorBase):

        self.lmot:MotorBase = lmot
        self.rmot:MotorBase = rmot

        self.now_duty:int = 0


    def standby(self) -> None:
        self.lmot.standby()
        self.rmot.standby()


    def brake(self) -> None:
        self.lmot.brake()
        self.rmot.brake()


    def pwm(self, lmot:int, rmot:int) -> None:

        if lmot > 0:
            self.lmot.ccw(lmot)
        else:
            self.lmot.cw(lmot)

        if rmot > 0:
            self.rmot.ccw(rmot)
        else:
            self.rmot.cw(rmot)

    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
    #   clockwise, counterclockwise
    #
    #   NOTE
    #   1. Problem about not matching pwm mode
    #       This problem is solved in motor_base.py.
    #       Check "pisat.act.motor.motor_base.py"
    #
    #   2. Which direction is clockwise and counterclockwise?
    #       We defines the clockwise is clockwise direction when you see
    #       terminals of a motor.
    #
    #   3. Positive and Negative duty
    #       duty >= 0 --> body move forward or stay
    #       duty <  0 --> body moves backward
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    def forward(self, duty:int):    # duty >= 0
        self.pwm(- duty, duty)      # R -> ccw, L -> cw
        self.now_duty = duty


    def backward(self, duty:int):   # duty >= 0
        self.pwm(duty, - duty)      # R -> cw, L -> ccw
        self.now_duty = - duty


    def cw(self, p:float, base:Optional[int]=None) -> None:     # p >= 0.

        if base is not None:
            self.now_duty = base

        if self.now_duty >= 0:
            self.pwm(- self.now_duty, int(self.now_duty / p))
        else:
            self.pwm(- int(self.now_duty / p), self.now_duty)


    def ccw(self, p:float, base:Optional[int]=None) -> None:

        if base is not None:
            self.now_duty = base

        if self.now_duty >= 0:
            self.pwm(- int(self.now_duty / p), self.now_duty)
        else:
            self.pwm(- self.now_duty, int(self.now_duty / p))


    def rturn(self, duty:int) -> None:    # duty >= 0
        self.pwm(- duty, - duty)          # R -> cw, L -> cw


    def lturn(self, duty:int) -> None:    # duty >= 0
        self.pwm(duty, duty)      # R -> ccw, L -> ccw
