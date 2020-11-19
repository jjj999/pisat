

from pisat.sensor import bno055
import unittest

import pigpio

from pisat.calc.altitude import press2alti
from pisat.handler import PigpioI2CHandler
from pisat.model import cached_loggable, LinkedDataModelBase, linked_loggable
from pisat.sensor import Bme280, Bno055, SensorGroup


NAME_BME280 = "bme280"
NAME_BNO055 = "bno055"
ADDRESS_BME280 = 0x76
ADDRESS_BNO055 = 0x28


class LinkedDataModel(LinkedDataModelBase):
    
    press = linked_loggable(Bme280.DataModel.press, NAME_BME280)
    temp = linked_loggable(Bme280.DataModel.temp, NAME_BME280)
    acc = linked_loggable(Bno055.DataModel.acc, NAME_BNO055)
    
    @cached_loggable
    def altitude(self):
        return press2alti(self.press, self.temp)
    
    
class TestSensorController(unittest.TestCase):
    
    def setUp(self) -> None:
        pi = pigpio.pi()
        handler_bme = PigpioI2CHandler(pi, ADDRESS_BME280)
        handler_bno = PigpioI2CHandler(pi, ADDRESS_BNO055)
        self.bme280 = Bme280(handler_bme, name=NAME_BME280)
        self.bno055 = Bno055(handler_bno, name=NAME_BNO055)
        self.bno055.change_operation_mode(self.bno055.OperationMode.NDOF)
        self.group = SensorGroup(LinkedDataModel, self.bme280, self.bno055, name="group")
        
    def test_model(self):
        self.assertEqual(self.group.model, LinkedDataModel)
        
    def test_read(self):
        for _ in range(10):
            data = self.group.read()
            
            print()
            for name, val in data.extract().items():
                print(f"{name}: {val}")
            print()
    
    def test_remove(self):
        self.group.remove(self.bme280)
        self.group.remove(self.bno055)
        self.assertEqual(len(self.group), 0)
        self.group.append(self.bme280)
        self.group.append(self.bno055)
        
    def test_get_sensors(self):
        dict_sensor = self.group.get_sensors()
        
        for key, val in dict_sensor.items():
            self.assertIn(key, (NAME_BME280, NAME_BNO055))
            self.assertIn(val, (self.bme280, self.bno055))
            
            
if __name__ == "__main__":
    unittest.main()
    