
from typing import Optional, Tuple, Union
from enum import Enum

import pigpio

from pisat.handler.serial_handler_base import SerialHandlerBase


class PigpioSerialHandler(SerialHandlerBase):
    
    class Baudrate(Enum):
        RATE_50 = 50
        RATE_75 = 75
        RATE_110 = 110
        RATE_134 = 134
        RATE_150 = 150
        RATE_200 = 200
        RATE_300 = 300
        RATE_600 = 600
        RATE_1200 = 1200
        RATE_1800 = 1800
        RATE_2400 = 2400
        RATE_4800 = 4800
        RATE_9600 = 9600
        RATE_19200 = 19200
        RATE_38400 = 38400
        RATE_57600 = 57600
        RATE_115200 = 115200
        RATE_230400 = 230400
        
        @classmethod
        def is_valid(cls, baudrate: int) -> bool:
            for rate in cls:
                if baudrate == rate.value:
                    return True
            return False
    
    def __init__(self,
                 pi: pigpio.pi,
                 port: str,
                 baudrate: int = 115200,
                 name: Optional[str] = None) -> None:
        super().__init__(port, baudrate, name=name)
        
        if not self.Baudrate.is_valid(baudrate):
            raise ValueError(
                "Given 'baudrate' is invalid."
            )
        
        self._pi: pigpio.pi = pi
        self._handle: int = pi.serial_open(port, baudrate)
        
    @property
    def handle(self):
        return self._handle
    
    @property
    def in_waiting(self):
        self._pi.serial_data_available(self._handle)
        
    def close(self) -> None:
        self._pi.serial_close(self._handle)
        
    def read(self, count: int) -> Tuple[int, bytes]:
        if count < 0:
            ValueError("'count' must be no less than 0.")
            
        data = self._pi.serial_read(self._handle, count)
        return (data[0], bytes(data[1]))
    
    def write(self, data: Union[bytes, bytearray]) -> None:
        self._pi.serial_write(self._handle, data)
        