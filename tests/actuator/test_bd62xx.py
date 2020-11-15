
import time
import unittest

import pigpio

from pisat.actuator import BD62xx
from pisat.handler import PigpioPWMHandler


PIN_FIN = 13
NAME_FIN = "fin"
PIN_RIN = 19
NAME_RIN = "rin"
FREQUENCY = 40000


class TestBD62xx(unittest.TestCase):
    
    def setUp(self) -> None:
        pi = pigpio.pi()
        handler_fin = PigpioPWMHandler(pi, PIN_FIN, FREQUENCY, name=NAME_FIN)
        handler_rin = PigpioPWMHandler(pi, PIN_RIN, FREQUENCY, name=NAME_RIN)

        self.driver = BD62xx(handler_fin, handler_rin, name="driver")
        
    def test_ccw(self):
        for i in range(1000):
            self.driver.ccw(i / 10)
            time.sleep(0.05)
        self.driver.brake()
        
    def test_cw(self):
        for i in range(1000):
            self.driver.cw(i / 10)
            time.sleep(0.05)
        self.driver.brake()
        
        
if __name__ == "__main__":
    unittest.main()
