#! python3

"""

pisat.logger.sensors.handler_i2c
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module is the wrapper of the pigpio.pi class,
especially about methods for I2C communication.

[author]
Yunhyeon Jeong, From The Earth 9th @Tohoku univ.

[info]
pigpio API
    http://abyz.me.uk/rpi/pigpio/python.html
    
"""

from typing import *

import pigpio

from pisat.handler.i2c_handler_base import I2CHandlerBase


class PigpioI2CHandler(I2CHandlerBase):

    def __init__(self,
                 pi: pigpio.pi,
                 address: int,
                 bus: int = 1,
                 flag: int = 0,
                 name: Optional[str] = None):
        super().__init__(address, bus, name=name)
        
        self._pi: pigpio.pi = pi
        self._handle: int = pi.i2c_open(bus, address, i2c_flags=flag)

    @property
    def handle(self):
        return self._handle

    def close(self) -> None:
        self._pi.i2c_close(self._handle)

    def read(self, reg: int, count: int) -> Tuple[int, bytearray]:
        if reg < 0:
            ValueError(
                "'reg' must be no less than 0."
            )
            
        data = self._pi.i2c_read_i2c_block_data(self._handle, reg, count)
        return data[0], bytes(data[1])

    def write(self, reg: int, data: Union[bytes, bytearray]) -> None:
        if reg < 0:
            ValueError(
                "'reg' must be no less than 0."
            )

        self._pi.i2c_write_i2c_block_data(self._handle, reg, data)
