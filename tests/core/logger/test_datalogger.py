
from pisat.core.logger.datalogger import DataLogger
import time
import unittest

import pigpio

from pisat.calc import press2alti
from pisat.core.logger import LogQueue
from pisat.handler import PigpioI2CHandler
from pisat.model import cached_loggable, LinkedDataModelBase, linked_loggable
from pisat.sensor import Bme280, Bno055


NAME_BME280 = "bme280"
ADDRESS_BME280 = 0x76
NAME_BNO055 = "bno055"
ADDRESS_BNO055 = 0x28
COUNTS_SAMPLING = 10000


class LinkedDataModel(LinkedDataModelBase):
    
    press = linked_loggable(Bme280.DataModel.press, NAME_BME280)
    temp = linked_loggable(Bme280.DataModel.temp, NAME_BME280)
    acc = linked_loggable(Bno055.DataModel.acc, NAME_BNO055)
    
    @cached_loggable
    def altitude(self):
        return press2alti(self.press, self.temp)
    
    
class TestDataLogger(unittest.TestCase):
    
    def setUp(self) -> None:
        pi = pigpio.pi()
        handler_bme = PigpioI2CHandler(pi, ADDRESS_BME280)
        handler_bno = PigpioI2CHandler(pi, ADDRESS_BNO055)
        self.bme280 = Bme280(handler_bme, name=NAME_BME280)
        self.bno055 = Bno055(handler_bno, name=NAME_BNO055)
        self.logque = LogQueue(LinkedDataModel)
        self.dlogger = DataLogger(self.logque, self.bme280, self.bno055)
        
    def sample(self, counts: int):
        self.dlogger.set_model(LinkedDataModel)
        
        time_init = time.time()
        with self.dlogger:
            for _ in range(counts):
                data = self.dlogger.read()
                self.assertTrue(isinstance(data, LinkedDataModel))
        time_finish = time.time()
        
        print(f"time to sample {counts} data: {time_finish - time_init} [sec]")
        
    def test_read(self):
        self.sample(COUNTS_SAMPLING)
        
        
if __name__ == "__main__":
    unittest.main()
    