
from typing import Optional

from pisat.handler.handler_base import HandlerBase


class DigitalIOHandlerBase(HandlerBase):
    
    def __init__(self, 
                 pin: int, 
                 name: Optional[str] = None) -> None:
        super().__init__(name=name)
        
        self._pin: int = pin
        
    @property
    def pin(self):
        return self._pin
