
from typing import Optional
from pisat.handler.digital_io_handler_base import DigitalIOHandlerBase


class DigitalOutputHandlerBase(DigitalIOHandlerBase):
    
    def __init__(self,
                 pin: int,
                 default: bool = False,
                 name: Optional[str] = None) -> None:
        super().__init__(pin, name=name)
        
        if default:
            self.set_high()
    
    def set_high(self) -> None:
        pass
    
    def set_low(self) -> None:
        pass