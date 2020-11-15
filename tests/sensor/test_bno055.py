

import time
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
        self.bno055.change_operation_mode(Bno055.OperationMode.NDOF)
        self.testor = SensorTestor(self.bno055)
        
    def test_observe(self):
        self.testor.observe(100)
        
    def test_bench_mark(self):
        result = self.testor.exec_benchmark(show=True)
        print(f"time to read 100 times: {result}")
        
    def test_remap(self):
        print(self.bno055.axis_z)
        self.bno055.remap_axis(z_sign=Bno055.AxisSign.POSITIVE)
        print("Z axis remapped.")
        time.sleep(5)
        self.testor.observe(100)
        
        
if __name__ == "__main__":
    unittest.main()