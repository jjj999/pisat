#! python3

"""

FILE NAME
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DESCRIPTION


[author]
AUTHOR NAME, ORGANIZATION NAME

[info]
OTHER INFORMATION
    
"""

from typing import List, Optional, Tuple, Union
from enum import Enum

from serial import Serial

from pisat.handler.serial_handler_base import SerialHandlerBase


class PyserialSerialHandler(SerialHandlerBase):
    
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
        RATE_460800 = 460800
        RATE_500000 = 500000
        RATE_576000 = 576000
        RATE_921600 = 921600
        RATE_1000000 = 1000000
        RATE_1152000 = 1152000
        RATE_1500000 = 1500000
        RATE_2000000 = 2000000
        RATE_2500000 = 2500000
        RATE_3000000 = 3000000
        RATE_3500000 = 3500000
        RATE_4000000 = 4000000
        
        @classmethod
        def is_valid(cls, baudrate: int) -> bool:
            for rate in cls:
                if baudrate == rate.value:
                    return True
            return False

    def __init__(self,
                 port: str,
                 baudrate: int = 115200,
                 read_timeout: Optional[float] = None,
                 write_timeout: Optional[float] = None):

        self._serial: Serial = Serial(port,
                                      baudrate=baudrate,
                                      timeout=read_timeout,
                                      write_timeout=write_timeout)

    @property
    def counts_readable(self):
        return self._serial.in_waiting

    @property
    def counts_writable(self):
        return self._serial.out_waiting

    def read(self, count: int) -> Tuple[int, bytes]:
        if count < 0:
            raise ValueError(
                "'count' must be no less than 0."
            )
        res = self._serial.read(size=count)
        return (len(res), res)

    def write(self, data: Union[bytes, bytearray]) -> None:
        self._serial.write(data)
        
    def flush(self) -> None:
        self._serial.flush()
