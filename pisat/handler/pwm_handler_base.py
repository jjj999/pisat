
from typing import Optional, Union
from enum import Enum

from pisat.handler.digital_io_handler_base import DigitalIOHandlerBase


class PWMHandlerBase(DigitalIOHandlerBase):
    
    class Duty(Enum):
        MAX = 100.
        MIN = 0.
        
        @classmethod
        def is_valid(cls, duty: float) -> bool:
            if cls.MIN.value <= duty <= cls.MAX.value:
                return True
            else:
                return False
    
    def __init__(self,
                 pin: int,
                 freq: Union[int, float],
                 duty: Union[int, float] = 0,
                 name: Optional[str] = None) -> None:
        super().__init__(pin, name=name)
        
        self._freq: Union[int, float] = freq
        self._duty: Union[int, float] = duty        
    
    @property
    def duty(self):
        return self._duty
    
    @property
    def freq(self):
        return self._freq
    
    def set_duty(self, duty: float) -> None:
        pass
    
    def set_freq(self, freq: Union[int, float]) -> None:
        pass
    
    def start(self, duty: Optional[Union[int, float]] = None) -> None:
        pass
    
    def stop(self) -> None:
        pass
    