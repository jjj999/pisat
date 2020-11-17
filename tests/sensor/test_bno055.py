

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
    
    def test_bench_mark(self):
        result = self.testor.exec_benchmark()
        print(f"time to read 100 times: {result}")
     
    def test_remap(self):
        
        print("Current Axis Map")
        print("----------------")
        print(f"x: {self.bno055.axis_x}, sign: {self.bno055.sign_x}")
        print(f"y: {self.bno055.axis_y}, sign: {self.bno055.sign_y}")
        print(f"z: {self.bno055.axis_z}, sign: {self.bno055.sign_z}")
        print()
        
        self.bno055.remap_axis(self.bno055.Axis.Y, self.bno055.Axis.X, self.bno055.Axis.Z)
        self.bno055.remap_sign(x=self.bno055.AxisSign.NEGATIVE)
        print("Axes remapped.", end="\n\n")
        self.bno055._read_map_config()
        self.bno055._read_map_sign()
        
        print("New Axis Map")
        print("----------------")
        print(f"x: {self.bno055.axis_x}, sign: {self.bno055.sign_x}")
        print(f"y: {self.bno055.axis_y}, sign: {self.bno055.sign_y}")
        print(f"z: {self.bno055.axis_z}, sign: {self.bno055.sign_z}")
        print()
        
        # reset
        self.bno055.reset_axis()
        self.bno055.reset_sign()
        
    def test_calibration(self):
        print()
        print("Calibration status")
        print("------------------")

        self.bno055.load_calib_stat()
        print(f"sys: {self.bno055.calib_stat_sys}")
        print(f"acc: {self.bno055.calib_stat_acc}")
        print(f"mag: {self.bno055.calib_stat_mag}")
        print(f"gyro: {self.bno055.calib_stat_gyro}")
        
    def test_observe(self):
        self.bno055.remap_axis(self.bno055.Axis.Y, self.bno055.Axis.X, self.bno055.Axis.Z)
        self.bno055.remap_sign(z=self.bno055.AxisSign.NEGATIVE)        
        self.testor.observe()

        
if __name__ == "__main__":
    unittest.main()