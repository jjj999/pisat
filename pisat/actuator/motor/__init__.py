#! python3
"""

pisat.actuator.motor
~~~~~~~~~~~~~~~~~~~~



[contributer]
Taiki Okada, From The Earth 10th @Tohoku univ.
Yunhyeon Jeong, From The Earth 9th @Tohoku univ.

[info]
pigpio API
    http://abyz.me.uk/rpi/pigpio/python.html
    
"""

from pisat.actuator.motor.motor_base import MotorBase, UnablePWMmodeError
from pisat.actuator.motor.twowheels_base import TwoWheelsBase