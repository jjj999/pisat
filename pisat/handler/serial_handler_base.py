
from typing import Optional, Tuple, Union
from enum import Enum

from pisat.handler.handler_base import HandlerBase


class SerialHandlerBase(HandlerBase):
    
    class Port(Enum):
        USB_0 = "/dev/ttyUSB0"
        USB_1 = "/dev/ttyUSB1"
        USB_2 = "/dev/ttyUSB2"
        USB_3 = "/dev/ttyUSB3"
        UART = "/dev/serial0"
    
    def __init__(self,
                 port: str,
                 baudrate: int,
                 name: Optional[str] = None) -> None:
        super().__init__(name=name)
        
        self._port: str = port
        self._baudrate: int = baudrate
        
    @property
    def port(self):
        return self._port
    
    @property
    def baudrate(self):
        return self._baudrate
    
    @property
    def in_waiting(self):
        pass
    
    def close(self) -> None:
        pass
    
    def read(self, count: int) -> Tuple[int, bytes]:
        pass
    
    def write(self, data: Union[bytes, bytearray]) -> None:
        pass
        