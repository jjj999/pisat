
from time import time

import pisat.calculate.const as const
from pisat.calculate.adapter import AltitudeAdapter, AdapterGroup
from pisat.sensor.sensor import Bme280


init_time = time()
bme = Bme280(debug=True)
alti = AltitudeAdapter()
group = AdapterGroup(alti)
print("done init: {} sec".format(time() - init_time))

init_time = time()
res = alti.supply(bme.read())
print("calc time: {} sec".format(time() - init_time))

print(res)

print(group.supply(bme.read()))