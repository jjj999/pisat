

import unittest

import pigpio

from pisat.handler import PigpioI2CHandler
from pisat.sensor import Apds9301
from pisat.tester.sensor import SensorTestor


ADDRESS_APDS9301 = 0x49


class TestAPDS9301(unittest.TestCase):
    
    def setUp(self) -> None:
        pi = pigpio.pi()
        handler = PigpioI2CHandler(pi, ADDRESS_APDS9301)
        self.apds9301 = Apds9301(handler, name="apds9301")
        self.testor = SensorTestor(self.apds9301)
        
    def test_observe(self):
        self.testor.print_data()
        
    def test_bench_mark(self):
        result = self.testor.exec_benchmark(show=True)
        print(f"time to read 100 times: {result}")
        
        
if __name__ == "__main__":
    unittest.main()
