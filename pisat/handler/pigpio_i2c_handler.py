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

from pisat.util.platform import is_raspberry_pi
from pisat.handler.i2c_handler_base import I2CHandlerBase

if is_raspberry_pi():
    import pigpio

class PigpioI2CHandler(I2CHandlerBase):
    
    MAX_LEN_READ = 32

    def __init__(self,
                 pi,
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
            raise ValueError(
                "'reg' must be no less than 0."
            )
        if count > self.MAX_LEN_READ:
            raise ValueError(
                f"'count' is out of range. It must be 0 <= 'count' <= {self.MAX_LEN_READ}."
            )
            
        counts, raw = self._pi.i2c_read_i2c_block_data(self._handle, reg, count)
        return counts, raw

    def write(self, reg: int, data: Union[int, bytes, bytearray]) -> None:
        if reg < 0:
            ValueError(
                "'reg' must be no less than 0."
            )

        if isinstance(data, int):
            self._pi.i2c_write_byte_data(self._handle, reg, data)
        else:
            self._pi.i2c_write_i2c_block_data(self._handle, reg, data)
