
import time
import unittest

import pigpio

from pisat.actuator import BD62xx, TwoWheels
from pisat.handler import PigpioPWMHandler


PIN_L_FIN = 12
NAME_L_FIN = "l_fin"
PIN_L_RIN = 18
NAME_L_RIN = "l_rin"
PIN_R_FIN = 13
NAME_R_FIN = "r_fin"
PIN_R_RIN = 19
NAME_R_RIN = "r_rin"
FREQUENCY = 40000


class TestTwoWheels(unittest.TestCase):
    
    def setUp(self) -> None:
        pi = pigpio.pi()
        handler_l_fin = PigpioPWMHandler(pi, PIN_L_FIN, FREQUENCY, name=NAME_L_FIN)
        handler_l_rin = PigpioPWMHandler(pi, PIN_L_RIN, FREQUENCY, name=NAME_L_RIN)
        handler_r_fin = PigpioPWMHandler(pi, PIN_R_FIN, FREQUENCY, name=NAME_R_FIN)
        handler_r_rin = PigpioPWMHandler(pi, PIN_R_RIN, FREQUENCY, name=NAME_R_RIN)
        
        driver_L = BD62xx(handler_l_fin, handler_l_rin, "left")
        driver_R = BD62xx(handler_r_fin, handler_r_rin, "right")
        self.wheels = TwoWheels(driver_L, driver_R, name="wheels")
        
