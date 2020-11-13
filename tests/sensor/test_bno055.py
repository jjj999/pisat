

import unittest

import pigpio

from pisat.handler import PigpioI2CHandler
from pisat.sensor import Bno055
from pisat.tester.sensor import SensorTestor


ADDRESS_BNO055 = 0x28


class TestBNO055(unittest.TestCase):
    
    def setUp(self) -> None:
        pi = pigpio.pi()
        handler = PigpioI2CHandler(pi, ADDRESS_BNO055)
        self.bno055 = Bno055(handler, name="bno055")
        self.testor = SensorTestor(self.bno055)
        
    def test_observe(self):
        self.testor.print_data()
        
    def test_bench_mark(self):
        result = self.testor.exec_benchmark(show=True)
        print(f"time to read 100 times: {result}")
        
        
if __name__ == "__main__":
    unittest.main()