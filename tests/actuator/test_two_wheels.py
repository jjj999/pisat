
import time
import unittest

import pigpio

from pisat.actuator import BD62xx, TwoWheels
from pisat.handler import PigpioPWMHandler


PIN_L_FIN = 12
NAME_L_FIN = "l_fin"
PIN_L_RIN = 18
NAME_L_RIN = "l_rin"
PIN_R_FIN = 16
NAME_R_FIN = "r_fin"
PIN_R_RIN = 26
NAME_R_RIN = "r_rin"
FREQUENCY = 40000


class TestTwoWheels(unittest.TestCase):
    
    def setUp(self) -> None:
        pi = pigpio.pi()
        handler_L_fin = PigpioPWMHandler(pi, PIN_L_FIN, FREQUENCY, name=NAME_L_FIN)
        handler_L_rin = PigpioPWMHandler(pi, PIN_L_RIN, FREQUENCY, name=NAME_L_RIN)
        handler_R_fin = PigpioPWMHandler(pi, PIN_R_FIN, FREQUENCY, name=NAME_R_FIN)
        handler_R_rin = PigpioPWMHandler(pi, PIN_R_RIN, FREQUENCY, name=NAME_R_RIN)

        self.driver_L = BD62xx(handler_L_fin, handler_L_rin, name="driverL")
        self.driver_R = BD62xx(handler_R_fin, handler_R_rin, name="driverR")
        self.wheels = TwoWheels(self.driver_L, self.driver_R, name="wheels")

    def test_straight(self):
        self.wheels.straight(30)
        time.sleep(3)
        self.wheels.straight(50)
        time.sleep(3)
        self.wheels.straight(70)
        time.sleep(3)
        self.wheels.brake()

    def test_ccw(self):
        print("test_ccw")
        for i in range(100):
            self.wheels.ccw(i)
            time.sleep(0.1)
        self.wheels.brake()
        
    def test_cw(self):
        print("test_cw")
        for i in range(100):
            self.wheels.cw(i)
            time.sleep(0.1)
        self.wheels.brake()
        
    def test_curve_ccw(self):
        print("test_curve_ccw")
        self.wheels.straight(100)
        time.sleep(3)
        self.wheels.curve_ccw(50)
        time.sleep(5)
        self.wheels.brake()

        
if __name__ == "__main__":
    unittest.main()
