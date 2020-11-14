
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

    def read_seq_byte(self, *regs: int) -> Tuple[int, bytearray]:
        result = bytearray()
        total = 0
        for reg in regs:
            count, raw = self.read(reg, 1)
            total += count
            result.extend(raw)

        return (total, result)

    def write(self, reg: int, data: Union[int, bytes, bytearray]) -> None:
        pass
    