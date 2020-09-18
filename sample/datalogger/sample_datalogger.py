
from os import name
import time

import pigpio

from pisat.handler import PigpioI2CHandler
from pisat.sensor import Bme280, Apds9301
from pisat.adapter import BarometerAdapter, AdapterGroup
from pisat.core.logger import DataLogger, SensorController, LogQueue


def main():
    
    NUM_LOGGING = 1000
    I2C_ADDRESS_BME280 = 0x77
    I2C_ADDRESS_APDS9301 = 0x39
    
    pi = pigpio.pi()
    handler_bme280 = PigpioI2CHandler(pi, I2C_ADDRESS_BME280, name="handler_bme280")
    handler_apds9301 = PigpioI2CHandler(pi, I2C_ADDRESS_APDS9301, name="handler_apds9301")
    
    bme280 = Bme280(handler_bme280)
    apds9301 = Apds9301(handler_apds9301)
    adapter_barometer = BarometerAdapter()
    
    con = SensorController(bme280 + apds9301, 
                           AdapterGroup(adapter_barometer))
    queue = LogQueue(500, dnames=con.dnames)
    counter = 0

    with DataLogger(con, queue) as dlogger:
        init_time = time.time()
        while counter < NUM_LOGGING:
            dlogger.read()
            counter += 1

    total_time = time.time() - init_time
    print("finish logging.")
    print("time: {} sec".format(total_time))
        
        
if __name__ == "__main__":
    main()
