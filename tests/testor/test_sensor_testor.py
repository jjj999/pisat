

import unittest

import pigpio

from pisat.handler import PigpioI2CHandler
from pisat.sensor import Bme280
from pisat.tester.sensor import SensorTestor


ADDRESS_BME280 = 0x76


class TestSensorTestor(unittest.TestCase):
    
    def setUp(self) -> None:
        pi = pigpio.pi()
        handler = PigpioI2CHandler(pi, ADDRESS_BME280)
        self.bme280 = Bme280(handler, name="bme280")
        self.testor = SensorTestor(self.bme280)
        
    def test_print_data(self):
        self.testor.print_data()
        
    def test_benchmark(self):
        result = self.testor.exec_benchmark()
        self.assertGreater(result, 0.1)
        
        
if __name__ == "__main__":
    unittest.main()
