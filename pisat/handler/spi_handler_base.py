
from typing import Optional, Tuple, Union

from pisat.handler.handler_base import HandlerBase


class SPIHandlerBase(HandlerBase):
    
    def __init__(self, 
                 baudrate: int, 
                 name: Optional[str] = None) -> None:
        super().__init__(name=name)
        
        self._baudrate = baudrate
        
    @property
    def baudrate(self):
        return self._baudrate
    
    def close(self) -> None:
        pass
    
    def read(self, count: int) -> Tuple[int, bytes]:
        pass
    
    def write(self, data: Union[bytes, bytearray]) -> None:
        pass
    
    def xfer(self, data: Union[bytes, bytearray]) -> Tuple[int, bytes]:
        pass
    