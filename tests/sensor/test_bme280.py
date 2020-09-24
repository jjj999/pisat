#! python3

"""

DESCRIPTION

[author]
AUTHOR NAME, ORGANIZATION NAME

[info]
OTHER INFORMATION
    
"""

import time

import pigpio

from pisat.sensor.handler import HandlerI2C
from pisat.sensor.sensor import Bme280


def readf_seq(bme280:Bme280, seq:int):
    time_init = time.time()
    for _ in range(seq):
        print(bme280.readf())
    print("time: ", time.time() - time_init)


def read_seq(bme280:Bme280, seq:int):
    data = {dname: [] for dname in Bme280.DATA_NAMES}
    
    for _ in range(seq):
        for dname, val in bme280.read().items():
            data[dname].append(val)
            
    return data


def print_const(bme280:Bme280):
    print("CHIP ID: ", bme280.id)
    print("MEASURING: ", bme280.measuring)
    print("IM_UPDATE", bme280.im_update)


if __name__ == "__main__":
    
    ADDRESS_I2C_BME280 = 0x77
    pi:pigpio.pi = pigpio.pi()
    handler:HandlerI2C = HandlerI2C(pi, ADDRESS_I2C_BME280)
    
    bme280:Bme280 = Bme280(handler)
   
    print_const(bme280)
