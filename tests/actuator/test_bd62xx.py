
import time
import unittest

import pigpio

from pisat.actuator import BD62xx
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

class TestBD62xx(unittest.TestCase):
    
    def setUp(self) -> None:
        pi = pigpio.pi()
        handler_L_fin = PigpioPWMHandler(pi, PIN_L_FIN, FREQUENCY, name=NAME_L_FIN)
        handler_L_rin = PigpioPWMHandler(pi, PIN_L_RIN, FREQUENCY, name=NAME_L_RIN)
        handler_R_fin = PigpioPWMHandler(pi, PIN_R_FIN, FREQUENCY, name=NAME_R_FIN)
        handler_R_rin = PigpioPWMHandler(pi, PIN_R_RIN, FREQUENCY, name=NAME_R_RIN)

        self.driver_L = BD62xx(handler_L_fin, handler_L_rin, name="driverL")
        self.driver_L.brake()
        self.driver_R = BD62xx(handler_R_fin, handler_R_rin, name="driverR")
        
    def test_ccw(self):
        print("test ccw")
        for i, j in zip(range(500), range(500, 1000)):
            self.driver_L.ccw(i / 10)
            self.driver_R.cw(j / 10)
            time.sleep(0.01)
        self.driver_L.brake()
        self.driver_R.brake()
        
    def test_cw(self):
        print("test cw")
        for i in range(1000):
            self.driver_L.cw(i / 10)
            self.driver_R.ccw(i / 10)
            time.sleep(0.01)
        self.driver_L.brake()
        self.driver_R.brake()
        
        
if __name__ == "__main__":
    unittest.main()
