

import unittest

import pigpio

from pisat.handler import PigpioI2CHandler
from pisat.sensor import Opt3002
from pisat.tester.sensor import SensorTestor


ADDRESS_OPT3002 = 0x68


class TestOPT3002(unittest.TestCase):
    
    def setUp(self) -> None:
        pi = pigpio.pi()
        handler = PigpioI2CHandler(pi, ADDRESS_OPT3002)
        self.opt3002 = Opt3002(handler, name="apds9301")
        self.testor = SensorTestor(self.opt3002)
        
    def test_observe(self):
        self.testor.print_data()
        
    def test_bench_mark(self):
        result = self.testor.exec_benchmark(show=True)
        print(f"time to read 100 times: {result}")
        
        
if __name__ == "__main__":
    unittest.main()