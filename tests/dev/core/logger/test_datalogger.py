import time
from collections import deque

from memory_profiler import profile

from pisat.sensor.sensor import Bme280, Apds9301
from pisat.calculate.adapter import AltitudeAdapter, AdapterGroup
from pisat.core.logger import DataLogger, Logque, SensorController


path_data = "../../../data/test.csv"
data = deque()

@profile        
def main():
    bme = Bme280(debug=True)
    apds = Apds9301(debug=True)
    alti = AltitudeAdapter()
    con = SensorController(bme + apds, AdapterGroup(alti))
    que = Logque(100, dnames=con.dnames)
    
    with DataLogger(con, que) as logger:
        for _ in range(100000):
            logger.read()
            
    print(que._dnames)
    print(len(que._dnames))

            
init = time.time()
main()
time = time.time() - init

print("time of main: {} sec".format(time))