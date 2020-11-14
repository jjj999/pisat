
import time
import unittest

import pigpio

from pisat.calc import press2alti
from pisat.core.logger import SensorController, LogQueue
from pisat.handler import PigpioI2CHandler
from pisat.model import cached_loggable, LinkedDataModelBase, linked_loggable
from pisat.sensor import Bme280, Bno055


NAME_BME280 = "bme280"
ADDRESS_BME280 = 0x76
NAME_BNO055 = "bno055"
ADDRESS_BNO055 = 0x28
COUNTS_SAMPLING = 100000


class LinkedDataModel(LinkedDataModelBase):
    
    press = linked_loggable(Bme280.DataModel.press, NAME_BME280)
    temp = linked_loggable(Bme280.DataModel.temp, NAME_BME280)
    acc = linked_loggable(Bno055.DataModel.acc, NAME_BNO055)
    
    @cached_loggable
    def altitude(self):
        return press2alti(self.press, self.temp)
    

class TestLogQueue(unittest.TestCase):
    
    def setUp(self) -> None:
        pi = pigpio.pi()
        handler_bme = PigpioI2CHandler(pi, ADDRESS_BME280)
        handler_bno = PigpioI2CHandler(pi, ADDRESS_BNO055)
        self.bme280 = Bme280(handler_bme, name=NAME_BME280)
        self.bno055 = Bno055(handler_bno, name=NAME_BNO055)
        self.sencon = SensorController(self.bme280, self.bno055, modelclass=LinkedDataModel)
        self.logque = LogQueue(LinkedDataModel)
        
    def test_path(self):
        path = self.logque.path
        first = path.split("_")[0]
        self.assertEqual(first, LinkedDataModel.__name__)
        
    def sample(self, counts: int):
        time_init = time.time()
        with self.logque:
            for _ in range(counts):
                self.logque.append(self.sencon.read())
        time_finish = time.time()
        
        print(f"time to sample {counts} data: {time_finish - time_init} [sec]")
        
    def test_append(self):
        self.sample(COUNTS_SAMPLING)
        
    def test_create_newfile(self):
        name_new_file = "test_new_file.csv"
        self.logque.create_newfile(name_new_file)
        self.assertEqual(self.logque.path, name_new_file)
        self.assertTrue(self.logque._first)
        
        self.sample(100)
        
    
if __name__ == "__main__":
    unittest.main()
