from time import time
from pprint import pprint

import pisat.sensor.const as const
from pisat.sensor.sensor import SensorGroup
from pisat.sensor.sensor import Bme280, Apds9301



bme280 = Bme280(debug=True)
bme280_2 = Bme280(debug=True)
bme280_3 = Bme280(debug=True)
apds9301 = Apds9301(debug=True)
apds9301_2 = Apds9301(debug=True)

group = SensorGroup(bme280, bme280_2, apds9301)
group_2 = SensorGroup(bme280_3, apds9301_2)

group.extend(group_2)

init_time = time()
res = group.read()
print("time : {}".format(time() - init_time))
pprint(res)

pprint(group.readf())
group.concentrate(const.DATA_PRESS, bme280)
pprint(group.readf())
pprint(group._DtoS)
