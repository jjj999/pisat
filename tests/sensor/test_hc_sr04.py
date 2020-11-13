

import unittest

import pigpio

from pisat.handler import PigpioDigitalInputHandler, PigpioDigitalOutputHandler
from pisat.sensor import HcSr04
from pisat.tester.sensor import SensorTestor


PIN_IN = 21
PIN_OUT = 20


class TestBNO055(unittest.TestCase):
    
    def setUp(self) -> None:
        pi = pigpio.pi()
        handler_in = PigpioDigitalInputHandler(pi, PIN_IN, name="echo")
        handler_out = PigpioDigitalOutputHandler(pi, PIN_OUT, name="trigger")
        self.hcsr04 = HcSr04(handler_in, handler_out, name="hcsr04")
        self.testor = SensorTestor(self.hcsr04)
        
    def test_observe(self):
        self.testor.print_data()
        
    def test_bench_mark(self):
        result = self.testor.exec_benchmark(show=True)
        print(f"time to read 100 times: {result}")
        
        
if __name__ == "__main__":
    unittest.main()