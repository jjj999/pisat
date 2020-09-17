
from typing import Optional, Tuple, Union

from pisat.handler.handler_base import HandlerBase


class I2CHandlerBase(HandlerBase):
    
    def __init__(self,
                 address: int, 
                 bus: int = 1, 
                 name: Optional[str] = None) -> None:
        super().__init__(name=name)
        
        self._address: int = address
        self._bus: int = bus
        
    @property
    def address(self):
        return self._address
    
    @property
    def bus(self):
        return self._bus
    
    def close(self) -> None:
        pass
    
    def read(self, reg: int, count: int) -> Tuple[int, bytearray]:
        pass
    
    def write(self, reg: int, data: Union[bytes, bytearray]) -> None:
        pass
    