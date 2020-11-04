from time import time

import pisat.calculate.const as const
from pisat.core.logger import SensorController
from pisat.sensor.sensor import Bme280, Apds9301, SensorGroup
from pisat.calculate.adapter import AltitudeAdapter, AdapterGroup


bme280 = Bme280(debug=True)
apds = Apds9301(debug=True)
alti = AltitudeAdapter()

sgroup = SensorGroup(bme280, apds)
agroup = AdapterGroup(alti)

con = SensorController(sgroup, agroup)

log = lambda x: print(x, end="\n\n")

"""
init = time()
dn = con.dnames
log("time: {} sec".format(time() - init))

init = time()
searched = con.search(const.DATA_ALTITUDE)
log("time: {} sec".format(time() - init))

init = time()
res = con.read(const.DATA_ALTITUDE)
log("time: {} sec".format(time() - init))

log(res)
"""

con.ignore(const.DATA_PRESS)
con.ignore(const.DATA_HUM)
init = time()
res = con.read()
log("time: {} sec".format(time() - init))
log(res)