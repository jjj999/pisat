
from os import name
from typing import *
import time

from pisat.core.cansat import CanSat
from pisat.core.logger import (
    SensorController, LogQueue, DataLogger, SystemLogger
)
from pisat.core.manager import ComponentManager
from pisat.core.nav import Node, Context
import pisat.config.dname as dname
from pisat.sensor.sensor import Bme280, SensorGroup, Apds9301
from pisat.adapter import BarometerAdapter, AdapterGroup


bme280 = Bme280(debug=True)
apds9301 = Apds9301(debug=True)
barometer = BarometerAdapter()
con = SensorController(SensorGroup(bme280, apds9301), AdapterGroup(barometer))
queue = LogQueue(1000, con.dnames)
dlogger = DataLogger(con, queue)
slogger = SystemLogger()
slogger.setFileHandler()

manager = ComponentManager(dlogger, slogger, recursive=True)


class TestNode1(Node):

    def enter(self):
        self.bme280 = bme280
        self.slogger: SystemLogger = self.manager.get_component("SystemLogger")

    def judge(self, data: Dict[str, Any]) -> bool:
        if data[dname.PRESSURE] > 50.:
            return True
        else:
            return False


class TestNode2(Node):

    def enter(self):
        self.counter = 0
        self.dlogger: DataLogger = self.manager.get_component("DataLogger")
        self.dlogger.ignore(dname.PRESSURE)

    def judge(self, data: Dict[str, Any]) -> bool:

        self.counter += 1
        if self.counter > 1000:
            return True
        else:
            return False

    def control(self):
        while True:

            if not self.event.is_set():
                ref = dlogger.get_ref()
            else:
                break


class FallingNode(Node):

    def enter(self):
        dlogger = self.manager.get_component("DataLogger")
        bme280 = self.manager.get_component("Bme280")
        dlogger.reset(bme280)

    def judge(self, data: Dict[str, Any]) -> bool:
        if data[dname.ALTITUDE_SEALEVEL] < 40000:
            return True
        else:
            return False


context = Context({
    TestNode1: {True: TestNode2, False: TestNode1},
    TestNode2: {True: FallingNode, False: TestNode2},
    FallingNode: {True: None, False: FallingNode}
},
    start=TestNode1)

cansat = CanSat(context, manager, dlogger=dlogger, slogger=slogger)

init_time = time.time()
cansat.run()
print("time: {} sec".format(time.time() - init_time))
