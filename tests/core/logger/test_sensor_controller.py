

import unittest

import pigpio

from pisat.calc.altitude import press2alti
from pisat.core.logger import SensorController
from pisat.handler import PigpioI2CHandler
from pisat.model import cached_loggable, LinkedDataModelBase, linked_loggable
from pisat.sensor import Bme280


NAME_BME280 = "bme280"
ADDRESS_BME280 = 0x76


class LinkedDataModel(LinkedDataModelBase):
    
    press = linked_loggable(Bme280.DataModel.press, NAME_BME280)
    temp = linked_loggable(Bme280.DataModel.temp, NAME_BME280)
    
    @cached_loggable
    def altitude(self):
        return press2alti(self.press, self.temp)
    
    
class TestSensorController(unittest.TestCase):
    
    def setUp(self) -> None:
        pi = pigpio.pi()
        handler = PigpioI2CHandler(pi, ADDRESS_BME280)
        self.bme280 = Bme280(handler, name=NAME_BME280)
        self.sencon = SensorController(self.bme280, modelclass=LinkedDataModel, name="sencon")
        
    def test_model(self):
        self.assertEqual(self.sencon.model, LinkedDataModel)
        
    def test_read(self):
        for _ in range(10):
            data = self.sencon.read()
            
            print()
            for name, val in data.extract().items():
                print(f"{name}: {val}")
            print()
    
    def test_remove(self):
        self.sencon.remove(self.bme280)
        self.assertEqual(len(self.sencon), 0)
        self.sencon.append(self.bme280)
        
    def test_get_sensors(self):
        dict_sensor = self.sencon.get_sensors()
        
        for key, val in dict_sensor.items():
            self.assertEqual(key, NAME_BME280)
            self.assertEqual(val, self.bme280)
            
            
if __name__ == "__main__":
    unittest.main()
    