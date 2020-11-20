
import time
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
    def counts_readable(self):
        pass
    
    def close(self) -> None:
        pass
    
    def read(self, count: int) -> Tuple[int, bytes]:
        pass
    
    def readline(self, end: bytes = b'\n', timeout: float = 0.) -> bytes:
        result = bytearray()
        cursor = 0
        tail = len(end)
        time_last = - 1
        while True:
            if not self.counts_readable:
                if time_last < 0:
                    time_last = time.time()
                    continue
                if time.time() - time_last > timeout:
                    break
                else:
                    continue
            else:
                time_last = - 1
            
            count, char = self.read(1)
            result.extend(char)
            
            if ord(char) == end[cursor]:
                cursor += 1
                if cursor == tail:
                    break
            else:
                cursor = 0
            
        return bytes(result)
    
    def readlines(self, size: int = -1, end: bytes = b'\n') -> Tuple[bytes]:
        result = []
        if size < 0:
            while True:
                line = self.readline(end=end)
                if not len(line):
                    break
                result.append(line)
        else:
            for _ in range(size):
                result.append(self.readline(end=end))
                
        return result
    
    def write(self, data: Union[bytes, bytearray]) -> None:
        pass
        