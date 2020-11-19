
from pisat.sensor import bno055
from pisat.sensor import bme280
import time
import unittest

import pigpio

from pisat.calc import press2alti
from pisat.core.cansat import CanSat
from pisat.core.logger import (
    LogQueue, DataLogger, SystemLogger
)
from pisat.core.manager import ComponentManager
from pisat.core.nav import Node, Context
from pisat.handler import PigpioI2CHandler
from pisat.model import cached_loggable, LinkedDataModelBase, linked_loggable
from pisat.sensor import Bme280, Bno055


NAME_BME280 = "bme280"
ADDRESS_BME280 = 0x76
NAME_BNO055 = "bno055"
ADDRESS_BNO055 = 0x28
NAME_DLOGGER = "dlogger"
NAME_SLOGGER = "slogger"


class LinkedDataModel(LinkedDataModelBase):
    
    press = linked_loggable(Bme280.DataModel.press, NAME_BME280)
    temp = linked_loggable(Bme280.DataModel.temp, NAME_BME280)
    acc = linked_loggable(Bno055.DataModel.acc, NAME_BNO055)
    
    @cached_loggable
    def altitude(self):
        return press2alti(self.press, self.temp)


class TestNode1(Node):
    
    model = LinkedDataModel

    def enter(self):
        self.slogger = self.manager.get_component(NAME_SLOGGER)

    def judge(self, data: LinkedDataModel) -> bool:
        self.slogger.info(f"judge called in {self.__class__.__name__}")
        
        if data.press > 900.:
            return True
        else:
            return False


class TestNode2(Node):
    
    model = LinkedDataModel

    def enter(self):
        self.counter = 0
        self.dlogger: DataLogger = self.manager.get_component(NAME_DLOGGER)

    def judge(self, data: LinkedDataModel) -> bool:

        self.counter += 1
        if self.counter > 1000:
            return True
        else:
            return False

    def control(self):
        while not self.event.is_set():
            ref = self.dlogger.refqueue
            time.sleep(0.001)


class TestCanSat(unittest.TestCase):
    
    def setUp(self) -> None:
        pi = pigpio.pi()
        handler_bme = PigpioI2CHandler(pi, ADDRESS_BME280)
        handler_bno = PigpioI2CHandler(pi, ADDRESS_BNO055)
        self.bme280 = Bme280(handler_bme, name=NAME_BME280)
        self.bno055 = Bno055(handler_bno, name=NAME_BNO055)
        self.logque = LogQueue(LinkedDataModel)
        self.dlogger = DataLogger(self.logque, self.bme280, self.bno055, name=NAME_DLOGGER)
        self.slogger = SystemLogger(name=NAME_SLOGGER)
        self.slogger.setFileHandler()
        self.manager = ComponentManager(self.dlogger, self.slogger, recursive=True)
                
        context = Context({TestNode1: {True: TestNode2, False: TestNode1},
                           TestNode2: {True: None, False: TestNode2}},
                           start=TestNode1)

        self.cansat = CanSat(context, self.manager, dlogger=self.dlogger, slogger=self.slogger)

    def test_run(self):
        init_time = time.time()
        self.cansat.run()
        print("time: {} sec".format(time.time() - init_time))
        
        
if __name__ == "__main__":
    unittest.main()
