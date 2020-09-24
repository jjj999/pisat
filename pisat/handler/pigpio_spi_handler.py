#! python3

"""

pisat.logger.sensors.handler_spi
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module is the wrapper of the pigpio.pi class,
especially about methods for SPI communication.

[author]
Yunhyeon Jeong, From The Earth 9th @Tohoku univ.

[info]
pigpio API
    http://abyz.me.uk/rpi/pigpio/python.html
"""


from typing import Optional, Tuple, Union
from enum import Enum

from pisat.util.platform import is_raspberry_pi
from pisat.handler.spi_handler_base import SPIHandlerBase

if is_raspberry_pi():
    import pigpio
    

class PigpioSPIHandler(SPIHandlerBase):
    
    class Channel(Enum):
        CHANNEL_0 = 0
        CHANNEL_1 = 1
        CHANNEL_2 = 2
        CHANNELS = (CHANNEL_0, CHANNEL_1, CHANNEL_2)
        
        @classmethod
        def is_valid(cls, channel: int) -> bool:
            if channel in cls.CHANNELS:
                return True
            else:
                return False
            
    class Baudrate(Enum):
        MAX = 125_000_000
        MIN = 32_000
        
        @classmethod
        def is_valid(cls, baudrate: int) -> bool:
            if cls.MIN.value <= baudrate <= cls.MAX.value:
                return True
            else:
                return False

    def __init__(self,
                 pi,
                 channel: int,
                 baudrate: int,
                 flag: int = 0,
                 name: Optional[str] = None) -> None:
        super().__init__(baudrate, name=name)
        
        self._pi: pigpio.pi = pi
        self._handle: int = pi.spi_open(channel, baudrate, spi_flags=flag)
        self._channel: int = channel

    @property
    def channel(self):
        return self._channel

    @property
    def handle(self):
        return self._handle

    def close(self) -> bool:
        self._pi.spi_close(self._handle)

    def read(self, count: int) -> Tuple[int, bytes]:
        if count < 0:
            ValueError(
                "'count' must be no less than 0."
            )
        
        data = self._pi.spi_read(self._handle, count)
        return (data[0], bytes(data[1]))

    def write(self, data: Union[bytes, bytearray]) -> None:
        self._pi.spi_write(self._handle, data)
    
    def xfer(self, data: Union[bytes, bytearray]) -> Tuple[int, bytes]:
        data = self._pi.spi_xfer(self._handle, data)
        return (data[0], bytes(data[1]))
